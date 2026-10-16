"""
Parser 1: recursive descent, as in chapters 9 to 11.

One function for each level of precedence, each calling the next
tighter one. Adding the comparisons meant adding a level: a new rule
in the grammar, and a new function on top.

    program    = { comparison ";" } .
    comparison = sum { ( "<" | "=" ) sum } .
    sum        = product { ( "+" | "-" ) product } .
    product    = unary { ( "*" | "/" | "%" ) unary } .
    unary      = "-" unary | primary .
    primary    = number | "(" comparison ")" .
"""

from common import Binary, CompileError, Negate, found, number


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def take(self, kind):
        token = self.peek()
        if token.kind != kind:
            raise CompileError(f"expected {kind!r}, found {found(token)}", token)
        self.i += 1
        return token

    def program(self):
        statements = []
        while self.peek().kind != "end":
            statements.append(self.comparison())
            self.take(";")
        return statements

    def left_associative(self, operators, operand):
        node = operand()
        while self.peek().kind in operators:
            token = self.take(self.peek().kind)
            node = Binary(token.kind, node, operand(), token)
        return node

    def comparison(self):
        return self.left_associative("<=", self.sum)

    def sum(self):
        return self.left_associative("+-", self.product)

    def product(self):
        return self.left_associative("*/%", self.unary)

    def unary(self):
        if self.peek().kind == "-":
            token = self.take("-")
            return Negate(self.unary(), token)
        return self.primary()

    def primary(self):
        token = self.peek()
        if token.kind == "number":
            return number(self.take("number"))
        if token.kind == "(":
            self.take("(")
            node = self.comparison()
            self.take(")")
            return node
        raise CompileError(f"expected a number or '(', found {found(token)}", token)


def parse(tokens):
    return Parser(tokens).program()
