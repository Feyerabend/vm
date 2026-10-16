#!/usr/bin/env python3
"""
A compiler for basal/0.

basal/0 is a small BASIC, in the spirit of Tiny BASIC: one statement
to a line, global variables that need no declaring, GOTO and GOSUB.

    LET A = 15
    LET B = 6
    WHILE A <> B DO
      IF B < A THEN
        LET A = A - B
      ELSE
        LET B = B - A
      ENDIF
    ENDWHILE
    PRINT A

It compiles to the same machine as enkel/0, and is built differently
on purpose. enkel.py builds a syntax tree and then walks it. This
compiler builds no tree at all: it writes the assembly for each piece
of the program the moment it has recognised it. That is called
syntax-directed translation, and it is how most compilers worked when
memory was too small to hold a tree.

There are three stages:

    scan       text     -> tokens               basal.py -tokens prog.bas
    desugar    tokens   -> simpler tokens       basal.py -desugar prog.bas
    translate  tokens   -> assembly             basal.py prog.bas

Desugaring rewrites the statements that are only convenient ways of
writing other statements. FOR ... NEXT becomes LET and WHILE, and ON
... GOTO becomes a row of IFs, before the translator ever sees them.
The translator does not know FOR exists.

    usage: basal.py [-tokens | -desugar] program.bas
"""

import sys


class CompileError(Exception):

    def __init__(self, message, token):
        super().__init__(message)
        self.line = token.line
        self.col = token.col


# Stage 1: scanning.
#
# Keywords are written in capitals. Names of variables and labels are
# letters and digits, and are told apart by case: A and a are two
# variables. A line ends a statement, so the end of a line is a token.

KEYWORDS = {
    "LET", "PRINT", "IF", "THEN", "ELSE", "ENDIF", "WHILE", "DO",
    "ENDWHILE", "GOTO", "GOSUB", "RETURN", "END", "FOR", "TO", "STEP",
    "NEXT", "ON",
}

SYMBOLS = ["<>", "<=", ">=", "=", "<", ">", "+", "-", "*", "/", "(", ")",
           ";", ",", "!"]


class Token:

    def __init__(self, kind, text, line, col):
        self.kind = kind        # "name", "number", "string", "newline", a keyword or symbol
        self.text = text
        self.line = line
        self.col = col

    def __repr__(self):
        text = "\\n" if self.kind == "newline" else self.text
        return f"{self.line}:{self.col}  {self.kind:<9} {text!r}"


def scan(text):
    tokens = []
    for line_no, line in enumerate(text.splitlines(), 1):
        i = 0
        while i < len(line):
            c = line[i]
            col = i + 1
            if c.isspace():
                i += 1
            elif c == "#":
                break
            elif c == '"':
                end = line.find('"', i + 1)
                if end < 0:
                    raise CompileError("string is never closed", Token(c, c, line_no, col))
                tokens.append(Token("string", line[i + 1:end], line_no, col))
                i = end + 1
            elif c.isalpha():
                start = i
                while i < len(line) and (line[i].isalnum() or line[i] == "_"):
                    i += 1
                word = line[start:i]
                tokens.append(Token(word if word in KEYWORDS else "name", word, line_no, col))
            elif c.isdigit():
                start = i
                while i < len(line) and line[i].isdigit():
                    i += 1
                tokens.append(Token("number", line[start:i], line_no, col))
            else:
                for symbol in SYMBOLS:
                    if line.startswith(symbol, i):
                        tokens.append(Token(symbol, symbol, line_no, col))
                        i += len(symbol)
                        break
                else:
                    raise CompileError(f"unexpected character {c!r}", Token(c, c, line_no, col))
        tokens.append(Token("newline", "\n", line_no, len(line) + 1))
    last = len(text.splitlines()) + 1
    tokens.append(Token("end of file", "", last, 1))
    return tokens


# Stage 2: desugaring.
#
#     FOR I = a TO b STEP s         LET I = a
#       ...                 ==>     WHILE I <= b DO      (>= if s < 0)
#     NEXT I                          ...
#                                     LET I = I + s
#                                   ENDWHILE
#
#     ON K GOTO L1, L2, L3  ==>     IF K = 1 THEN
#                                   GOTO L1
#                                   ENDIF
#                                   IF K = 2 THEN ... (and so on)
#
# The rewriting works on tokens, not on text, and the new tokens carry
# the line and column of the tokens they replace, so that an error in
# a FOR loop is still reported where the FOR is.

