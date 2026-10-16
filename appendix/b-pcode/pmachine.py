"""
The P-machine of Niklaus Wirth's PL/0 compiler (1976), ancestor of the
p-code of Pascal-P and UCSD Pascal.

Eight instructions, each with a level l and an argument a:

    lit 0 a     push the number a
    opr 0 n     an operation: return, or arithmetic on the stack
    lod l a     push the variable at offset a, l levels out
    sto l a     pop into the variable at offset a, l levels out
    cal l a     call the procedure at a, declared l levels out
    int 0 a     make room for a words: the frame and the variables
    jmp 0 a     jump to a
    jpc 0 a     pop, and jump to a if it was zero

Every frame begins with three words: the static link (the frame of the
procedure this one is declared in), the dynamic link (the frame of the
caller), and the return address. "l levels out" means: follow the
static link l times. That is how a procedure nested in another reaches
the variables of the one around it.

The assembler writes "opr" with names (opr add) and leaves out the
level where it is always 0 (lit 5, jmp loop). "opr write", which pops
and prints, is ours: Wirth's PL/0 had no output.

    python3 pmachine.py [-t] program.p
"""

import sys

OPR = {"ret": 0, "neg": 1, "add": 2, "sub": 3, "mul": 4, "div": 5,
       "odd": 6, "eql": 8, "neq": 9, "lss": 10, "geq": 11, "gtr": 12,
       "leq": 13, "write": 14}

LEVELLED = ("lod", "sto", "cal")
PLAIN = ("lit", "int", "jmp", "jpc")
STACK_SIZE = 500


class Error(Exception):
    pass


def assemble(text):
    """Return the code as a list of (op, level, argument)."""
    code = []
    labels = {}
    lines = []
    for number, line in enumerate(text.splitlines(), 1):
        line = line.split(";")[0].strip()
        while line and line.split()[0].endswith(":"):
            label, line = line.split(":", 1)
            labels[label] = len(code)
            line = line.strip()
        if not line:
            continue
        words = line.replace(",", " ").split()
        op, operands = words[0], words[1:]
        if op == "opr":
            if len(operands) != 1 or operands[0] not in OPR:
                raise Error(f"line {number}: opr takes one of {', '.join(OPR)}")
            code.append(("opr", 0, OPR[operands[0]]))
        elif op in LEVELLED and len(operands) == 2:
            code.append((op, int(operands[0]), operands[1]))
        elif op in PLAIN and len(operands) == 1:
            code.append((op, 0, operands[0]))
        else:
            raise Error(f"line {number}: cannot read {line!r}")
        lines.append(number)
    for k, (op, level, argument) in enumerate(code):
        if isinstance(argument, int):
            continue
        if argument.lstrip("-").isdigit():
            argument = int(argument)
        elif argument in labels:
            argument = labels[argument]
        else:
            raise Error(f"line {lines[k]}: no label {argument!r}")
        code[k] = (op, level, argument)
    return code


def show(instruction):
    op, level, argument = instruction
    if op == "opr":
        argument = next(name for name, n in OPR.items() if n == argument)
    return f"{op} {level} {argument}"


def run(code, trace=False):
    s = [0] * STACK_SIZE
    t = -1              # the top of the stack
    b = 0               # the base of the current frame
    p = 0               # the next instruction

    def base(l):
        """The frame l levels out, along the static links."""
        frame = b
        for _ in range(l):
            frame = s[frame]
        return frame

    while True:
        if not 0 <= p < len(code):
            raise Error(f"no instruction at {p}")
        op, l, a = code[p]
        if trace:
            print(f"  {p:3}  {show(code[p]):12}  b={b:<3} {' '.join(map(str, s[:t + 1]))}")
        p += 1
        if op == "lit":
            t += 1
            s[t] = a
        elif op == "opr":
            if a == 0:                      # return
                t = b - 1
                p = s[t + 3]
                b = s[t + 2]
                if p == 0:
                    return
            elif a == 1:
                s[t] = -s[t]
            elif a == 6:
                s[t] = s[t] % 2
            elif a == 14:
                print(s[t])
                t -= 1
            else:
                t -= 1
                x, y = s[t], s[t + 1]
                if a == 5:
                    if y == 0:
                        raise Error(f"division by zero at {p - 1}")
                    q = abs(x) // abs(y)
                    s[t] = q if (x < 0) == (y < 0) else -q
                else:
                    s[t] = {2: x + y, 3: x - y, 4: x * y, 8: int(x == y),
                            9: int(x != y), 10: int(x < y), 11: int(x >= y),
                            12: int(x > y), 13: int(x <= y)}[a]
        elif op == "lod":
            t += 1
            s[t] = s[base(l) + a]
        elif op == "sto":
            s[base(l) + a] = s[t]
            t -= 1
        elif op == "cal":
            s[t + 1] = base(l)              # static link
            s[t + 2] = b                    # dynamic link
            s[t + 3] = p                    # return address
            b = t + 1
            p = a
        elif op == "int":
            t += a
            if t >= STACK_SIZE:
                raise Error("stack overflow")
        elif op == "jmp":
            p = a
        elif op == "jpc":
            if s[t] == 0:
                p = a
            t -= 1


def main(args):
    trace = "-t" in args
    args = [a for a in args if a != "-t"]
    if len(args) != 1:
        sys.exit("usage: pmachine.py [-t] program.p")
    try:
        with open(args[0]) as f:
            run(assemble(f.read()), trace)
    except Error as e:
        sys.exit(f"pmachine: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
