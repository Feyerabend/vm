#!/usr/bin/env python3
"""
An assembler for the machine.

Assembly language is the instruction listing of chapter 5 with three
additions that make it fit for people:

  * labels: 'loop:' names the address of whatever follows it, and a
    jump can then say 'JMP loop' instead of 'JMP 6';
  * checks: every instruction gets exactly the operands it needs, of
    the right kind, and every label used is defined exactly once;
  * '.word n' puts the number n into the program as it is.

One instruction per line. A line may start with any number of labels.
Everything from '#' or ';' to the end of a line is a comment.

    loop:   DUP
            JZ end          ; leave when the counter reaches zero
            ...
            JMP loop
    end:    HALT

The assembler reads the source twice. The first pass only counts:
it works out the address of every instruction, and so of every
label. The second pass writes the code, and by then every label has
a known address, even the ones defined further down. This is the
classic two-pass assembler.

    usage: asm.py [-l] program.asm program.vm

With -l, a listing showing each address, the words written there and
the source line they came from is printed on standard output.
"""

import re
import sys

import isa
import vmfile

LABEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")
NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class Line:
    """One line of source, taken apart."""

    def __init__(self, number, text, labels, op, operands):
        self.number = number
        self.text = text
        self.labels = labels
        self.op = op            # an instruction name, '.word', or None
        self.operands = operands
        self.address = None


def parse_line(number, text):
    rest = re.split(r"[#;]", text, maxsplit=1)[0].strip()
    labels = []
    while True:
        m = LABEL.match(rest)
        if not m:
            break
        labels.append(m.group(1))
        rest = rest[m.end():].strip()
    words = rest.split()
    if not words:
        return Line(number, text, labels, None, [])
    return Line(number, text, labels, words[0], words[1:])


def size(line):
    if line.op is None:
        return 0
    if line.op.lower() == ".word":
        return 1
    entry = isa.BY_NAME.get(line.op.upper())
    if entry is None:
        return 1        # an error, reported in pass 2; count it as one word
    return 1 + len(entry[1])


def number(word):
    """The value of a number written in decimal or hex (0x1f), else None."""
    try:
        return int(word, 0)
    except ValueError:
        return None


class Assembler:

    def __init__(self, path):
        self.path = path
        self.errors = []
        self.labels = {}

    def error(self, line, message):
        self.errors.append((line.number, f"{self.path}:{line.number}: {message}"))

    def pass1(self, lines):
        address = 0
        for line in lines:
            for label in line.labels:
                if label in self.labels:
                    self.error(line, f"label '{label}' is defined twice")
                else:
                    self.labels[label] = address
            line.address = address
            address += size(line)

    def operand(self, line, kind, word):
        n = number(word)
        if kind == "addr" and n is None and NAME.match(word):
            if word not in self.labels:
                self.error(line, f"undefined label '{word}'")
                return 0
            return self.labels[word]
        if n is None:
            self.error(line, f"expected a number, found '{word}'")
            return 0
        if not -2**31 <= n < 2**31:
            self.error(line, f"number out of range: {word}")
            return 0
        if kind == "k" and n < 0:
            self.error(line, f"a local number cannot be negative: {n}")
        return n

    def pass2(self, lines):
        code = []
        for line in lines:
            if line.op is None:
                continue
            if line.op.lower() == ".word":
                if len(line.operands) != 1:
                    self.error(line, ".word takes one number")
                    code.append(0)
                else:
                    code.append(self.operand(line, "n", line.operands[0]))
                continue
            entry = isa.BY_NAME.get(line.op.upper())
            if entry is None:
                self.error(line, f"unknown instruction '{line.op}'")
                code.append(0)
                continue
            op, kinds = entry
            if len(line.operands) != len(kinds):
                self.error(line, f"{line.op.upper()} takes {len(kinds)} "
                                 f"operand{'' if len(kinds) == 1 else 's'}, "
                                 f"found {len(line.operands)}")
                code.extend([op] + [0] * len(kinds))
                continue
            code.append(op)
            for kind, word in zip(kinds, line.operands):
                code.append(self.operand(line, kind, word))
        return code

    def assemble(self, text):
        lines = [parse_line(i, t) for i, t in enumerate(text.splitlines(), 1)]
        self.pass1(lines)
        code = self.pass2(lines)
        if not code and not self.errors:
            self.errors.append((0, f"{self.path}: no code"))
        self.errors.sort(key=lambda e: e[0])
        return lines, code


def listing(lines, code):
    for line in lines:
        words = code[line.address:line.address + size(line)]
        cells = " ".join(f"{w:d}" for w in words)
        where = f"{line.address:5d}" if words else "     "
        print(f"{where}  {cells:<16} {line.text}")


def main():
    args = sys.argv[1:]
    show = args[:1] == ["-l"]
    if show:
        args = args[1:]
    if len(args) != 2:
        sys.exit("usage: asm.py [-l] program.asm program.vm")
    source, target = args
    with open(source) as f:
        text = f.read()
    asm = Assembler(source)
    lines, code = asm.assemble(text)
    if asm.errors:
        sys.exit("\n".join(message for _, message in asm.errors))
    vmfile.write(target, code)
    if show:
        listing(lines, code)


if __name__ == "__main__":
    main()
