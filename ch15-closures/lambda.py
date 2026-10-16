#!/usr/bin/env python3
"""
A compiler for lambda/0.

lambda/0 is a small functional language, in the style of ML. Every
construct is an expression with a value, variables never change once
bound, and functions are values like any other:

    let add x y = x + y in
    let add5 = add 5 in          # a new function, made from add
    print (add5 10)              # 15

The grammar:

    program     = sequence .
    sequence    = expr { ";" expr } .
    expr        = "let" [ "rec" ] name { name } "=" expr "in" sequence
                | "fun" name { name } "->" sequence
                | "if" expr "then" expr "else" expr
                | "print" expr
                | comparison .
    comparison  = sum [ ( "<" | ">" | "=" | "<>" | "<=" | ">=" ) sum ] .
    sum         = product { ( "+" | "-" ) product } .
    product     = unary { ( "*" | "/" | "%" ) unary } .
    unary       = "-" unary | application .
    application = atom { atom } .
    atom        = number | name | "(" sequence ")" .

Every function takes exactly one argument. 'fun x y -> e' is short for
'fun x -> fun y -> e', and 'f a b' means '(f a) b': applying a
function of two arguments to one gives back a function waiting for
the second. This is called currying, after Haskell Curry.

'let f x = e' is short for 'let f = fun x -> e'. 'let rec' lets a
function refer to itself. 'print e' prints e and has e as its value.
'#' starts a comment.

    usage: lambda.py [-tree] program.lam
"""

import sys


class CompileError(Exception):

    def __init__(self, message, token):
        super().__init__(message)
        self.line = token.line
        self.col = token.col


# Scanning.

KEYWORDS = {"let", "rec", "in", "fun", "if", "then", "else", "print"}
SYMBOLS = ["->", "<>", "<=", ">=", "=", "<", ">", "+", "-", "*", "/", "%", "(", ")", ";"]


class Token:

    def __init__(self, kind, text, line, col):
        self.kind, self.text, self.line, self.col = kind, text, line, col


def scan(text):
    tokens = []
    for line_no, line in enumerate(text.splitlines(), 1):
        i = 0
        while i < len(line):
            c = line[i]
            if c.isspace():
                i += 1
            elif c == "#":
                break
            elif c.isalpha() or c == "_":
                start = i
                while i < len(line) and (line[i].isalnum() or line[i] in "_'"):
                    i += 1
                word = line[start:i]
                tokens.append(Token(word if word in KEYWORDS else "name", word, line_no, start + 1))
            elif c.isdigit():
                start = i
                while i < len(line) and line[i].isdigit():
                    i += 1
                tokens.append(Token("number", line[start:i], line_no, start + 1))
            else:
                for symbol in SYMBOLS:
                    if line.startswith(symbol, i):
                        tokens.append(Token(symbol, symbol, line_no, i + 1))
                        i += len(symbol)
                        break
                else:
                    raise CompileError(f"unexpected character {c!r}", Token(c, c, line_no, i + 1))
    if tokens:
        last = tokens[-1]
        tokens.append(Token("end", "", last.line, last.col + len(last.text)))
    else:
        tokens.append(Token("end", "", 1, 1))
    return tokens


