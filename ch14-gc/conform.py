#!/usr/bin/env python3
"""
Run the conformance suite against an implementation of the machine.

    usage: conform.py [--known NAME,...] COMMAND...

    conform.py ./vm
    conform.py python3 vm.py

Every program suite/NAME.asm is assembled and run, and what happens
is compared with suite/NAME.expect, which holds what SPEC.md says
must happen:

    <everything the program writes to standard output>
    status <exit status>
    <everything the machine writes to standard error>

The suite also runs the machine on program files that are broken in
every way section 7 of the specification lists, made by BROKEN below.
Their expected messages contain '<file>' where the path goes.
"""

import os
import struct
import subprocess
import sys

import asm
import vmfile

SUITE = "suite"
BUILD = "build"

GOOD = b"SVM\x01" + struct.pack("<i", 1) + struct.pack("<i", 0)

BROKEN = {
    "short": (b"SVM\x01\x01", "too short to be a program"),
    "magic": (b"ELF\x01" + GOOD[4:], "not a program (wrong magic number)"),
    "version": (b"SVM\x02" + GOOD[4:], "unknown format version"),
    "zero": (b"SVM\x01" + struct.pack("<i", 0), "bad code length"),
    "negative": (b"SVM\x01" + struct.pack("<i", -1), "bad code length"),
    "huge": (b"SVM\x01" + struct.pack("<i", 1 << 30), "bad code length"),
    "truncated": (b"SVM\x01" + struct.pack("<i", 2) + struct.pack("<i", 0), "code ends early"),
    "trailing": (GOOD + b"\x00", "extra bytes after the code"),
}


def build():
    """Assemble the suite and write the broken files. Returns the cases."""
    os.makedirs(BUILD, exist_ok=True)
    cases = []
    for entry in sorted(os.listdir(SUITE)):
        if not entry.endswith(".asm"):
            continue
        name = entry[:-4]
        source = os.path.join(SUITE, entry)
        with open(source) as f:
            assembler = asm.Assembler(source)
            _, code = assembler.assemble(f.read())
        if assembler.errors:
            sys.exit("\n".join(message for _, message in assembler.errors))
        program = os.path.join(BUILD, name + ".vm")
        vmfile.write(program, code)
        with open(os.path.join(SUITE, name + ".expect"), encoding="latin-1") as f:
            cases.append((name, program, f.read()))
    for name, (data, reason) in BROKEN.items():
        program = os.path.join(BUILD, "file-" + name + ".vm")
        with open(program, "wb") as f:
            f.write(data)
        cases.append(("file-" + name, program, f"status 2\n<file>: {reason}\n"))
    missing = os.path.join(BUILD, "no-such-file.vm")
    cases.append(("file-missing", missing, "status 2\n<file>: cannot open\n"))
    return cases


def run(command, program):
    # Output is compared as bytes, read one character per byte, since
    # EMIT can write bytes that are not valid text.
    p = subprocess.run(command + [program], capture_output=True)
    got = (p.stdout.decode("latin-1") + f"status {p.returncode}\n"
           + p.stderr.decode("latin-1"))
    return got.replace(program, "<file>")


def main():
    command = sys.argv[1:]
    # Tests that this machine is known to fail, and says so in its
    # documentation. They are still run, and reported, but do not make
    # the whole run fail; and if one of them passes, that is reported
    # too, since then the documentation is wrong.
    known = set()
    if command[:1] == ["--known"]:
        known = set(command[1].split(","))
        command = command[2:]
    if not command:
        sys.exit("usage: conform.py [--known NAME,...] COMMAND...")
    cases = build()
    failed = []
    for name, program, expected in cases:
        got = run(command, program)
        if got != expected:
            failed.append(name)
            print(f"FAIL {name}")
            print("  expected: " + ascii(expected))
            print("  got:      " + ascii(got))
    passed = len(cases) - len(failed)
    print(f"{' '.join(command)}: {passed} of {len(cases)} passed")
    unexpected = [name for name in failed if name not in known]
    fixed = [name for name in known if name not in failed]
    for name in sorted(known & set(failed)):
        print(f"  {name}: a known failure")
    for name in fixed:
        print(f"  {name}: was expected to fail, and passed")
    sys.exit(1 if unexpected or fixed else 0)


if __name__ == "__main__":
    main()
