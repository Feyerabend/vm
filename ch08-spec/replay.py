#!/usr/bin/env python3
"""
Replay a saved trace, forwards and backwards.

A trace written by 'vm -t' records the state of the machine after
every step. Saved to a file, it can be explored after the run is
over, and, unlike the debugger, in either direction: when a wrong
value turns up, you can step back to see where it came from.

    ./vm -t program.vm 2> trace.txt
    python3 replay.py trace.txt

Commands, one per line:

    n [k]       next step, or k steps forward
    p [k]       previous step, or k steps back
    g k         go to step k
    f addr      find the next step at address addr
    b addr      find the previous step at address addr
    v value     find the next step where value is on top of the stack
    w           show a few steps around the current one
    q           quit

    usage: replay.py trace.txt
"""

import sys

import isa


class Step:
    """One line of a trace: step, address, instruction, stack."""

    def __init__(self, line):
        self.line = line.rstrip("\n")
        fields = self.line.split()
        self.number = int(fields[0])
        self.address = int(fields[1])
        name = fields[2]
        operands = 1 if name == ".word" else len(isa.BY_NAME[name][1])
        stack = fields[3 + operands:]
        values = [int(w) for w in stack if w != "|"]
        self.top = values[-1] if values else None


def read(path):
    steps = []
    with open(path) as f:
        for line in f:
            fields = line.split()
            if len(fields) >= 3 and fields[0].isdigit():
                steps.append(Step(line))
    return steps


def show(steps, i):
    print(steps[i].line)


def search(steps, i, direction, test):
    j = i + direction
    while 0 <= j < len(steps):
        if test(steps[j]):
            return j
        j += direction
    print("not found")
    return i


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: replay.py trace.txt")
    steps = read(sys.argv[1])
    if not steps:
        sys.exit(f"{sys.argv[1]}: no steps in the trace")
    i = 0
    show(steps, i)
    while True:
        try:
            words = input("(replay) ").split()
        except EOFError:
            print()
            break
        if not words:
            continue
        cmd, args = words[0], words[1:]
        try:
            n = int(args[0]) if args else None
        except ValueError:
            print(f"not a number: {args[0]}")
            continue
        if cmd == "q":
            break
        elif cmd == "n":
            i = min(i + (n or 1), len(steps) - 1)
        elif cmd == "p":
            i = max(i - (n or 1), 0)
        elif cmd == "g" and n is not None:
            i = min(max(n - 1, 0), len(steps) - 1)
        elif cmd == "f" and n is not None:
            i = search(steps, i, +1, lambda s: s.address == n)
        elif cmd == "b" and n is not None:
            i = search(steps, i, -1, lambda s: s.address == n)
        elif cmd == "v" and n is not None:
            i = search(steps, i, +1, lambda s: s.top == n)
        elif cmd == "w":
            for j in range(max(i - 3, 0), min(i + 4, len(steps))):
                print(("> " if j == i else "  ") + steps[j].line)
            continue
        else:
            print("commands: n [k], p [k], g k, f addr, b addr, v value, w, q")
            continue
        show(steps, i)


if __name__ == "__main__":
    main()
