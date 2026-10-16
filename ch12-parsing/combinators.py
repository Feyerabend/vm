"""
Parser 3: parser combinators.

Here a parser is a value: a function that takes the tokens and a
position, and returns what it found and where it stopped, or None if
it found nothing. Small parsers are combined into bigger ones by
ordinary functions, the *combinators*:

    token("number")         one token of that kind
    seq(a, b, c)            a, then b, then c
    alt(a, b)               a, or else b
    many(a)                 a, any number of times
    apply(a, f)             a, with f applied to what it found
    chain_left(a, ops)      a, then any number of (op a), grouped from the left

and the grammar is then written down almost as it reads in EBNF; see
the bottom of this file. This is the idea of archive/parse, here
working on tokens, building the same trees as the other two parsers.

Combinators make a grammar easy to write and to change. Their
traditional weakness is error messages: when alt(a, b) fails, which
failure should be reported, a's or b's? The answer used here is the
usual one: report the failure that got *furthest* into the input,
since that is nearly always where the mistake is.
"""

from common import Binary, CompileError, Negate, found, number


class State:
    """Remembers the furthest place any parser failed, and what it wanted there."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.furthest = 0
        self.expected = set()

    def fail(self, i, what):
        if i > self.furthest:
            self.furthest, self.expected = i, {what}
        elif i == self.furthest:
            self.expected.add(what)
        return None


def token(kind):
    def parse(state, i):
        if state.tokens[i].kind == kind:
            return state.tokens[i], i + 1
        return state.fail(i, kind)
    return parse


def seq(*parsers):
    def parse(state, i):
        values = []
        for p in parsers:
            result = p(state, i)
            if result is None:
                return None
            value, i = result
            values.append(value)
        return values, i
    return parse


def alt(*parsers):
    def parse(state, i):
        for p in parsers:
            result = p(state, i)
            if result is not None:
                return result
        return None
    return parse


def many(parser):
    def parse(state, i):
        values = []
        while True:
            result = parser(state, i)
            if result is None:
                return values, i
            value, i = result
            values.append(value)
    return parse


def apply(parser, f):
    def parse(state, i):
        result = parser(state, i)
        if result is None:
            return None
        value, i = result
        return f(value), i
    return parse


def lazy(make):
    """A parser defined later: needed for a grammar that refers to itself."""
    def parse(state, i):
        return make()(state, i)
    return parse


def chain_left(operand, operators):
    """operand { op operand }, built into a left-leaning tree."""
    op = alt(*[token(o) for o in operators])
    rest = many(seq(op, operand))

    def build(values):
        node, pairs = values
        for token, right in pairs:
            node = Binary(token.kind, node, right, token)
        return node
    return apply(seq(operand, rest), build)


# The grammar.

def negate(values):
    minus, operand = values
    return Negate(operand, minus)


primary = alt(
    apply(token("number"), number),
    apply(seq(token("("), lazy(lambda: comparison), token(")")), lambda v: v[1]),
)
unary = alt(
    apply(seq(token("-"), lazy(lambda: unary)), negate),
    primary,
)
product = chain_left(unary, "*/%")
total = chain_left(product, "+-")
comparison = chain_left(total, "<=")
statement = apply(seq(comparison, token(";")), lambda v: v[0])
program = apply(seq(many(statement), token("end")), lambda v: v[0])


def describe(kind):
    return "a number" if kind == "number" else repr(kind)


def parse(tokens):
    state = State(tokens)
    result = program(state, 0)
    if result is None:
        at = tokens[state.furthest]
        wanted = " or ".join(sorted(describe(k) for k in state.expected))
        raise CompileError(f"expected {wanted}, found {found(at)}", at)
    return result[0]
