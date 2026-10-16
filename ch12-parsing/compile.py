#!/usr/bin/env python3
"""
Compile with any of the three parsers. They must all build the same
tree, so whichever is chosen, the assembly is the same.

    usage: compile.py [-descent | -pratt | -combinators] [-tree] program.expr

-descent is the default. With -tree, print each tree as an
s-expression instead of compiling.
"""

import sys

import combinators
import common
import descent
import pratt

PARSERS = {"-descent": descent, "-pratt": pratt, "-combinators": combinators}


def main():
    args = sys.argv[1:]
    parser = descent
    if args and args[0] in PARSERS:
        parser = PARSERS[args.pop(0)]
    tree = args[:1] == ["-tree"]
    if tree:
        args.pop(0)
    if len(args) != 1:
        sys.exit("usage: compile.py [-descent | -pratt | -combinators] [-tree] program.expr")
    path = args[0]
    with open(path) as f:
        text = f.read()
    try:
        statements = parser.parse(common.scan(text))
    except common.CompileError as error:
        common.report(path, text, error)
        sys.exit(1)
    if tree:
        for node in statements:
            print(common.sexp(node))
    else:
        sys.stdout.write(common.compile_program(statements))


if __name__ == "__main__":
    main()
