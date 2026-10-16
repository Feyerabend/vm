#!/usr/bin/env python3
"""
Parse a program with all three parsers, and check that they build
exactly the same trees, comparing them as s-expressions.

    usage: same.py program.expr
"""

import sys

import combinators
import common
import descent
import pratt


def main():
    path = sys.argv[1]
    with open(path) as f:
        tokens = common.scan(f.read())
    trees = {}
    for name, parser in (("descent", descent), ("pratt", pratt), ("combinators", combinators)):
        trees[name] = [common.sexp(t) for t in parser.parse(tokens)]
    reference = trees["descent"]
    for name, sexps in trees.items():
        for k, (a, b) in enumerate(zip(reference, sexps)):
            if a != b:
                sys.exit(f"{path}: statement {k + 1}: descent and {name} differ\n  {a}\n  {b}")
        if len(sexps) != len(reference):
            sys.exit(f"{path}: {name} found {len(sexps)} statements, descent {len(reference)}")
    print(f"{path}: {len(reference)} trees, the same from all three parsers")


if __name__ == "__main__":
    main()
