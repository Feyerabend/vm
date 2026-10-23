"""
The P4 machine: the p-code of Pascal-P4 (Zurich, 1976), the last of
the portable Pascal-P compilers. UCSD Pascal grew from the one before
it, P2.

Where the PL/0 machine of pmachine.py has eight instructions, P4 has
sixty-odd, because Pascal has types. An instruction has a name, often a
type letter after it, and up to two numbers p and q:

    lodi 0 5    push the integer at offset 5, 0 levels out
    ldci 7      push the integer 7
    adi         add the two integers on top
    fjp l3      pop a boolean, and jump to label 3 if it was false

The type letters are i (integer), r (real), b (boolean), c (char),
s (set), a (address), and for comparisons m (a block of q words, such
as an array). Each word of the store holds one value of any type.

A frame begins with five words, made by mst before the arguments are
pushed:

    mp+0  the function's result
    mp+1  the static link: the frame this procedure is declared in
    mp+2  the dynamic link: the caller's frame
    mp+3  the caller's ep
    mp+4  the return address

then the arguments, then the local variables. The main program is a
procedure too, called from address 0. Its frame starts at 0, and its
variables have fixed addresses: 5 to 8 are the files input, output, prd
and prr, and the program's own variables follow. ldo, sro and lao reach
them without the static links.

The registers are pc, sp (the top of the stack), mp (the frame), ep
(the most the stack can grow in this frame, set by ent 2) and np (the
bottom of the heap, which new grows downwards).

The code is text, in the form the original P4 interpreter read it. A line that
starts with a space is an instruction, `l n` defines label n here, and
`l n=v` gives label n the value v. A line starting with i is a comment.
`q` ends a segment. The first segment is the program and is placed from
address 3; the second, at 0, calls it:

     mst 0
     cup 0 l3
     stp

This is our own implementation, written from the P4 interpreter's
description of what each instruction does. It traps where the original
left things to chance: an undefined value, a division by zero, a jump
into nowhere.

    python3 p4.py [-t] program.p4
"""

import math
import sys

MAXSTK = 13650          # the stack grows up from 0, the heap down from here
CONSTANTS = MAXSTK + 1  # string constants (lca) are kept above it
MAXSTR = 18001          # the top of the store; nil points here
STRING = 16             # P4's strings are 16 characters
BEGINCODE = 3
INPUT, OUTPUT, PRD, PRR = 5, 6, 7, 8
SETMAX = 58             # P4's sets hold 0 to 58

TYPES = {"i", "r", "b", "c", "s", "a"}
COMPARE = ("equ", "neq", "geq", "grt", "leq", "les")
SPECIAL = ("get", "put", "rst", "rln", "new", "wln", "wrs", "eln", "wri",
           "wrr", "wrc", "rdi", "rdr", "rdc", "sin", "cos", "exp", "log",
           "sqt", "atn", "sav")

# How each instruction is written: "t" a type letter, "p" and "q"
# numbers, "l" a label.
FORMS = {
    "lod": "tpq", "str": "tpq", "lda": "pq", "ldo": "tq", "sro": "tq",
    "lao": "q", "sto": "t", "ldc": "", "lca": "", "ind": "tq", "inc": "tq",
    "dec": "tq", "mst": "p", "cup": "pl", "ent": "pl", "ret": "",
    "csp": "", "ixa": "q", "ujp": "l", "fjp": "l", "xjp": "l", "ujc": "",
    "chk": "t", "eof": "", "mov": "q", "stp": "", "ord": "", "chr": "",
    "adi": "", "adr": "", "sbi": "", "sbr": "", "sgs": "", "flt": "",
    "flo": "", "trc": "", "ngi": "", "ngr": "", "sqi": "", "sqr": "",
    "abi": "", "abr": "", "not": "", "and": "", "ior": "", "dif": "",
    "int": "", "uni": "", "inn": "", "mod": "", "odd": "", "mpi": "",
    "mpr": "", "dvi": "", "dvr": "",
    **{c: "" for c in COMPARE},
}


class Error(Exception):
    pass