# The syntax tree. Each kind of node is a tuple whose first element
# names it, and whose last is the token it started at:
#
#     ("num", value, tok)            ("var", name, tok)
#     ("neg", e, tok)                ("op", op, left, right, tok)
#     ("if", c, then, else, tok)     ("print", e, tok)
#     ("fun", param, body, tok)      ("app", function, argument, tok)
#     ("let", name, value, body, recursive, tok)
#     ("seq", [e1, e2, ...], tok)

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def at(self, *kinds):
        return self.peek().kind in kinds

    def take(self, kind):
        token = self.peek()
        if token.kind != kind:
            found = "the end of the program" if token.kind == "end" else repr(token.text)
            wanted = "a name" if kind == "name" else repr(kind)
            raise CompileError(f"expected {wanted}, found {found}", token)
        self.i += 1
        return token

    def program(self):
        node = self.sequence()
        self.take("end")
        return node

    def sequence(self):
        token = self.peek()
        items = [self.expr()]
        while self.at(";"):
            self.take(";")
            items.append(self.expr())
        return items[0] if len(items) == 1 else ("seq", items, token)

    def expr(self):
        token = self.peek()
        if self.at("let"):
            self.take("let")
            recursive = self.at("rec")
            if recursive:
                self.take("rec")
            name = self.take("name")
            params = []
            while self.at("name"):
                params.append(self.take("name"))
            self.take("=")
            value = self.expr()
            for p in reversed(params):
                value = ("fun", p.text, value, p)
            if recursive and value[0] != "fun":
                raise CompileError("only a function can be 'let rec'", name)
            self.take("in")
            # The body reaches as far to the right as it can, past
            # semicolons: everything after 'in' is in the scope of name.
            return ("let", name.text, value, self.sequence(), recursive, name)
        if self.at("fun"):
            self.take("fun")
            params = [self.take("name")]
            while self.at("name"):
                params.append(self.take("name"))
            self.take("->")
            body = self.sequence()
            for p in reversed(params):
                body = ("fun", p.text, body, p)
            return body
        if self.at("if"):
            self.take("if")
            condition = self.expr()
            self.take("then")
            then = self.expr()
            self.take("else")
            return ("if", condition, then, self.expr(), token)
        if self.at("print"):
            self.take("print")
            return ("print", self.expr(), token)
        return self.comparison()

    def comparison(self):
        left = self.sum()
        if self.at("<", ">", "=", "<>", "<=", ">="):
            op = self.take(self.peek().kind)
            return ("op", op.kind, left, self.sum(), op)
        return left

    def sum(self):
        node = self.product()
        while self.at("+", "-"):
            op = self.take(self.peek().kind)
            node = ("op", op.kind, node, self.product(), op)
        return node

    def product(self):
        node = self.unary()
        while self.at("*", "/", "%"):
            op = self.take(self.peek().kind)
            node = ("op", op.kind, node, self.unary(), op)
        return node

    def unary(self):
        if self.at("-"):
            token = self.take("-")
            return ("neg", self.unary(), token)
        return self.application()

    def application(self):
        node = self.atom()
        while self.at("number", "name", "("):
            token = self.peek()
            node = ("app", node, self.atom(), token)
        return node

    def atom(self):
        token = self.peek()
        if self.at("number"):
            self.take("number")
            if int(token.text) > 2**31 - 1:
                raise CompileError(f"number too large: {token.text}", token)
            return ("num", int(token.text), token)
        if self.at("name"):
            self.take("name")
            return ("var", token.text, token)
        if self.at("("):
            self.take("(")
            node = self.sequence()
            self.take(")")
            return node
        found = "the end of the program" if token.kind == "end" else repr(token.text)
        raise CompileError(f"expected a value, found {found}", token)


# Free variables: the variables an expression uses but does not bind.
# A function must carry the values of its free variables with it,
# since it may be called long after the place that bound them is gone.

def free(node):
    kind = node[0]
    if kind == "num":
        return set()
    if kind == "var":
        return {node[1]}
    if kind in ("neg", "print"):
        return free(node[1])
    if kind == "op":
        return free(node[2]) | free(node[3])
    if kind == "if":
        return free(node[1]) | free(node[2]) | free(node[3])
    if kind == "app":
        return free(node[1]) | free(node[2])
    if kind == "fun":
        return free(node[2]) - {node[1]}
    if kind == "let":
        _, name, value, body, recursive, _ = node
        if recursive:
            return (free(value) | free(body)) - {name}
        return free(value) | (free(body) - {name})
    if kind == "seq":
        return set().union(*(free(e) for e in node[1]))
    raise ValueError(kind)


def first_use(node, name):
    """The token where name is first used in node, for error messages."""
    if node[0] == "var":
        return node[2] if node[1] == name else None
    children = node[1] if node[0] == "seq" else [c for c in node[1:-1] if isinstance(c, tuple)]
    for child in children:
        found = first_use(child, name)
        if found:
            return found
    return None


# Code generation.
#
# A function is compiled into code that expects two locals: local 0 is
# its own closure, local 1 its argument. A closure is a block:
#
#     field 0       the address of the function's code
#     field 1 ...   the values of its free variables, in sorted order
#
# To call a closure c with an argument a: push c, push a, take field 0
# of c, and CALLI 2. The called code finds c and a as locals 0 and 1.
#
# Where each variable is, during code generation:
#
#     ("local", k)        local k of the current frame: LOAD k
#     ("captured", i)     field i of the current closure: LOAD 0, PUSH i, GETF
#
# 'depth' counts the values above the frame pointer at each point, so
# that a 'let' knows which local its value will be.

COMPARISONS = {
    "=": ["EQ"], "<>": ["EQ", "PUSH 0", "EQ"], "<": ["LT"], ">": ["SWAP", "LT"],
    "<=": ["SWAP", "LT", "PUSH 0", "EQ"], ">=": ["LT", "PUSH 0", "EQ"],
}
ARITHMETIC = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}


