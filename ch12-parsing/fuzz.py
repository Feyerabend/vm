#!/usr/bin/env python3
"""
Write random expressions, and what they must evaluate to.

Chapter 9's fuzz.py, with the comparisons < and = added, at the
loosest precedence.

The expressions are printed with as few parentheses as the grammar
allows, so the parser's handling of precedence (* before +) and of
left-to-right order (100 - 10 - 1) is put to the test. Now and then
a pair of parentheses that is not needed is added too.

The expected values are computed here, in Python, following the rules
of the specification: 32-bit wrapping, and division rounding towards
zero. If the compiler, the assembler and the machine all do their
job, running the program prints exactly the expected values.

    usage: fuzz.py seed count program.expr expected.out
"""

import random
import sys

COMPARISON, ADDITIVE, MULTIPLICATIVE, UNARY, ATOM = 0, 1, 2, 3, 4
PRECEDENCE = {"<": COMPARISON, "=": COMPARISON, "+": ADDITIVE, "-": ADDITIVE,
              "*": MULTIPLICATIVE, "/": MULTIPLICATIVE, "%": MULTIPLICATIVE}


def wrap(n):
    return (n + 2**31) % 2**32 - 2**31


def evaluate(node):
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "neg":
        return wrap(-evaluate(node[1]))
    a, b = evaluate(node[1]), evaluate(node[2])
    if kind == "+":
        return wrap(a + b)
    if kind == "-":
        return wrap(a - b)
    if kind == "*":
        return wrap(a * b)
    if kind == "<":
        return int(a < b)
    if kind == "=":
        return int(a == b)
    q = abs(a) // abs(b)
    q = q if (a < 0) == (b < 0) else -q
    return wrap(q) if kind == "/" else wrap(a - b * q)


def make(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        return ("num", rng.choice([0, 1, 2, 3, 7, 10, 255, rng.randint(0, 2**31 - 1)]))
    if rng.random() < 0.15:
        return ("neg", make(rng, depth - 1))
    op = rng.choice("+-*/%<=")
    left, right = make(rng, depth - 1), make(rng, depth - 1)
    if op in "/%":
        while evaluate(right) == 0:
            right = make(rng, depth - 1)
    return (op, left, right)


def precedence(node):
    if node[0] == "num":
        return ATOM
    if node[0] == "neg":
        return UNARY
    return PRECEDENCE[node[0]]


def render(rng, node):
    if node[0] == "num":
        return str(node[1])
    if node[0] == "neg":
        inner = render(rng, node[1])
        return "-" + (f"({inner})" if precedence(node[1]) < UNARY else inner)
    p = precedence(node)
    left, right = render(rng, node[1]), render(rng, node[2])
    if precedence(node[1]) < p or rng.random() < 0.05:
        left = f"({left})"
    if precedence(node[2]) <= p or rng.random() < 0.05:
        right = f"({right})"
    return f"{left} {node[0]} {right}"


def main():
    seed, count, program, expected = sys.argv[1:]
    rng = random.Random(int(seed))
    with open(program, "w") as p, open(expected, "w") as e:
        for _ in range(int(count)):
            node = make(rng, rng.randint(1, 6))
            p.write(render(rng, node) + ";\n")
            e.write(f"{evaluate(node)}\n")


if __name__ == "__main__":
    main()