def numbers(text, line):
    try:
        return [int(w) for w in text.split()]
    except ValueError:
        raise Error(f"line {line}: expected numbers, found {text.strip()!r}")


def label_of(text, line):
    """The n of the first `l n` or `ln` in text."""
    at = text.find("l")
    if at < 0 or not text[at + 1:].strip().isdigit():
        raise Error(f"line {line}: expected a label, found {text.strip()!r}")
    return int(text[at + 1:])


def instruction(text, line, constants, address):
    """Read one instruction: (name, type, p, q, label)."""
    name, t, rest = text[:3], text[3:4], text[4:]
    if name not in FORMS:
        raise Error(f"line {line}: no instruction {name!r}")
    form = FORMS[name]
    if "t" not in form and name not in COMPARE + ("ldc", "lca", "ret"):
        t, rest = "", text[3:]
    p = q = label = None
    if "t" in form or name in COMPARE:
        if t not in TYPES and not (name in COMPARE and t == "m"):
            raise Error(f"line {line}: {name} needs a type, not {t!r}")
    if name == "ldc":
        if t == "i":
            q = numbers(rest, line)[0]
        elif t == "r":
            q = float(rest)
        elif t == "b":
            q = numbers(rest, line)[0] == 1
        elif t == "c":
            if "'" not in rest or len(rest) <= rest.index("'") + 1:
                raise Error(f"line {line}: ldcc needs a quoted character")
            q = rest[rest.index("'") + 1]
        elif t == "n":
            t, q = "a", MAXSTR
        elif t == "(":
            elements = numbers(rest.split(")")[0].replace(",", " "), line)
            t, q = "s", frozenset(elements)
        else:
            raise Error(f"line {line}: ldc of what? {text!r}")
    elif name == "lca":
        if t != "'":
            raise Error(f"line {line}: lca needs a quoted string")
        q = address
        for k, c in enumerate(rest[:STRING].ljust(STRING)):
            constants[address + k] = c
    elif name == "ret":
        if t not in "pirbca":
            raise Error(f"line {line}: ret needs p, i, r, b, c or a")
    elif name == "csp":
        q = rest.split()[-1] if rest.split() else ""
        if q not in SPECIAL:
            raise Error(f"line {line}: no standard procedure {q!r}")
    elif name in COMPARE:
        if t == "m":
            q = numbers(rest, line)[0]
    elif name == "chk":
        p, q = numbers(rest, line)[:2]          # the bounds
    else:
        args = rest
        if "p" in form and "q" in form:
            p, q = numbers(args, line)[:2]
        elif "p" in form:
            words = args.split()
            p = numbers(words[0] if words else "", line)[0]
            args = args[args.find(words[0]) + len(words[0]):] if words else ""
        elif "q" in form:
            q = numbers(args, line)[0]
        if "l" in form:
            label = label_of(args, line)
    return (name, t, p, q, label)


def assemble(text):
    """Return the code and the string constants: a list of instructions
    (name, type, p, q), and a dictionary of addresses and characters."""
    code, constants, labels, uses = {}, {}, {}, []
    segment, pc = 0, BEGINCODE
    next_constant = CONSTANTS
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line[0] == "i":
            continue
        if line[0] == "l":
            body = line[1:].replace(" ", "")
            n, _, value = body.partition("=")
            if not n.isdigit():
                raise Error(f"line {number}: cannot read {line!r}")
            if int(n) in labels:
                raise Error(f"line {number}: label {n} defined twice")
            labels[int(n)] = int(value) if value else pc
        elif line[0] == "q":
            segment += 1
            if segment == 2:
                break
            pc = 0
        elif line[0] == " ":
            if segment == 1 and pc >= BEGINCODE:
                raise Error(f"line {number}: the second segment has room for {BEGINCODE}")
            name, t, p, q, label = instruction(line[1:], number, constants, next_constant)
            if name == "lca":
                next_constant += STRING
            if label is not None:
                uses.append((pc, label, number))
            code[pc] = (name, t, p, q)
            pc += 1
        else:
            raise Error(f"line {number}: cannot read {line!r}")
    if segment < 2:
        raise Error("the code must end with two segments, each closed by q")
    for at, label, number in uses:
        if label not in labels:
            raise Error(f"line {number}: label {label} is never defined")
        name, t, p, _ = code[at]
        code[at] = (name, t, p, labels[label])
    return [code.get(k) for k in range(max(code) + 1)], constants


