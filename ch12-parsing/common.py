"""
What the three parsers share: the scanner, the syntax tree, and the
code generator. Only parsing differs between them.

The language is chapter 9's, with two comparisons added at the lowest
precedence:

    program    = { expression ";" } .
    expression = sum [ ( "<" | "=" ) sum ] ...      (see each parser)

Precedence, from loosest to tightest:

    <  =            compare, 1 if true, 0 if false
    +  -
    *  /  %
    -               negation, in front
"""

import sys


class CompileError(Exception):

    def __init__(self, message, token):
        super().__init__(message)
        self.line = token.line
        self.col = token.col


class Token:

    def __init__(self, kind, text, line, col):
        self.kind = kind
        self.text = text
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.line}:{self.col}  {self.kind:<8} {self.text!r}"


OPERATORS = "+-*/%();<="


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
            raise CompileError(f"unexpected character {c!r}", Token(c, c, line, col))
    tokens.append(Token("end", "", line, col))
    return tokens


def found(token):
    return "the end of the program" if token.kind == "end" else repr(token.text)


# The syntax tree.

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


def number(token):
    value = int(token.text)
    if value > 2**31 - 1:
        raise CompileError(f"number too large: {token.text}", token)
    return Number(value, token)


def sexp(node):
    """A tree as one line of text, in Lisp style: (* (+ 2 3) 7).
    Two trees are the same exactly when their sexps are."""
    if isinstance(node, Number):
        return str(node.value)
    if isinstance(node, Negate):
        return f"(neg {sexp(node.operand)})"
    return f"({node.op} {sexp(node.left)} {sexp(node.right)})"


# Code generation: post-order, as in chapter 9.

OPCODES = {"+": ["ADD"], "-": ["SUB"], "*": ["MUL"], "/": ["DIV"], "%": ["MOD"],
           "<": ["LT"], "=": ["EQ"]}


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
        out += [f"        {op}" for op in OPCODES[node.op]]


def compile_program(statements):
    out = []
    for node in statements:
        generate(node, out)
        out.append("        PRINT")
    out.append("        HALT")
    return "\n".join(out) + "\n"


def report(path, text, error):
    lines = text.splitlines()
    source = lines[error.line - 1] if 0 < error.line <= len(lines) else ""
    print(f"{path}:{error.line}:{error.col}: {error}", file=sys.stderr)
    print(f"    {source}", file=sys.stderr)
    print(f"    {' ' * (error.col - 1)}^", file=sys.stderr)