def statement_lines(tokens):
    """Split the tokens into lines, each a list of tokens without the newline."""
    lines, current = [], []
    for token in tokens:
        if token.kind == "newline":
            lines.append((current, token))
            current = []
        elif token.kind == "end of file":
            if current:
                lines.append((current, token))
            return lines, token
        else:
            current.append(token)
    return lines, tokens[-1]


def make(kind, at, text=None):
    return Token(kind, kind if text is None else text, at.line, at.col)


def desugar(tokens):
    lines, eof = statement_lines(tokens)
    out = []
    loops = []      # open FOR loops: (variable token, step tokens, FOR token)
    for words, newline in lines:
        if words and words[0].kind == "FOR":
            out += desugar_for(words, newline, loops)
        elif words and words[0].kind == "NEXT":
            out += desugar_next(words, newline, loops)
        elif words and words[0].kind == "ON":
            out += desugar_on(words, newline)
        else:
            out += words + [newline]
    if loops:
        raise CompileError("FOR without NEXT", loops[-1][2])
    return out + [eof]


def desugar_for(words, newline, loops):
    # FOR name = start TO limit [STEP [-] number]
    f = words[0]
    if len(words) < 6 or words[1].kind != "name" or words[2].kind != "=":
        raise CompileError("expected FOR name = start TO limit", f)
    to = next((i for i, w in enumerate(words) if w.kind == "TO"), None)
    if to is None:
        raise CompileError("FOR needs TO", f)
    step_at = next((i for i, w in enumerate(words) if w.kind == "STEP"), len(words))
    start, limit, step = words[3:to], words[to + 1:step_at], words[step_at + 1:]
    if not start or not limit:
        raise CompileError("expected FOR name = start TO limit", f)
    if step_at == len(words):
        step = [make("number", f, "1")]
    sign = -1 if step and step[0].kind == "-" else 1
    if not (len(step) == 1 + (sign < 0) and step[-1].kind == "number"):
        raise CompileError("STEP must be a number, such as 2 or -1", words[step_at])
    if int(step[-1].text) == 0:
        raise CompileError("STEP cannot be 0", step[-1])
    var = words[1]
    loops.append((var, step, f))
    compare = make("<=" if sign > 0 else ">=", f)
    return ([make("LET", f), var, make("=", f)] + start + [newline] +
            [make("WHILE", f), var, compare] + limit + [make("DO", f), newline])


def desugar_next(words, newline, loops):
    n = words[0]
    if not loops:
        raise CompileError("NEXT without FOR", n)
    var, step, _ = loops.pop()
    if len(words) != 2 or words[1].kind != "name" or words[1].text != var.text:
        raise CompileError(f"expected NEXT {var.text}", n)
    plus = make("+", n)
    return ([make("LET", n), var, make("=", n), var, plus] + step + [newline] +
            [make("ENDWHILE", n), newline])


def desugar_on(words, newline):
    # ON expression GOTO label, label, ...   (or GOSUB)
    on = words[0]
    jump = next((i for i, w in enumerate(words) if w.kind in ("GOTO", "GOSUB")), None)
    if jump is None or jump == 1:
        raise CompileError("expected ON expression GOTO label, ...", on)
    value, targets = words[1:jump], words[jump + 1:]
    labels = targets[0::2]
    commas = targets[1::2]
    if not labels or any(t.kind != "name" for t in labels) or any(c.kind != "," for c in commas):
        raise CompileError("expected labels separated by commas", words[jump])
    out = []
    for k, label in enumerate(labels, 1):
        out += ([make("IF", on), make("(", on)] + value + [make(")", on), make("=", on),
                make("number", on, str(k)), make("THEN", on), newline,
                words[jump], label, newline,
                make("ENDIF", on), newline])
    return out


# Stage 3: translating.
#
# A recursive descent parser, as in the other compilers, but each
# function writes assembly as it goes instead of returning a tree.
# Compare translate_expression below with the tree-building parser
# and the separate code generator of chapter 9: the same post-order,
# folded into the parser.

