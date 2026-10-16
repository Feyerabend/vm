#!/usr/bin/env python3
"""
A disassembler: turn a .vm file back into assembly language.

The names of labels are not in the file; only the addresses are. So
the disassembler makes up a name for every address that some jump or
call goes to: 'L12' for address 12. The result assembles back into
exactly the same file, which the tests check.

A word that is not an instruction the machine knows, or an
instruction cut off by the end of the code, is written as '.word', so
nothing is lost even then. The disassembler cannot tell code from
data; it reads every word as code if it can.

    usage: disasm.py program.vm
"""

import sys

import isa
import vmfile


def decode(code):
    """Split the code into (address, name, operands) triples."""
    out = []
    pc = 0
    while pc < len(code):
        entry = isa.BY_CODE.get(code[pc])
        if entry is None or pc + len(entry[1]) >= len(code):
            out.append((pc, ".word", [code[pc]]))
            pc += 1
            continue
        name, kinds = entry
        out.append((pc, name, list(zip(kinds, code[pc + 1:pc + 1 + len(kinds)]))))
        pc += 1 + len(kinds)
    return out


def targets(decoded, length):
    found = set()
    for _, name, operands in decoded:
        if name == ".word":
            continue
        for kind, value in operands:
            if kind == "addr" and 0 <= value < length:
                found.add(value)
    return found


def disassemble(code):
    decoded = decode(code)
    labels = targets(decoded, len(code))
    starts = {address for address, _, _ in decoded}
    lines = []
    for address, name, operands in decoded:
        label = f"L{address}:" if address in labels else ""
        if name == ".word":
            text = f".word {operands[0]}"
        else:
            words = []
            for kind, value in operands:
                if kind == "addr" and value in labels and value in starts:
                    words.append(f"L{value}")
                else:
                    words.append(str(value))
            text = " ".join([name] + words)
        lines.append(f"{label:<8}{text:<20}; {address}")
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: disasm.py program.vm")
    try:
        code = vmfile.read(sys.argv[1])
    except vmfile.FormatError as e:
        sys.exit(f"{sys.argv[1]}: {e}")
    sys.stdout.write(disassemble(code))


if __name__ == "__main__":
    main()