def show(instruction):
    name, t, p, q = instruction
    if name == "lca":
        return "lca'...'"
    if name == "ldc":
        args = repr(q) if t == "c" else str(int(q) if t == "b" else q)
    else:
        args = " ".join(str(x) for x in (p, q) if x is not None)
    return f"{name}{t} {args}".rstrip()


class Text:
    """The file input, read as Pascal reads it: one character at a time,
    with a look at the next (input^), and a line end seen as a blank."""

    def __init__(self, stream):
        self.stream = stream
        self.data = None
        self.at = 0

    def load(self):
        if self.data is None:
            self.data = self.stream.read()

    def eof(self):
        self.load()
        return self.at >= len(self.data)

    def eoln(self):
        if self.eof():
            raise Error("eoln at the end of input")
        return self.data[self.at] == "\n"

    def peek(self):
        if self.eof():
            return " "
        c = self.data[self.at]
        return " " if c == "\n" else c

    def get(self):
        if self.eof():
            raise Error("reading past the end of input")
        self.at += 1

    def read_char(self):
        c = self.peek()
        self.get()
        return c

    def read_number(self, kind):
        self.load()
        while not self.eof() and self.data[self.at] in " \t\n":
            self.at += 1
        start = self.at
        allowed = "+-0123456789" + (".eE" if kind is float else "")
        while not self.eof() and self.data[self.at] in allowed:
            self.at += 1
        try:
            return kind(self.data[start:self.at])
        except ValueError:
            raise Error(f"read: not a number: {self.data[start:self.at + 1]!r}")

    def readln(self):
        while not self.eof() and self.data[self.at] != "\n":
            self.at += 1
        if not self.eof():
            self.at += 1


def real(x, width):
    """A real, as Pascal writes it: in floating point, in width places."""
    digits = max(width - 7, 1)
    text = f"{x:.{digits}E}"
    return (text if x < 0 else " " + text).rjust(width)


