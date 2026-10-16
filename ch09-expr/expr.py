#!/usr/bin/env python3
"""
A compiler for arithmetic expressions.

The language is as small as a language can usefully be: a program
is a list of expressions, each ended by a semicolon, and running the
program prints the value of each one.

    (2 + 3) * 7 - 5;
    -17 % 5;

The grammar, in EBNF:

    program    = { expression ";" } .
    expression = term { ("+" | "-") term } .
    term       = unary { ("*" | "/" | "%") unary } .
    unary      = "-" unary | factor .
    factor     = number | "(" expression ")" .

Comments run from '#' to the end of a line.

The compiler works in three stages, each a separate piece of code
with a separate job, and each can be watched on its own:

    scan       text    -> tokens          expr.py -tokens prog.expr
    parse      tokens  -> syntax tree     expr.py -tree prog.expr
    generate   tree    -> assembly        expr.py prog.expr

The assembly goes on through asm.py to a .vm file, as in chapter 6.

    usage: expr.py [-tokens | -tree] program.expr
"""

import sys


class CompileError(Exception):

    def __init__(self, message, line, col):
        super().__init__(message)
        self.line = line
        self.col = col


# Stage 1: scanning.
#
# The scanner turns a string of characters into a list of tokens: the
# words of the language. It knows nothing about grammar. It only
# knows what a number looks like, which characters are operators, and
# that spaces and comments do not matter.

class Token:

    def __init__(self, kind, text, line, col):
        self.kind = kind        # "number", an operator such as "+", or "end"
        self.text = text
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.line}:{self.col}  {self.kind:<8} {self.text!r}"


OPERATORS = "+-*/%();"


def scan(text):
    tokens = []
    line, col, i = 1, 1, 0
    while i < len(text):
        c = text[i]
        if c == "\n":
            line, col, i = line + 1, 1, i + 1
        elif c in " \t\r":
            col, i = col + 1, i + 1
        elif c == "#":
            while i < len(text) and text[i] != "\n":
                i += 1
        elif c in OPERATORS:
            tokens.append(Token(c, c, line, col))
            col, i = col + 1, i + 1
        elif c.isdigit():
            start = i
            while i < len(text) and text[i].isdigit():
                i += 1
            tokens.append(Token("number", text[start:i], line, col))
            col += i - start
        else:
            raise CompileError(f"unexpected character {c!r}", line, col)
    tokens.append(Token("end", "", line, col))
    return tokens


# Stage 2: parsing.
#
# The parser checks that the tokens follow the grammar, and builds a
# syntax tree that says what they mean. There is one function for
# each rule of the grammar, and each function calls the functions of
# the rules it mentions. This is a recursive descent parser.
#
# The tree has no parentheses in it: they have done their job once
# the shape of the tree is right. (2 + 3) * 7 becomes
#
#     *
#     ├── +
#     │   ├── 2
#     │   └── 3
#     └── 7

class Number:

    def __init__(self, value, token):
        self.value = value
        self.token = token


class Negate:

    def __init__(self, operand, token):
        self.operand = operand
        self.token = token


class Binary:

    def __init__(self, op, left, right, token):
        self.op = op
        self.left = left
        self.right = right
        self.token = token


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def take(self, kind):
        token = self.peek()
        if token.kind != kind:
            found = "the end of the program" if token.kind == "end" else repr(token.text)
            raise CompileError(f"expected {kind!r}, found {found}", token.line, token.col)
        self.i += 1
        return token

    def program(self):
        statements = []
        while self.peek().kind != "end":
            statements.append(self.expression())
            self.take(";")
        return statements

    def expression(self):
        node = self.term()
        while self.peek().kind in ("+", "-"):
            token = self.take(self.peek().kind)
            node = Binary(token.kind, node, self.term(), token)
        return node

    def term(self):
        node = self.unary()
        while self.peek().kind in ("*", "/", "%"):
            token = self.take(self.peek().kind)
            node = Binary(token.kind, node, self.unary(), token)
        return node

    def unary(self):
        if self.peek().kind == "-":
            token = self.take("-")
            return Negate(self.unary(), token)
        return self.factor()

    def factor(self):
        token = self.peek()
        if token.kind == "number":
            self.take("number")
            value = int(token.text)
            if value > 2**31 - 1:
                raise CompileError(f"number too large: {token.text}", token.line, token.col)
            return Number(value, token)
        if token.kind == "(":
            self.take("(")
            node = self.expression()
            self.take(")")
            return node
        found = "the end of the program" if token.kind == "end" else repr(token.text)
        raise CompileError(f"expected a number or '(', found {found}", token.line, token.col)


def parse(tokens):
    return Parser(tokens).program()


def show_tree(node, prefix="", last=True, top=True):
    """Draw a syntax tree as indented text."""
    if isinstance(node, Number):
        label, children = str(node.value), []
    elif isinstance(node, Negate):
        label, children = "negate", [node.operand]
    else:
        label, children = node.op, [node.left, node.right]
    lines = [label if top else prefix + ("└── " if last else "├── ") + label]
    inner = "" if top else prefix + ("    " if last else "│   ")
    for k, child in enumerate(children):
        lines += show_tree(child, inner, k == len(children) - 1, False)
    return lines


# Stage 3: generating code.
#
# A stack machine makes this stage almost embarrassingly simple. To
# compute left + right: compute left, leaving it on the stack; compute
# right, leaving it on top; then ADD. Every node does the same: its
# children first, then itself. That order of visiting a tree is called
# post-order, and for a stack machine it is the whole code generator.

OPCODES = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}


def generate(node, out):
    if isinstance(node, Number):
        out.append(f"        PUSH {node.value}")
    elif isinstance(node, Negate):
        out.append("        PUSH 0")
        generate(node.operand, out)
        out.append("        SUB")
    else:
        generate(node.left, out)
        generate(node.right, out)
        out.append(f"        {OPCODES[node.op]}")


def compile_program(statements):
    out = []
    for node in statements:
        line = node.token.line
        out.append(f"; line {line}")
        generate(node, out)
        out.append("        PRINT")
    out.append("        HALT")
    return "\n".join(out) + "\n"


def report(path, text, error):
    """Print an error with the line it is on and a mark under the place."""
    lines = text.splitlines()
    source = lines[error.line - 1] if error.line - 1 < len(lines) else ""
    print(f"{path}:{error.line}:{error.col}: {error}", file=sys.stderr)
    print(f"    {source}", file=sys.stderr)
    print(f"    {' ' * (error.col - 1)}^", file=sys.stderr)


def main():
    args = sys.argv[1:]
    mode = args.pop(0) if args and args[0] in ("-tokens", "-tree") else None
    if len(args) != 1:
        sys.exit("usage: expr.py [-tokens | -tree] program.expr")
    path = args[0]
    with open(path) as f:
        text = f.read()
    try:
        tokens = scan(text)
        if mode == "-tokens":
            for token in tokens:
                print(token)
            return
        statements = parse(tokens)
        if mode == "-tree":
            for node in statements:
                print("\n".join(show_tree(node)))
                print()
            return
        sys.stdout.write(compile_program(statements))
    except CompileError as error:
        report(path, text, error)
        sys.exit(1)


if __name__ == "__main__":
    main()
