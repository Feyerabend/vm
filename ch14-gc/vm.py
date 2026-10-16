#!/usr/bin/env python3
"""
The machine again, in Python, written from SPEC.md (version 3).

It is meant to behave exactly like vm.c: the same output, the same
traps with the same messages, the same exit status, and with -t the
same trace, line for line. The conformance suite checks that both do
what the specification says, and compare.py checks that their traces
agree step by step.

It is not a translation of vm.c. Where Python and C differ, it has
to work harder to get the specified answer. The clearest case is
division: Python's // rounds towards minus infinity, and the
specification, like C, rounds towards zero, so -7 // 2 is -4 in
Python and -7 / 2 is -3 here.

    usage: vm.py [-t] program.vm
"""

import sys

import isa
import vmfile

STACK_SIZE = 256
FRAMES = 256
MEMORY_SIZE = 4096
HEAP_SIZE = 65536       # counted as in vm.c: a block of n values takes n + 2
HEADER = 2


class Ref:
    """A reference to a block on the heap. Python reclaims a block by
    itself once nothing refers to it, so this machine needs no garbage
    collector of its own. But to run out of memory exactly where vm.c
    does, it counts heap space as vm.c does, and when the count says
    the heap is full, it counts again how much is still reachable:
    which is what vm.c's collectors would find."""

    def __init__(self, number, size):
        self.number = number
        self.values = [0] * size

    def __str__(self):
        return f"@{self.number}"


def is_ref(v):
    return isinstance(v, Ref)


def wrap(n):
    """Wrap an integer of any size into a signed 32-bit value."""
    return (n + 2**31) % 2**32 - 2**31