def run(code, constants, trace=False, stdin=sys.stdin, out=sys.stdout):
    store = [None] * (MAXSTR + 1)
    for address, c in constants.items():
        store[address] = c
    pc, sp, mp, np, ep = 0, -1, 0, MAXSTK + 1, 5
    text = Text(stdin)
    store[INPUT] = " "

    def base(levels):
        """The frame levels out, along the static links."""
        frame = mp
        for _ in range(levels):
            frame = store[frame + 1]
        return frame

    def defined(x):
        if x is None:
            raise Error("an undefined value is used")
        return x

    def file(address, reading):
        if address == INPUT and reading or address == OUTPUT and not reading:
            return
        names = {INPUT: "input", OUTPUT: "output", PRD: "prd", PRR: "prr"}
        what = "read from" if reading else "write to"
        raise Error(f"cannot {what} {names.get(address, address)}")

    def special(name):
        nonlocal sp, np
        top = store[sp]
        if name in ("wri", "wrr", "wrc"):
            file(top, False)
            x, width = defined(store[sp - 2]), store[sp - 1]
            if name == "wri":
                out.write(str(x).rjust(width))
            elif name == "wrr":
                out.write(real(x, width))
            else:
                out.write(x.rjust(width))
            sp -= 3
        elif name == "wrs":
            file(top, False)
            address, width, length = store[sp - 3], store[sp - 2], store[sp - 1]
            if width > length:
                out.write(" " * (width - length))
            else:
                length = width
            out.write("".join(store[address + k] for k in range(length)))
            sp -= 4
        elif name == "wln":
            file(top, False)
            out.write("\n")
            sp -= 1
        elif name in ("rdi", "rdr", "rdc"):
            file(top, True)
            if name == "rdc":
                store[store[sp - 1]] = text.read_char()
            else:
                store[store[sp - 1]] = text.read_number(int if name == "rdi" else float)
            store[INPUT] = text.peek()
            sp -= 2
        elif name == "rln":
            file(top, True)
            text.readln()
            store[INPUT] = text.peek()
            sp -= 1
        elif name == "get":
            file(top, True)
            text.get()
            store[INPUT] = text.peek()
            sp -= 1
        elif name == "eln":
            file(top, True)
            store[sp] = text.eoln()
        elif name == "put":
            raise Error("put: output is written with write")
        elif name == "new":
            address = np - store[sp]
            if address <= ep:
                raise Error("the store is full: new")
            np = address
            store[store[sp - 1]] = np
            sp -= 2
        elif name == "sav":
            store[store[sp]] = np
            sp -= 1
        elif name == "rst":
            np = store[sp]
            sp -= 1
        else:
            f = {"sin": math.sin, "cos": math.cos, "exp": math.exp,
                 "log": math.log, "sqt": math.sqrt, "atn": math.atan}[name]
            try:
                store[sp] = f(defined(store[sp]))
            except ValueError:
                raise Error(f"{name} of {store[sp]}")

    def compare(name, t, q):
        nonlocal sp
        sp -= 1
        x, y = store[sp], store[sp + 1]
        if t == "m":
            # Two blocks of q words, compared word by word.
            k = 0
            while k < q and store[x + k] == store[y + k]:
                k += 1
            if k == q:
                x, y = 0, 0
            else:
                x, y = defined(store[x + k]), defined(store[y + k])
        elif t == "a" and name not in ("equ", "neq"):
            raise Error("addresses can only be compared for equality")
        elif t == "s" and name in ("grt", "les"):
            raise Error("sets have no < or >")
        if name not in ("equ", "neq"):
            defined(x), defined(y)
        store[sp] = {"equ": x == y, "neq": x != y, "geq": x >= y,
                     "grt": x > y, "leq": x <= y, "les": x < y}[name]

    def element(x):
        if not 0 <= defined(x) <= SETMAX:
            raise Error(f"{x} cannot be in a set (0 to {SETMAX})")
        return x

    while True:
        if not 0 <= pc < len(code) or code[pc] is None:
            raise Error(f"no instruction at {pc}")
        name, t, p, q = code[pc]
        if trace:
            stack = " ".join("?" if v is None else repr(v) if isinstance(v, str) else str(v)
                             for v in store[max(mp, 0):sp + 1])
            print(f"  {pc:4}  {show(code[pc]):14}  mp={mp:<4} {stack}", file=out)
        pc += 1
        try:
            if name == "lod":
                sp += 1
                store[sp] = store[base(p) + q]
            elif name == "ldo":
                sp += 1
                store[sp] = store[q]
            elif name == "str":
                store[base(p) + q] = store[sp]
                sp -= 1
            elif name == "sro":
                store[q] = store[sp]
                sp -= 1
            elif name == "lda":
                sp += 1
                store[sp] = base(p) + q
            elif name == "lao" or name == "lca":
                sp += 1
                store[sp] = q
            elif name == "sto":
                store[defined(store[sp - 1])] = store[sp]
                sp -= 2
            elif name == "ldc":
                sp += 1
                store[sp] = q
            elif name == "ind":
                store[sp] = store[defined(store[sp]) + q]
            elif name == "inc":
                store[sp] = defined(store[sp]) + q
            elif name == "dec":
                store[sp] = defined(store[sp]) - q
            elif name == "mst":
                store[sp + 2] = base(p)         # the static link
                store[sp + 3] = mp              # the dynamic link
                store[sp + 4] = ep
                sp += 5
            elif name == "cup":
                mp = sp - (p + 4)
                store[mp + 4] = pc
                pc = q
            elif name == "ent":
                if p == 1:                      # room for the variables
                    sp = mp + q
                else:                           # and for the stack above them
                    ep = sp + q
                if sp > np or ep > np:
                    raise Error("the store is full: the stack meets the heap")
            elif name == "ret":
                sp = mp - 1 if t == "p" else mp
                pc = store[mp + 4]
                ep = store[mp + 3]
                mp = store[mp + 2]
            elif name == "csp":
                special(q)
            elif name == "ixa":
                i = defined(store[sp])
                sp -= 1
                store[sp] = q * i + defined(store[sp])
            elif name in COMPARE:
                compare(name, t, q)
            elif name == "ujp":
                pc = q
            elif name == "fjp":
                if not defined(store[sp]):
                    pc = q
                sp -= 1
            elif name == "xjp":
                pc = defined(store[sp]) + q
                sp -= 1
            elif name == "ujc":
                raise Error("case: no label for this value")
            elif name == "chk":
                x = defined(store[sp])
                if t == "a":
                    if x < np or x > MAXSTR - p:
                        raise Error("a bad pointer: nil or not from new")
                elif not p <= x <= q:
                    raise Error(f"{x} is out of range {p}..{q}")
            elif name == "eof":
                if store[sp] != INPUT:
                    raise Error("eof: only on input")
                store[sp] = text.eof()
            elif name == "stp":
                return
            elif name in ("ord", "chr"):
                # Only the type changes, and words have none: but the
                # value does, here, where a char is a character.
                x = defined(store[sp])
                if name == "ord" and isinstance(x, str):
                    store[sp] = ord(x)
                elif name == "ord" and isinstance(x, bool):
                    store[sp] = int(x)
                elif name == "chr":
                    if not 0 <= x < 0x110000:
                        raise Error(f"chr({x})")
                    store[sp] = chr(x)
            elif name in ("not", "odd", "ngi", "ngr", "abi", "abr", "sqi",
                          "sqr", "flt", "trc", "sgs"):
                x = defined(store[sp])
                store[sp] = {
                    "not": lambda: not x, "odd": lambda: x % 2 == 1,
                    "ngi": lambda: -x, "ngr": lambda: -x,
                    "abi": lambda: abs(x), "abr": lambda: abs(x),
                    "sqi": lambda: x * x, "sqr": lambda: x * x,
                    "flt": lambda: float(x), "trc": lambda: int(x),
                    "sgs": lambda: frozenset([element(x)]),
                }[name]()
            elif name == "flo":
                store[sp - 1] = float(defined(store[sp - 1]))
            elif name == "inn":
                sp -= 1
                store[sp] = element(store[sp]) in defined(store[sp + 1])
            elif name == "mov":
                to, source = defined(store[sp - 1]), defined(store[sp])
                sp -= 2
                store[to:to + q] = store[source:source + q]
            else:
                sp -= 1
                x, y = defined(store[sp]), defined(store[sp + 1])
                if name == "dvi" and y == 0:
                    raise Error("division by zero")
                if name == "mod" and y <= 0:
                    raise Error(f"mod {y}: Pascal's mod needs a number above 0")
                if name == "dvr" and y == 0:
                    raise Error("division by zero")
                quotient = abs(x) // abs(y) if name in ("dvi", "mod") else 0
                if (x < 0) != (y < 0):
                    quotient = -quotient
                store[sp] = {
                    "adi": lambda: x + y, "adr": lambda: x + y,
                    "sbi": lambda: x - y, "sbr": lambda: x - y,
                    "mpi": lambda: x * y, "mpr": lambda: x * y,
                    # div rounds towards zero; mod is never negative.
                    "dvi": lambda: quotient, "mod": lambda: x % y,
                    "dvr": lambda: x / y,
                    "and": lambda: x and y, "ior": lambda: x or y,
                    "uni": lambda: x | y, "int": lambda: x & y,
                    "dif": lambda: x - y,
                }[name]()
        except IndexError:
            raise Error(f"an address outside the store, at {pc - 1}")
        except TypeError:
            raise Error(f"a value of the wrong type, at {pc - 1}")
        except Error as e:
            raise Error(f"{e}, at {pc - 1}")
        if sp > ep and name not in ("mst", "cup", "ent"):
            raise Error(f"the stack is deeper than ent allowed, at {pc - 1}")


def main(args):
    trace = "-t" in args
    args = [a for a in args if a != "-t"]
    if len(args) != 1:
        sys.exit("usage: p4.py [-t] program.p4")
    try:
        with open(args[0]) as f:
            code, constants = assemble(f.read())
        run(code, constants, trace)
    except Error as e:
        sys.stdout.flush()
        sys.exit(f"p4: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