class Generator:

    def __init__(self):
        self.out = []
        self.functions = []     # (label, fun node, free variables), waiting to be compiled
        self.labels = 0

    def emit(self, instruction):
        self.out.append(f"        {instruction}")

    def new_label(self, stem="L"):
        self.labels += 1
        return f"{stem}{self.labels}"

    def program(self, node):
        self.out.append("main:")
        self.gen(node, {}, 0)
        self.emit("DROP")
        self.emit("HALT")
        while self.functions:
            label, fun, names = self.functions.pop(0)
            self.out.append("")
            self.out.append(f"; fun {fun[1]} -> ..., capturing: {' '.join(names) or 'nothing'}")
            self.out.append(f"{label}:")
            env = {fun[1]: ("local", 1)}
            for i, name in enumerate(names):
                env.setdefault(name, ("captured", i + 1))
            self.gen(fun[2], env, 2)
            self.emit("RET")
        return "\n".join(self.out) + "\n"

    def variable(self, name, env, token):
        if name not in env:
            raise CompileError(f"'{name}' is not defined", token)
        where, k = env[name]
        if where == "local":
            self.emit(f"LOAD {k}")
        else:
            self.emit("LOAD 0")
            self.emit(f"PUSH {k}")
            self.emit("GETF")

    def closure(self, fun, env, depth, itself=None):
        """Make a closure for fun. If itself is a name, fun is being
        bound to that name by 'let rec', and may refer to itself."""
        names = sorted(free(fun))
        for name in names:
            if name != itself and name not in env:
                raise CompileError(f"'{name}' is not defined", first_use(fun, name))
        label = self.new_label("fun_")
        self.functions.append((label, fun, names))
        self.emit(f"PUSH {1 + len(names)}")
        self.emit("NEW")
        self.emit("DUP")
        self.emit("PUSH 0")
        self.emit(f"PUSH {label}")
        self.emit("SETF")
        for i, name in enumerate(names):
            self.emit("DUP")
            self.emit(f"PUSH {i + 1}")
            if name == itself:
                self.emit("OVER")           # the closure being made
            else:
                self.variable(name, env, fun[3])
            self.emit("SETF")

    def gen(self, node, env, depth):
        """Generate code that leaves the value of node on the stack."""
        kind = node[0]
        if kind == "num":
            self.emit(f"PUSH {node[1]}")
        elif kind == "var":
            self.variable(node[1], env, node[2])
        elif kind == "neg":
            self.emit("PUSH 0")
            self.gen(node[1], env, depth + 1)
            self.emit("SUB")
        elif kind == "op":
            _, op, left, right, _ = node
            self.gen(left, env, depth)
            self.gen(right, env, depth + 1)
            for instruction in COMPARISONS.get(op, [ARITHMETIC.get(op)]):
                self.emit(instruction)
        elif kind == "if":
            _, condition, then, otherwise, _ = node
            other, done = self.new_label(), self.new_label()
            self.gen(condition, env, depth)
            self.emit(f"JZ {other}")
            self.gen(then, env, depth)
            self.emit(f"JMP {done}")
            self.out.append(f"{other}:")
            self.gen(otherwise, env, depth)
            self.out.append(f"{done}:")
        elif kind == "print":
            self.gen(node[1], env, depth)
            self.emit("DUP")
            self.emit("PRINT")
        elif kind == "fun":
            self.closure(node, env, depth)
        elif kind == "app":
            _, function, argument, _ = node
            self.gen(function, env, depth)
            self.gen(argument, env, depth + 1)
            self.emit("OVER")
            self.emit("PUSH 0")
            self.emit("GETF")               # the code address of the closure
            self.emit("CALLI 2")
        elif kind == "let":
            _, name, value, body, recursive, _ = node
            if recursive:
                self.closure(value, env, depth, itself=name)
            else:
                self.gen(value, env, depth)
            inner = dict(env)
            inner[name] = ("local", depth)
            self.gen(body, inner, depth + 1)
            self.emit("SWAP")
            self.emit("DROP")               # the let's local, under the result
        elif kind == "seq":
            for k, item in enumerate(node[1]):
                self.gen(item, env, depth)
                if k < len(node[1]) - 1:
                    self.emit("DROP")


def show(node):
    kind = node[0]
    if kind == "num":
        return str(node[1])
    if kind == "var":
        return node[1]
    if kind == "neg":
        return f"(neg {show(node[1])})"
    if kind == "op":
        return f"({node[1]} {show(node[2])} {show(node[3])})"
    if kind == "if":
        return f"(if {show(node[1])} {show(node[2])} {show(node[3])})"
    if kind == "print":
        return f"(print {show(node[1])})"
    if kind == "fun":
        return f"(fun {node[1]} {show(node[2])})"
    if kind == "app":
        return f"({show(node[1])} {show(node[2])})"
    if kind == "let":
        return f"(let{' rec' if node[4] else ''} {node[1]} {show(node[2])} {show(node[3])})"
    return "(seq " + " ".join(show(e) for e in node[1]) + ")"


def report(path, text, error):
    lines = text.splitlines()
    source = lines[error.line - 1] if 0 < error.line <= len(lines) else ""
    print(f"{path}:{error.line}:{error.col}: {error}", file=sys.stderr)
    print(f"    {source}", file=sys.stderr)
    print(f"    {' ' * (error.col - 1)}^", file=sys.stderr)


def main():
    args = sys.argv[1:]
    tree = args[:1] == ["-tree"]
    if tree:
        args.pop(0)
    if len(args) != 1:
        sys.exit("usage: lambda.py [-tree] program.lam")
    path = args[0]
    with open(path) as f:
        text = f.read()
    try:
        node = Parser(scan(text)).program()
        if tree:
            print(show(node))
            return
        sys.stdout.write(Generator().program(node))
    except CompileError as error:
        report(path, text, error)
        sys.exit(1)


if __name__ == "__main__":
    main()