def divide(a, b):
    """The quotient rounded towards zero, as in C, before wrapping."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


class Trap(Exception):
    pass


class Halt(Exception):
    pass


class Machine:

    def __init__(self, code):
        self.code = code
        self.pc = 0
        self.stack = []
        self.frames = []        # (return address, caller's fp)
        self.fp = 0
        self.start = 0
        self.memory = [0] * MEMORY_SIZE
        self.heap_used = 0
        self.blocks_made = 0
        self.out = sys.stdout.buffer

    # The checked basic operations, as in vm.c.

    def push(self, v):
        if len(self.stack) == STACK_SIZE:
            raise Trap("stack overflow")
        self.stack.append(v)

    def pop(self):
        if len(self.stack) == self.fp:
            raise Trap("stack underflow")
        return self.stack.pop()

    def operand(self):
        if self.pc >= len(self.code):
            raise Trap("missing operand")
        v = self.code[self.pc]
        self.pc += 1
        return v

    def address(self):
        addr = self.operand()
        if not 0 <= addr < len(self.code):
            raise Trap("jump out of program")
        return addr

    def local(self):
        k = self.operand()
        if k < 0 or self.fp + k >= len(self.stack):
            raise Trap("no such local")
        return self.fp + k

    def number(self, v):
        if is_ref(v):
            raise Trap("not a number")
        return v

    def block(self, v):
        if not is_ref(v):
            raise Trap("not a reference")
        return v

    def binary(self, f):
        b = self.pop()
        a = self.pop()
        a, b = self.number(a), self.number(b)
        self.push(wrap(f(a, b)))

    def reachable(self):
        """The places taken by every block reachable from the roots."""
        seen = set()
        todo = [v for v in self.stack + self.memory if is_ref(v)]
        total = 0
        while todo:
            r = todo.pop()
            if id(r) in seen:
                continue
            seen.add(id(r))
            total += HEADER + len(r.values)
            todo.extend(v for v in r.values if is_ref(v))
        return total

    def allocate(self, n):
        if n < 0:
            raise Trap("bad size")
        if n > HEAP_SIZE - HEADER - self.heap_used:
            self.heap_used = self.reachable()
            if n > HEAP_SIZE - HEADER - self.heap_used:
                raise Trap("out of memory")
        self.heap_used += HEADER + n
        self.blocks_made += 1
        return Ref(self.blocks_made, n)

    def field(self, r, i):
        if not 0 <= i < len(r.values):
            raise Trap("index out of bounds")
        return i

    def step(self):
        self.start = self.pc
        if not 0 <= self.pc < len(self.code):
            raise Trap("ran off the end of the program")
        op = self.code[self.pc]
        self.pc += 1
        name = isa.BY_CODE.get(op, ("?",))[0]

        if name == "HALT":
            raise Halt()
        elif name == "PUSH":
            self.push(self.operand())
        elif name == "ADD":
            self.binary(lambda a, b: a + b)
        elif name == "SUB":
            self.binary(lambda a, b: a - b)
        elif name == "MUL":
            self.binary(lambda a, b: a * b)
        elif name == "PRINT":
            self.out.write(b"%d\n" % self.number(self.pop()))
        elif name == "JMP":
            self.pc = self.address()
        elif name == "JZ":
            addr = self.address()
            if self.pop() == 0:         # a Ref is never equal to 0
                self.pc = addr
        elif name == "DUP":
            a = self.pop()
            self.push(a)
            self.push(a)
        elif name == "DROP":
            self.pop()
        elif name == "SWAP":
            b = self.pop()
            a = self.pop()
            self.push(b)
            self.push(a)
        elif name == "OVER":
            b = self.pop()
            a = self.pop()
            self.push(a)
            self.push(b)
            self.push(a)
        elif name == "ROT":
            c = self.pop()
            b = self.pop()
            a = self.pop()
            self.push(b)
            self.push(c)
            self.push(a)
        elif name == "LT":
            self.binary(lambda a, b: int(a < b))
        elif name == "EQ":
            b = self.pop()
            a = self.pop()
            if is_ref(a) or is_ref(b):
                self.push(int(a is b))
            else:
                self.push(int(a == b))
        elif name == "LOAD":
            self.push(self.stack[self.local()])
        elif name == "STORE":
            k = self.operand()
            v = self.pop()
            if k < 0 or self.fp + k >= len(self.stack):
                raise Trap("no such local")
            self.stack[self.fp + k] = v
        elif name == "CALL":
            addr = self.address()
            nargs = self.operand()
            if nargs < 0 or nargs > len(self.stack) - self.fp:
                raise Trap("not enough arguments")
            if len(self.frames) == FRAMES:
                raise Trap("too many nested calls")
            self.frames.append((self.pc, self.fp))
            self.fp = len(self.stack) - nargs
            self.pc = addr
        elif name == "RET":
            if not self.frames:
                raise Trap("return without call")
            v = self.pop()
            del self.stack[self.fp:]
            self.pc, self.fp = self.frames.pop()
            self.push(v)
        elif name in ("DIV", "MOD"):
            b = self.pop()
            a = self.pop()
            a, b = self.number(a), self.number(b)
            if b == 0:
                raise Trap("division by zero")
            q = divide(a, b)
            self.push(wrap(q if name == "DIV" else a - b * q))
        elif name == "AND":
            self.binary(lambda a, b: a & b)
        elif name == "OR":
            self.binary(lambda a, b: a | b)
        elif name == "XOR":
            self.binary(lambda a, b: a ^ b)
        elif name == "LOADM":
            a = self.number(self.pop())
            if not 0 <= a < MEMORY_SIZE:
                raise Trap("no such memory address")
            self.push(self.memory[a])
        elif name == "STOREM":
            v = self.pop()
            a = self.number(self.pop())
            if not 0 <= a < MEMORY_SIZE:
                raise Trap("no such memory address")
            self.memory[a] = v
        elif name == "EMIT":
            a = self.number(self.pop())
            if not 0 <= a <= 255:
                raise Trap("not a character")
            self.out.write(bytes([a]))
        elif name == "NEW":
            self.push(self.allocate(self.number(self.pop())))
        elif name == "GETF":
            i = self.pop()
            r = self.block(self.pop())
            self.push(r.values[self.field(r, self.number(i))])
        elif name == "SETF":
            v = self.pop()
            i = self.pop()
            r = self.block(self.pop())
            r.values[self.field(r, self.number(i))] = v
        elif name == "LEN":
            self.push(len(self.block(self.pop()).values))
        else:
            raise Trap("unknown instruction")

    # Tracing, in exactly the format of vm.c.

    def instruction(self, at):
        op = self.code[at]
        if op not in isa.BY_CODE:
            return f".word {op}"
        name, kinds = isa.BY_CODE[op]
        operands = self.code[at + 1:at + 1 + len(kinds)]
        return " ".join([name] + [str(v) for v in operands])

    def stack_text(self):
        starts = [fp for _, fp in self.frames[1:]] + ([self.fp] if self.frames else [])
        words = []
        for i in range(len(self.stack) + 1):
            words.extend("|" for s in starts if s == i)
            if i < len(self.stack):
                words.append(str(self.stack[i]))
        return " ".join(words)

    def trace_line(self, n, at):
        text = self.instruction(at)
        line = f"{n:6d} {at:5d}  {text}"
        if self.stack or self.frames:
            line += " " * max(14 - len(text), 0) + "  " + self.stack_text()
        return line


def run(machine, tracing):
    n = 0
    try:
        while True:
            at = machine.pc
            try:
                machine.step()
            except Halt:
                if tracing:
                    n += 1
                    machine.out.flush()
                    print(machine.trace_line(n, at), file=sys.stderr)
                machine.out.flush()
                return 0
            if tracing:
                n += 1
                machine.out.flush()
                print(machine.trace_line(n, at), file=sys.stderr)
    except Trap as trap:
        machine.out.flush()
        print(f"trap: {trap} at {machine.start}", file=sys.stderr)
        return 1


def main():
    args = sys.argv[1:]
    tracing = args[:1] == ["-t"]
    if tracing:
        args = args[1:]
    if len(args) != 1:
        print("usage: vm.py [-t] program.vm", file=sys.stderr)
        return 2
    path = args[0]
    try:
        code = vmfile.read(path)
    except OSError:
        print(f"{path}: cannot open", file=sys.stderr)
        return 2
    except vmfile.FormatError as e:
        print(f"{path}: {e}", file=sys.stderr)
        return 2
    return run(Machine(code), tracing)


if __name__ == "__main__":
    sys.exit(main())
