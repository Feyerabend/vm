"""
Parser 2: a Pratt parser.

Vaughan Pratt, 1973: "Top down operator precedence". Instead of one
function per level of precedence, there is one table, and one loop.

Each infix operator has a *binding power*: how tightly it holds the
operands on either side of it. To parse an expression, take an
operand, then keep taking operators, but only those that bind more
tightly than whatever asked for this expression in the first place.

    2 + 3 * 7 < 30
        ^ power 20: take 3 * 7 first, since * binds at 30, more than 20
                ^ < binds at 10, less than 20: stop, and hand back 3 * 7

Adding the comparisons to this parser meant adding two lines to the
table, and nothing else.

Associativity is in the numbers too. The right operand of an operator
is parsed with that operator's own power as the minimum, and the loop
only takes operators with *more* power than the minimum. So a second
operator of the same power stops it, and 100 - 10 - 1 is
(100 - 10) - 1: left-associative. For a right-associative operator,
such as a power operator, pass its power minus one instead, and the
second one is let in.
"""

from common import Binary, CompileError, Negate, found, number

# infix operator -> binding power
INFIX = {
    "<": 10, "=": 10,
    "+": 20, "-": 20,
    "*": 30, "/": 30, "%": 30,
}

PREFIX_MINUS = 40       # -2 * 3 is (-2) * 3


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
            statements.append(self.expression(0))
            self.take(";")
        return statements

    def expression(self, min_power):
        """Parse an expression, taking only operators that bind more
        tightly than min_power."""
        left = self.prefix()
        while True:
            token = self.peek()
            power = INFIX.get(token.kind)
            if power is None or power <= min_power:
                return left
            self.take(token.kind)
            right = self.expression(power)          # left-associative: stop at equal power
            left = Binary(token.kind, left, right, token)

    def prefix(self):
        """What can begin an expression: a number, a parenthesis, a minus."""
        token = self.peek()
        if token.kind == "number":
            return number(self.take("number"))
        if token.kind == "(":
            self.take("(")
            node = self.expression(0)
            self.take(")")
            return node
        if token.kind == "-":
            self.take("-")
            return Negate(self.expression(PREFIX_MINUS), token)
        raise CompileError(f"expected a number or '(', found {found(token)}", token)


def parse(tokens):
    return Parser(tokens).program()
