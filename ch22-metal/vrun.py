#!/usr/bin/env python3
"""
Run a .vm file on the CPU of cpu.v, in simulation, as if it were a
machine like the others: what the program prints goes to standard
output, a trap message to standard error, and the exit status is the
specification's. Then the conformance suite can test the hardware.

A damaged file is reported exactly as the machine reports it, before
any simulation starts.

    usage: vrun.py [-c] program.vm

-c prints the number of clock cycles the program took, on stderr.
"""

import os
import subprocess
import sys
import tempfile

import vmfile

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    args = sys.argv[1:]
    cycles = args[:1] == ["-c"]
    if cycles:
        args = args[1:]
    if len(args) != 1:
        sys.exit("usage: vrun.py [-c] program.vm")
    path = args[0]
    try:
        code = vmfile.read(path)
    except OSError:
        print(f"{path}: cannot open", file=sys.stderr)
        sys.exit(2)
    except vmfile.FormatError as e:
        print(f"{path}: {e}", file=sys.stderr)
        sys.exit(2)
    with tempfile.TemporaryDirectory() as work:
        hexfile = os.path.join(work, "program.hex")
        with open(hexfile, "w") as f:
            for word in code:
                f.write(f"{word & 0xffffffff:08x}\n")
        p = subprocess.run(["vvp", "-n", os.path.join(HERE, "sim"),
                            f"+program={hexfile}", f"+length={len(code)}"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.stdout.buffer.write(p.stdout)
    sys.stdout.buffer.flush()
    status = 3
    for line in p.stderr.decode("latin-1").splitlines():
        if line.startswith("status "):
            status = int(line.split()[1])
        elif line.startswith("cycles ") and not cycles:
            continue
        else:
            print(line, file=sys.stderr)
    sys.exit(status)


if __name__ == "__main__":
    main()