class Translator:

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.out = []
        self.variables = {}         # name -> memory address
        self.labels_defined = {}
        self.labels_used = []
        self.count = 0
        self.needs_print = False

    def peek(self):
        return self.tokens[self.i]

    def at(self, *kinds):
        return self.peek().kind in kinds

    def take(self, kind):
        token = self.peek()
        if token.kind != kind:
            what = {"name": "a name", "number": "a number", "newline": "the end of the line"}
            found = {"newline": "the end of the line", "end of file": "the end of the file"}
            raise CompileError(f"expected {what.get(kind, repr(kind))}, "
                               f"found {found.get(token.kind, repr(token.text))}", token)
        self.i += 1
        return token

    def emit(self, instruction):
        self.out.append(f"        {instruction}")

    def label(self, name):
        self.out.append(f"{name}:")

    def new_label(self):
        self.count += 1
        return f"L{self.count}"

    def address(self, name):
        # A variable exists from the first time it is mentioned.
        if name not in self.variables:
            self.variables[name] = len(self.variables)
            if len(self.variables) > 4096:
                raise CompileError("too many variables", self.peek())
        return self.variables[name]

    def program(self):
        self.statements(until=("end of file",))
        self.emit("HALT")
        for name, token in self.labels_used:
            if name not in self.labels_defined:
                raise CompileError(f"there is no label '{name}'", token)
        if self.needs_print:
            self.out += PRINT_ROUTINE
        return "\n".join(self.out) + "\n"

    def statements(self, until):
        while not self.at(*until):
            if self.at("newline"):
                self.take("newline")
                continue
            self.statement()

    def statement(self):
        token = self.peek()
        self.out.append(f"; {token.line}")
        kind = token.kind
        if kind == "!":
            self.take("!")
            name = self.take("name")
            if name.text in self.labels_defined:
                raise CompileError(f"label '{name.text}' is defined twice", name)
            self.labels_defined[name.text] = name
            self.label("u_" + name.text)
        elif kind == "LET":
            self.take("LET")
            name = self.take("name")
            self.take("=")
            self.emit(f"PUSH {self.address(name.text)}")
            self.expression()
            self.emit("STOREM")
        elif kind == "PRINT":
            self.print_statement()
        elif kind == "IF":
            self.take("IF")
            self.condition()
            self.take("THEN")
            self.take("newline")
            otherwise, done = self.new_label(), self.new_label()
            self.emit(f"JZ {otherwise}")
            self.statements(until=("ELSE", "ENDIF", "end of file"))
            if self.at("ELSE"):
                self.take("ELSE")
                self.emit(f"JMP {done}")
                self.label(otherwise)
                self.statements(until=("ENDIF", "end of file"))
                self.take("ENDIF")
                self.label(done)
            else:
                self.take("ENDIF")
                self.label(otherwise)
        elif kind == "WHILE":
            self.take("WHILE")
            top, done = self.new_label(), self.new_label()
            self.label(top)
            self.condition()
            self.take("DO")
            self.take("newline")
            self.emit(f"JZ {done}")
            self.statements(until=("ENDWHILE", "end of file"))
            self.take("ENDWHILE")
            self.emit(f"JMP {top}")
            self.label(done)
        elif kind in ("GOTO", "GOSUB"):
            self.take(kind)
            name = self.take("name")
            self.labels_used.append((name.text, name))
            if kind == "GOTO":
                self.emit(f"JMP u_{name.text}")
            else:
                self.emit(f"CALL u_{name.text} 0")
                self.emit("DROP")
        elif kind == "RETURN":
            self.take("RETURN")
            self.emit("PUSH 0")
            self.emit("RET")
        elif kind == "END":
            self.take("END")
            self.emit("HALT")
        else:
            raise CompileError(f"expected a statement, found {token.text!r}", token)
        if not self.at("end of file"):
            self.take("newline")

    def print_statement(self):
        # PRINT "text"[;]   or   PRINT expression[;]   or   PRINT
        # A ';' at the end means: stay on this line.
        self.take("PRINT")
        if self.at("newline", "end of file"):
            self.emit("PUSH 10")
            self.emit("EMIT")
            return
        if self.at("string"):
            for c in self.take("string").text.encode("latin-1", "replace"):
                self.emit(f"PUSH {c}")
                self.emit("EMIT")
            stay = self.at(";")
        else:
            self.expression()
            stay = self.at(";")
            if stay:
                self.needs_print = True
                self.emit("CALL print_number 1")
                self.emit("DROP")
            else:
                self.emit("PRINT")
                return
        if stay:
            self.take(";")
        else:
            self.emit("PUSH 10")
            self.emit("EMIT")

    # condition = expression ("=" | "<>" | "<" | "<=" | ">" | ">=") expression .
    def condition(self):
        self.expression()
        token = self.peek()
        if token.kind not in COMPARISONS:
            raise CompileError(f"expected a comparison such as = or <, found {token.text!r}", token)
        self.take(token.kind)
        self.expression()
        for instruction in COMPARISONS[token.kind]:
            self.emit(instruction)

    # expression = term { ("+" | "-") term } .
    def expression(self):
        self.term()
        while self.at("+", "-"):
            op = self.take(self.peek().kind).kind
            self.term()
            self.emit("ADD" if op == "+" else "SUB")

    # term = factor { ("*" | "/") factor } .
    def term(self):
        self.factor()
        while self.at("*", "/"):
            op = self.take(self.peek().kind).kind
            self.factor()
            self.emit("MUL" if op == "*" else "DIV")

    # factor = name | number | "(" expression ")" | ("-" | "+") factor .
    def factor(self):
        token = self.peek()
        if self.at("name"):
            self.take("name")
            self.emit(f"PUSH {self.address(token.text)}")
            self.emit("LOADM")
        elif self.at("number"):
            self.take("number")
            if int(token.text) > 2**31 - 1:
                raise CompileError(f"number too large: {token.text}", token)
            self.emit(f"PUSH {token.text}")
        elif self.at("("):
            self.take("(")
            self.expression()
            self.take(")")
        elif self.at("-"):
            self.take("-")
            self.emit("PUSH 0")
            self.factor()
            self.emit("SUB")
        elif self.at("+"):
            self.take("+")
            self.factor()
        else:
            raise CompileError(f"expected a value, found {token.text!r}", token)


