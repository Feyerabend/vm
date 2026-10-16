#!/usr/bin/env python3
"""
Compile a program for the machine into C.

Every instruction becomes the C code that the interpreter would have
run for it, with its operands written in as constants, behind a label
named after its address:

    A12: start = 12;                    PUSH 7
        push_int(7);
        goto A14;
    A14: start = 14;                    ADD
        { struct value w = pop(), v = pop();
          push_int(wrap_add(number(v), number(w))); }
        goto A15;

A jump to a known address is a goto. Where the address is known only
while running, after RET and CALLI, the code goes through a switch on
it. There is no loop, no fetching, and no decoding left: that is what
the interpreter spent much of its time on, and the C compiler can now
see, and optimise, the program as a whole.

Every address gets a label, not only those where an instruction
begins when the program is read from the start, since a program may
jump into the middle of an instruction. Everything that can trap,
traps as in the interpreter, with the same message, at the same
address, using the interpreter's own code in runtime.h.

A program that passes chapter 19's verification, here chapter 17's
analysis in flow.py with no instruction certain to trap, is compiled
without the checks the verification made: pops do not check for
underflow, LOAD and STORE do not check their locals, and only the
instructions that can be reached get code at all.

    usage: vm2c.py [-C] program.vm > program.c
           cc -O2 -I. program.c -o program

-C compiles every check in, as if the program had not verified.
"""

import sys

import flow
import isa
import vmfile

NOPERANDS = {code: len(kinds) for code, (name, kinds) in isa.BY_CODE.items()}

ARITHMETIC = {
    "ADD": "wrap_add(a, b)", "SUB": "wrap_sub(a, b)", "MUL": "wrap_mul(a, b)",
    "AND": "a & b", "OR": "a | b", "XOR": "a ^ b", "LT": "a < b",
}

SIMPLE = {
    "PRINT": 'printf("%d\\n", number(pop()));',
    "DUP": "{ struct value v = pop(); push(v); push(v); }",
    "DROP": "pop();",
    "SWAP": "{ struct value w = pop(), v = pop(); push(w); push(v); }",
    "OVER": "{ struct value w = pop(), v = pop(); push(v); push(w); push(v); }",
    "ROT": "{ struct value u = pop(), w = pop(), v = pop(); push(w); push(u); push(v); }",
    "EQ": "{ struct value w = pop(), v = pop(); push_int(same(v, w)); }",
    "LOADM": ("{ int a = number(pop());"
              " if (a < 0 || a >= MEMORY_SIZE) trap(\"no such memory address\");"
              " push(memory[a]); }"),
    "STOREM": ("{ struct value w = pop(); int a = number(pop());"
               " if (a < 0 || a >= MEMORY_SIZE) trap(\"no such memory address\");"
               " memory[a] = w; }"),
    "EMIT": ("{ int c = number(pop());"
             " if (c < 0 || c > 255) trap(\"not a character\"); putchar(c); }"),
    "NEW": "push(allocate(number(pop())));",
    "GETF": ("{ struct value w = pop(), v = pop(); int b = block(v);"
             " push(heap[field(b, number(w))]); }"),
    "SETF": ("{ struct value u = pop(), w = pop(), v = pop(); int b = block(v);"
             " heap[field(b, number(w))] = u; }"),
    "LEN": "push_int(heap[block(pop())].n);",
}


def verified(code):
    """The addresses that can be reached, if the program verifies."""
    try:
        depth, traps, _ = flow.analyse(code)
    except flow.Refused:
        return None
    if traps:
        return None
    return set(depth)


