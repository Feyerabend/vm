#!/usr/bin/env python3
"""
Run two implementations of the machine side by side, tracing, and
report the first step where they part ways.

    usage: compare.py "COMMAND A" "COMMAND B" program.vm...

    compare.py ./vm "python3 vm.py" build/*.vm samples/*.vm

The conformance suite only looks at what a program prints and how it
ends. Two machines can agree on all of that and still have taken
different paths to get there. Comparing traces catches that: every
step, every stack, must be the same. Testing one implementation
against another like this is called differential testing.
"""

import shlex
import subprocess
import sys


def trace(command, program):
    p = subprocess.run(shlex.split(command) + ["-t", program],
                       capture_output=True, text=True)
    return p.stdout, p.returncode, p.stderr.splitlines()


def first_difference(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b)) if len(a) != len(b) else None


def main():
    if len(sys.argv) < 4:
        sys.exit('usage: compare.py "COMMAND A" "COMMAND B" program.vm...')
    a, b, programs = sys.argv[1], sys.argv[2], sys.argv[3:]
    differing = 0
    for program in programs:
        out_a, status_a, lines_a = trace(a, program)
        out_b, status_b, lines_b = trace(b, program)
        i = first_difference(lines_a, lines_b)
        if i is None and out_a == out_b and status_a == status_b:
            continue
        differing += 1
        print(f"{program}: the machines differ")
        if i is not None:
            print(f"  first different line, number {i + 1}:")
            print(f"  {a:>20}: {lines_a[i] if i < len(lines_a) else '(nothing)'}")
            print(f"  {b:>20}: {lines_b[i] if i < len(lines_b) else '(nothing)'}")
        if out_a != out_b:
            print("  the output differs")
        if status_a != status_b:
            print(f"  exit status {status_a} against {status_b}")
    print(f"{len(programs) - differing} of {len(programs)} programs traced identically")
    sys.exit(1 if differing else 0)


if __name__ == "__main__":
    main()