COMPARISONS = {
    "=": ["EQ"],
    "<>": ["EQ", "PUSH 0", "EQ"],
    "<": ["LT"],
    ">": ["SWAP", "LT"],
    "<=": ["SWAP", "LT", "PUSH 0", "EQ"],
    ">=": ["LT", "PUSH 0", "EQ"],
}


# The run-time library: code that the compiler adds to a program when
# the program needs it. The machine's PRINT always ends the line, so
# PRINT X; needs a way to print a number without one. This routine
# prints its argument digit by digit with EMIT.
#
# It works with the number made negative, never positive, because
# every 32-bit number can be negated into a negative one, but
# -2147483648 cannot be negated into a positive one.

PRINT_ROUTINE = """
; run-time library: print_number(n) prints n with no newline
print_number:
        LOAD 0
        PUSH 0
        LT
        JZ print_negate
        PUSH 45                 ; '-'
        EMIT
        LOAD 0                  ; n is already negative
        JMP print_digits_of
print_negate:
        PUSH 0
        LOAD 0
        SUB                     ; -n
print_digits_of:
        CALL print_digits 1
        RET

; print_digits(m), for m <= 0, prints the digits of -m
print_digits:
        LOAD 0
        PUSH -9
        LT                      ; m < -9: more than one digit
        JZ print_last
        LOAD 0
        PUSH 10
        DIV
        CALL print_digits 1     ; all digits but the last
        DROP
print_last:
        PUSH 48                 ; '0'
        PUSH 0
        LOAD 0
        PUSH 10
        MOD
        SUB                     ; -(m mod 10), from 0 to 9
        ADD
        EMIT
        PUSH 0
        RET""".splitlines()


def report(path, text, error):
    lines = text.splitlines()
    source = lines[error.line - 1] if 0 < error.line <= len(lines) else ""
    print(f"{path}:{error.line}:{error.col}: {error}", file=sys.stderr)
    print(f"    {source}", file=sys.stderr)
    print(f"    {' ' * (error.col - 1)}^", file=sys.stderr)


def main():
    args = sys.argv[1:]
    mode = args.pop(0) if args and args[0] in ("-tokens", "-desugar") else None
    if len(args) != 1:
        sys.exit("usage: basal.py [-tokens | -desugar] program.bas")
    path = args[0]
    with open(path) as f:
        text = f.read()
    try:
        tokens = scan(text)
        if mode == "-tokens":
            for token in tokens:
                print(token)
            return
        tokens = desugar(tokens)
        if mode == "-desugar":
            print(unscan(tokens), end="")
            return
        sys.stdout.write(Translator(tokens).program())
    except CompileError as error:
        report(path, text, error)
        sys.exit(1)


def unscan(tokens):
    """Write tokens back out as program text, to show what desugaring did."""
    out, line = [], []
    for token in tokens:
        if token.kind == "newline":
            out.append(" ".join(line))
            line = []
        elif token.kind == "string":
            line.append(f'"{token.text}"')
        elif token.kind == "!":
            line.append("!")
        elif token.kind != "end of file":
            line.append(token.text)
    if line:
        out.append(" ".join(line))
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    main()