def compile_program(code, checked):
    n = len(code)
    out = []
    reachable = None if checked else verified(code)
    if reachable is not None:
        # In a verified program, these cannot fail: no need to check.
        out.append("#undef pop")
        out.append("#define pop() (stack[--sp])")
        out.append("#define local_at(k) (fp + (k))")

    def emit(line):
        out.append("    " + line)

    def call(a, ret, nargs_c):
        if reachable is None:
            emit(f"if ({nargs_c} < 0 || {nargs_c} > sp - fp) trap(\"not enough arguments\");")
        emit('if (fsp == FRAMES) trap("too many nested calls");')
        emit(f"frames[fsp].ret = {ret};")
        emit("frames[fsp].fp = fp;")
        emit("fsp++;")
        emit(f"fp = sp - {nargs_c};")

    sure = reachable is not None
    for a in range(n):
        if sure and a not in reachable:
            continue
        op = code[a]
        out.append(f"A{a}: start = {a};")
        if op not in isa.BY_CODE:
            emit('trap("unknown instruction");')
            continue
        name = isa.BY_CODE[op][0]
        have = n - a - 1                # words after the opcode
        operands = code[a + 1:a + 1 + NOPERANDS[op]]
        nxt = a + 1 + NOPERANDS[op]
        missing = 'trap("missing operand");'
        if name == "HALT":
            emit("return;")
            continue
        if name == "PUSH":
            if have < 1:
                emit(missing)
                continue
            emit(f"push_int({operands[0]});")
        elif name in ARITHMETIC:
            emit("{ struct value w = pop(), v = pop(); int a = number(v), b = number(w);"
                 f" push_int({ARITHMETIC[name]}); }}")
        elif name in ("DIV", "MOD"):
            f = "wrap_div" if name == "DIV" else "wrap_mod"
            emit("{ struct value w = pop(), v = pop(); int a = number(v), b = number(w);"
                 f' if (b == 0) trap("division by zero"); push_int({f}(a, b)); }}')
        elif name in SIMPLE:
            emit(SIMPLE[name])
        elif name in ("JMP", "JZ"):
            if have < 1:
                emit(missing)
                continue
            t = operands[0]
            if not 0 <= t < n:
                emit('trap("jump out of program");')
                continue
            if name == "JMP":
                emit(f"goto A{t};")
                continue
            emit(f"{{ struct value v = pop(); if (!v.is_ref && v.n == 0) goto A{t}; }}")
        elif name == "LOAD":
            if have < 1:
                emit(missing)
                continue
            emit(f"push(stack[local_at({operands[0]})]);")
        elif name == "STORE":
            if have < 1:
                emit(missing)
                continue
            k = operands[0]
            if sure:
                emit(f"stack[fp + {k}] = pop();")
            else:
                emit(f'{{ struct value v = pop(); if ({k} < 0 || fp + {k} >= sp) trap("no such local");'
                     f" stack[fp + {k}] = v; }}")
        elif name == "CALL":
            if have < 1:
                emit(missing)
                continue
            t = operands[0]
            if not 0 <= t < n:
                emit('trap("jump out of program");')
                continue
            if have < 2:
                emit(missing)
                continue
            call(a, nxt, str(operands[1]))
            emit(f"goto A{t};")
            continue
        elif name == "CALLI":
            if have < 1:
                emit(missing)
                continue
            emit("{ int t = number(pop());")
            emit(f'  if (t < 0 || t >= {n}) trap("jump out of program");')
            call(a, nxt, str(operands[0]))
            emit("  target = t; }")
            emit("goto dispatch;")
            continue
        elif name == "RET":
            emit("{ struct value v;" + ("" if sure else ' if (fsp == 0) trap("return without call");'))
            emit("  v = pop(); sp = fp; fsp--; target = frames[fsp].ret;")
            emit("  fp = frames[fsp].fp; push(v); }")
            emit("goto dispatch;")
            continue
        else:
            raise ValueError(name)
        emit(f"goto A{nxt};")
    out.append(f"A{n}: start = {n};")
    emit('trap("ran off the end of the program");')
    out.append("dispatch:")
    emit("switch (target) {")
    for a in range(n + 1):
        if sure and a not in reachable and a != n:
            continue
        emit(f"case {a}: goto A{a};")
    emit("}")
    emit("return;")

    body = "\n".join(out)
    note = "verified: compiled without the checks verification made" if sure else "not verified: every check compiled in"
    return f'''/* Compiled from a program for the machine by vm2c.py: {note}. */

#include "runtime.h"

static void run(void) {{
    int target = 0;

    (void) target;
{body}
}}

int main(int argc, char *argv[]) {{
    if (!run_options(argc, argv)) {{
        fprintf(stderr, "usage: %s [-g mark | -g copy] [-S] [-s]\\n", argv[0]);
        return 2;
    }}
    code_len = {n};
    heap_init();
    atexit(report);
    run();
    return 0;
}}
'''


def main():
    args = sys.argv[1:]
    checked = args[:1] == ["-C"]
    if checked:
        args = args[1:]
    if len(args) != 1:
        sys.exit("usage: vm2c.py [-C] program.vm > program.c")
    path = args[0]
    # A damaged file is reported exactly as the machine reports it.
    try:
        code = vmfile.read(path)
    except OSError:
        print(f"{path}: cannot open", file=sys.stderr)
        sys.exit(2)
    except vmfile.FormatError as e:
        print(f"{path}: {e}", file=sys.stderr)
        sys.exit(2)
    sys.stdout.write(compile_program(code, checked))


if __name__ == "__main__":
    main()
