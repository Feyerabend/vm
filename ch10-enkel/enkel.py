#!/usr/bin/env python3
"""
A compiler for enkel/0.

enkel/0 is a small procedural language in the family of PL/0 and
Pascal. A program has global constants, arrays and variables,
procedures with arguments and local variables, and a main block:

    array A:10;
    var n;

    procedure square[x];
    begin
        return x * x
    end;

    begin
        n is 0;
        while n < 10 do
        begin
            call square[n];
            A.n is rval;
            n is n + 1
        end;
        print A.9
    end.

The full grammar is in LANG.md. This compiler has the same three
stages as the expression compiler of chapter 9, and one more:

    scan       text    -> tokens
    parse      tokens  -> syntax tree
    resolve    tree    -> tree, with every name looked up
    generate   tree    -> assembly

The new stage, resolving, is what a language with names needs. It
decides what each name means, a constant, a global variable, an
array, a local of the current procedure, or a procedure, and refuses
names that mean nothing.

    usage: enkel.py [-tokens | -tree] program.p
"""

import sys


class CompileError(Exception):

    def __init__(self, message, token):
        super().__init__(message)
        self.line = token.line
        self.col = token.col


# Stage 1: scanning.

KEYWORDS = {
    "const", "array", "var", "procedure", "call", "begin", "end",
    "if", "then", "else", "while", "do", "return", "print", "emit",
    "is", "and", "or", "xor",
}

SYMBOLS = ["<=", ">=", ".", ",", ";", ":", "[", "]", "(", ")",
           "=", "#", "<", ">", "+", "-", "*", "/", "%"]


class Token:

    def __init__(self, kind, text, line, col):
        self.kind = kind        # "name", "number", a keyword, a symbol, or "end of file"
        self.text = text
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.line}:{self.col}  {self.kind:<10} {self.text!r}"


def scan(text):
    tokens = []
    line, col, i = 1, 1, 0

    def advance(n):
        nonlocal i, col
        i += n
        col += n

    while i < len(text):
        c = text[i]
        if c == "\n":
            line, col, i = line + 1, 1, i + 1
        elif c.isspace():
            advance(1)
        elif c == "{":
            start = Token("{", "{", line, col)
            while i < len(text) and text[i] != "}":
                if text[i] == "\n":
                    line, col, i = line + 1, 0, i
                advance(1)
            if i == len(text):
                raise CompileError("comment is never closed", start)
            advance(1)
        elif c.isalpha() or c == "_":
            start = i
            while i < len(text) and (text[i].isalnum() or text[i] == "_"):
                i += 1
            word = text[start:i]
            kind = word if word in KEYWORDS else "name"
            tokens.append(Token(kind, word, line, col))
            col += i - start
        elif c.isdigit():
            start = i
            while i < len(text) and text[i].isdigit():
                i += 1
            tokens.append(Token("number", text[start:i], line, col))
            col += i - start
        else:
            for symbol in SYMBOLS:
                if text.startswith(symbol, i):
                    tokens.append(Token(symbol, symbol, line, col))
                    advance(len(symbol))
                    break
            else:
                raise CompileError(f"unexpected character {c!r}", Token(c, c, line, col))
    # The end of the file is placed just after the last token, which is
    # where a message about something missing there should point.
    if tokens:
        last = tokens[-1]
        line, col = last.line, last.col + len(last.text)
    tokens.append(Token("end of file", "", line, col))
    return tokens


# Stage 2: parsing.
#
# The syntax tree is made of the classes below. Each remembers the
# token it started at, so later stages can report errors in the right
# place.

class Node:

    def __init__(self, token, **fields):
        self.token = token
        self.__dict__.update(fields)

    def __repr__(self):
        fields = {k: v for k, v in self.__dict__.items() if k != "token"}
        return f"{type(self).__name__}{fields}"


class Program(Node): pass           # consts, arrays, globals, procedures, body
class Procedure(Node): pass         # name, params, consts, locals, body
class Assign(Node): pass            # target, value
class Call(Node): pass              # name, args
class Block(Node): pass             # statements
class If(Node): pass                # condition, then, otherwise
class While(Node): pass             # condition, body
class DoWhile(Node): pass           # body, condition
class Return(Node): pass            # value or None
class Print(Node): pass             # value
class Emit(Node): pass              # value
class Empty(Node): pass
class Compare(Node): pass           # op, left, right
class Binary(Node): pass            # op, left, right
class Negate(Node): pass            # operand
class Number(Node): pass            # value
class Name(Node): pass              # name, and after resolving: meaning
class Element(Node): pass           # name, index, and after resolving: meaning


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
            raise CompileError(f"expected {self.describe(kind)}, found {self.found(token)}", token)
        self.i += 1
        return token

    def describe(self, kind):
        return "a name" if kind == "name" else "a number" if kind == "number" else repr(kind)

    def found(self, token):
        return "the end of the file" if token.kind == "end of file" else repr(token.text)

    def number(self):
        token = self.take("number")
        value = int(token.text)
        if value > 2**31 - 1:
            raise CompileError(f"number too large: {token.text}", token)
        return value

    # program = block "." .
    def program(self):
        token = self.peek()
        consts, arrays, variables, procedures, body = self.block(top=True)
        self.take(".")
        self.take("end of file")
        return Program(token, consts=consts, arrays=arrays, globals=variables,
                       procedures=procedures, body=body)

    # block = ["const" ...] ["array" ...] ["var" ...] {procedure} statement .
    def block(self, top):
        consts, arrays, variables, procedures = [], [], [], []
        if self.at("const"):
            self.take("const")
            while True:
                name = self.take("name")
                self.take("=")
                consts.append((name, self.number()))
                if not self.at(","):
                    break
                self.take(",")
            self.take(";")
        if self.at("array"):
            token = self.take("array")
            if not top:
                raise CompileError("arrays can only be declared at the top of the program", token)
            while True:
                name = self.take("name")
                self.take(":")
                size_token = self.peek()
                size = self.number()
                if size < 1:
                    raise CompileError("an array needs at least one element", size_token)
                arrays.append((name, size))
                if not self.at(","):
                    break
                self.take(",")
            self.take(";")
        if self.at("var"):
            self.take("var")
            variables.append(self.take("name"))
            while self.at(","):
                self.take(",")
                variables.append(self.take("name"))
            self.take(";")
        while self.at("procedure"):
            token = self.take("procedure")
            if not top:
                raise CompileError("procedures cannot be declared inside procedures", token)
            name = self.take("name")
            self.take("[")
            params = []
            if self.at("name"):
                params.append(self.take("name"))
                while self.at(","):
                    self.take(",")
                    params.append(self.take("name"))
            self.take("]")
            self.take(";")
            p_consts, _, p_locals, _, p_body = self.block(top=False)
            self.take(";")
            procedures.append(Procedure(token, name=name, params=params, consts=p_consts,
                                        locals=p_locals, body=p_body))
        return consts, arrays, variables, procedures, self.statement()

    def statement(self):
        token = self.peek()
        if self.at("name"):
            target = self.variable()
            self.take("is")
            return Assign(token, target=target, value=self.expression())
        if self.at("call"):
            self.take("call")
            name = self.take("name")
            self.take("[")
            args = []
            if not self.at("]"):
                args.append(self.expression())
                while self.at(","):
                    self.take(",")
                    args.append(self.expression())
            self.take("]")
            return Call(token, name=name, args=args)
        if self.at("begin"):
            self.take("begin")
            statements = [self.statement()]
            while self.at(";"):
                self.take(";")
                statements.append(self.statement())
            self.take("end")
            return Block(token, statements=statements)
        if self.at("if"):
            self.take("if")
            condition = self.condition()
            self.take("then")
            then = self.statement()
            otherwise = None
            if self.at("else"):
                self.take("else")
                otherwise = self.statement()
            return If(token, condition=condition, then=then, otherwise=otherwise)
        if self.at("while"):
            self.take("while")
            condition = self.condition()
            self.take("do")
            return While(token, condition=condition, body=self.statement())
        if self.at("do"):
            self.take("do")
            body = self.statement()
            self.take("while")
            return DoWhile(token, body=body, condition=self.condition())
        if self.at("return"):
            self.take("return")
            value = None
            if not self.at(";", "end", "else", "while", ".", "end of file"):
                value = self.expression()
            return Return(token, value=value)
        if self.at("print"):
            self.take("print")
            return Print(token, value=self.expression())
        if self.at("emit"):
            self.take("emit")
            return Emit(token, value=self.expression())
        return Empty(token)

    # condition = expression [("=" | "#" | "<" | "<=" | ">" | ">=") expression] .
    def condition(self):
        left = self.expression()
        if self.at("=", "#", "<", "<=", ">", ">="):
            token = self.take(self.peek().kind)
            return Compare(token, op=token.kind, left=left, right=self.expression())
        return left

    # expression = term {("+" | "-" | "or" | "xor") term} .
    def expression(self):
        node = self.term()
        while self.at("+", "-", "or", "xor"):
            token = self.take(self.peek().kind)
            node = Binary(token, op=token.kind, left=node, right=self.term())
        return node

    # term = factor {("*" | "/" | "%" | "and") factor} .
    def term(self):
        node = self.factor()
        while self.at("*", "/", "%", "and"):
            token = self.take(self.peek().kind)
            node = Binary(token, op=token.kind, left=node, right=self.factor())
        return node

    # factor = variable | number | "(" expression ")" | "-" factor .
    def factor(self):
        token = self.peek()
        if self.at("name"):
            return self.variable()
        if self.at("number"):
            return Number(token, value=self.number())
        if self.at("("):
            self.take("(")
            node = self.expression()
            self.take(")")
            return node
        if self.at("-"):
            self.take("-")
            return Negate(token, operand=self.factor())
        raise CompileError(f"expected a value, found {self.found(token)}", token)

    # variable = name ["." (name | number | "(" expression ")")] .
    def variable(self):
        name = self.take("name")
        if not self.at("."):
            return Name(name, name=name.text)
        self.take(".")
        token = self.peek()
        if self.at("name"):
            index = Name(token, name=self.take("name").text)
        elif self.at("number"):
            index = Number(token, value=self.number())
        elif self.at("("):
            self.take("(")
            index = self.expression()
            self.take(")")
        else:
            raise CompileError(f"expected an index, found {self.found(token)}", token)
        return Element(name, name=name.text, index=index)


# Stage 3: resolving names.
#
# Every name gets a meaning:
#
#     ("const", value)          a constant: just a number
#     ("global", address)       a global variable, at a memory address
#     ("array", base, size)     an array, from base to base + size - 1
#     ("local", k)              local k of the current call
#     ("procedure", node)       a procedure
#
# Memory address 0 holds rval. Globals follow it, then the arrays.

RVAL = 0


class Resolver:

    def __init__(self, program):
        self.program = program
        self.globals = {"rval": ("global", RVAL)}
        self.procedures = {}
        self.memory_used = 1
        self.scope = None
        self.in_procedure = False

    def declare(self, table, token, meaning):
        if token.text in table:
            raise CompileError(f"'{token.text}' is declared twice", token)
        table[token.text] = meaning

    def resolve(self):
        p = self.program
        for name, value in p.consts:
            self.declare(self.globals, name, ("const", value))
        for name in p.globals:
            self.declare(self.globals, name, ("global", self.memory_used))
            self.memory_used += 1
        for name, size in p.arrays:
            self.declare(self.globals, name, ("array", self.memory_used, size))
            self.memory_used += size
        if self.memory_used > 4096:
            raise CompileError("the arrays and variables do not fit in memory", p.token)
        # All procedures are declared before any body is resolved, so
        # a procedure can call itself, or one declared after it.
        for proc in p.procedures:
            self.declare(self.procedures, proc.name, ("procedure", proc))
            if proc.name.text in self.globals:
                raise CompileError(f"'{proc.name.text}' is already a variable", proc.name)
        for proc in p.procedures:
            self.scope = {}
            self.in_procedure = True
            for k, name in enumerate(proc.params + proc.locals):
                self.declare(self.scope, name, ("local", k))
            for name, value in proc.consts:
                self.declare(self.scope, name, ("const", value))
            self.statement(proc.body)
        self.scope = {}
        self.in_procedure = False
        self.statement(p.body)

    def lookup(self, token, name):
        if name in self.scope:
            return self.scope[name]
        if name in self.globals:
            return self.globals[name]
        if name in self.procedures:
            raise CompileError(f"'{name}' is a procedure, not a value", token)
        raise CompileError(f"'{name}' is not declared", token)

    def statement(self, node):
        kind = type(node)
        if kind is Assign:
            self.value(node.target, assigning=True)
            self.value(node.value)
        elif kind is Call:
            if node.name.text not in self.procedures:
                raise CompileError(f"there is no procedure '{node.name.text}'", node.name)
            proc = self.procedures[node.name.text][1]
            if len(node.args) != len(proc.params):
                raise CompileError(f"'{proc.name.text}' takes {len(proc.params)} "
                                   f"argument{'' if len(proc.params) == 1 else 's'}, "
                                   f"given {len(node.args)}", node.name)
            node.procedure = proc
            for arg in node.args:
                self.value(arg)
        elif kind is Block:
            for s in node.statements:
                self.statement(s)
        elif kind is If:
            self.value(node.condition)
            self.statement(node.then)
            if node.otherwise:
                self.statement(node.otherwise)
        elif kind in (While, DoWhile):
            self.value(node.condition)
            self.statement(node.body)
        elif kind is Return:
            node.in_procedure = self.in_procedure
            if node.value:
                self.value(node.value)
        elif kind in (Print, Emit):
            self.value(node.value)

    def value(self, node, assigning=False):
        kind = type(node)
        if kind is Name:
            node.meaning = self.lookup(node.token, node.name)
            what = node.meaning[0]
            if what == "array":
                raise CompileError(f"'{node.name}' is an array: say which element, "
                                   f"as in {node.name}.0", node.token)
            if assigning and what == "const":
                raise CompileError(f"'{node.name}' is a constant and cannot be changed", node.token)
        elif kind is Element:
            node.meaning = self.lookup(node.token, node.name)
            if node.meaning[0] != "array":
                raise CompileError(f"'{node.name}' is not an array", node.token)
            self.value(node.index)
            if type(node.index) is Number and not 0 <= node.index.value < node.meaning[2]:
                raise CompileError(f"'{node.name}' has elements 0 to {node.meaning[2] - 1}, "
                                   f"not {node.index.value}", node.index.token)
        elif kind in (Binary, Compare):
            self.value(node.left)
            self.value(node.right)
        elif kind is Negate:
            self.value(node.operand)


# Stage 4: generating code.

OPCODES = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD",
           "and": "AND", "or": "OR", "xor": "XOR"}

# a op b, for each comparison, from LT and EQ alone.
COMPARISONS = {
    "=": ["EQ"],
    "#": ["EQ", "PUSH 0", "EQ"],                 # not (a = b)
    "<": ["LT"],
    ">": ["SWAP", "LT"],                         # b < a
    "<=": ["SWAP", "LT", "PUSH 0", "EQ"],        # not (b < a)
    ">=": ["LT", "PUSH 0", "EQ"],                # not (a < b)
}


class Generator:

    def __init__(self, source_lines):
        self.out = []
        self.labels = 0
        self.source_lines = source_lines
        self.last_line = None

    def emit(self, instruction):
        self.out.append(f"        {instruction}")

    def label(self, name):
        self.out.append(f"{name}:")

    def new_label(self):
        self.labels += 1
        return f"L{self.labels}"

    def note(self, token):
        """Put the source line in the assembly as a comment, once."""
        if token.line != self.last_line and token.line <= len(self.source_lines):
            self.last_line = token.line
            self.out.append(f"; {token.line}: {self.source_lines[token.line - 1].strip()}")

    def program(self, p):
        self.label("main")
        self.statement(p.body)
        self.emit("HALT")
        for proc in p.procedures:
            self.out.append("")
            self.out.append(f"; procedure {proc.name.text}")
            self.label("p_" + proc.name.text)
            for _ in proc.locals:
                self.emit("PUSH 0")
            self.statement(proc.body)
            self.emit("PUSH 0")
            self.emit("RET")
        return "\n".join(self.out) + "\n"

    def statement(self, node):
        kind = type(node)
        if kind is not Block and kind is not Empty:
            self.note(node.token)
        if kind is Assign:
            self.assign(node.target, node.value)
        elif kind is Call:
            for arg in node.args:
                self.value(arg)
            self.emit(f"CALL p_{node.procedure.name.text} {len(node.args)}")
            self.emit("DROP")
        elif kind is Block:
            for s in node.statements:
                self.statement(s)
        elif kind is If:
            otherwise, done = self.new_label(), self.new_label()
            self.value(node.condition)
            self.emit(f"JZ {otherwise}")
            self.statement(node.then)
            if node.otherwise:
                self.emit(f"JMP {done}")
                self.label(otherwise)
                self.statement(node.otherwise)
                self.label(done)
            else:
                self.label(otherwise)
        elif kind is While:
            top, done = self.new_label(), self.new_label()
            self.label(top)
            self.value(node.condition)
            self.emit(f"JZ {done}")
            self.statement(node.body)
            self.emit(f"JMP {top}")
            self.label(done)
        elif kind is DoWhile:
            top = self.new_label()
            self.label(top)
            self.statement(node.body)
            self.value(node.condition)
            self.emit("PUSH 0")
            self.emit("EQ")
            self.emit(f"JZ {top}")
        elif kind is Return:
            if node.value:
                # Only a return with a value sets rval.
                self.emit(f"PUSH {RVAL}")
                self.value(node.value)
                self.emit("STOREM")
            if node.in_procedure:
                self.emit("PUSH 0")
                self.emit("RET")
            else:
                self.emit("HALT")
        elif kind is Print:
            self.value(node.value)
            self.emit("PRINT")
        elif kind is Emit:
            self.value(node.value)
            self.emit("EMIT")

    def assign(self, target, value):
        meaning = target.meaning
        if meaning[0] == "local":
            self.value(value)
            self.emit(f"STORE {meaning[1]}")
        elif meaning[0] == "global":
            self.emit(f"PUSH {meaning[1]}")
            self.value(value)
            self.emit("STOREM")
        else:
            self.address(target)
            self.value(value)
            self.emit("STOREM")

    def address(self, element):
        """Leave the memory address of an array element on the stack."""
        base = element.meaning[1]
        if type(element.index) is Number:
            self.emit(f"PUSH {base + element.index.value}")
        else:
            self.emit(f"PUSH {base}")
            self.value(element.index)
            self.emit("ADD")

    def value(self, node):
        kind = type(node)
        if kind is Number:
            self.emit(f"PUSH {node.value}")
        elif kind is Name:
            meaning = node.meaning
            if meaning[0] == "const":
                self.emit(f"PUSH {meaning[1]}")
            elif meaning[0] == "local":
                self.emit(f"LOAD {meaning[1]}")
            else:
                self.emit(f"PUSH {meaning[1]}")
                self.emit("LOADM")
        elif kind is Element:
            self.address(node)
            self.emit("LOADM")
        elif kind is Negate:
            self.emit("PUSH 0")
            self.value(node.operand)
            self.emit("SUB")
        elif kind is Binary:
            self.value(node.left)
            self.value(node.right)
            self.emit(OPCODES[node.op])
        elif kind is Compare:
            self.value(node.left)
            self.value(node.right)
            for instruction in COMPARISONS[node.op]:
                self.emit(instruction)


def show_tree(node, indent=""):
    """The syntax tree as indented text, for -tree."""
    lines = []
    if isinstance(node, Node):
        fields = {k: v for k, v in node.__dict__.items() if k != "token"}
        simple = {k: v for k, v in fields.items() if not isinstance(v, (Node, list, tuple))}
        label = type(node).__name__ + "".join(f" {k}={v!r}" for k, v in simple.items())
        lines.append(indent + label)
        for k, v in fields.items():
            if isinstance(v, Node):
                lines += show_tree(v, indent + "  ")
            elif isinstance(v, list):
                for item in v:
                    lines += show_tree(item, indent + "  ")
    elif isinstance(node, Token):
        lines.append(indent + node.text)
    elif isinstance(node, tuple):
        lines.append(indent + " ".join(x.text if isinstance(x, Token) else str(x) for x in node))
    return lines


def report(path, text, error):
    lines = text.splitlines()
    source = lines[error.line - 1] if 0 < error.line <= len(lines) else ""
    print(f"{path}:{error.line}:{error.col}: {error}", file=sys.stderr)
    print(f"    {source.expandtabs(4)}", file=sys.stderr)
    column = len(source[:error.col - 1].expandtabs(4))
    print(f"    {' ' * column}^", file=sys.stderr)


def main():
    args = sys.argv[1:]
    mode = args.pop(0) if args and args[0] in ("-tokens", "-tree") else None
    if len(args) != 1:
        sys.exit("usage: enkel.py [-tokens | -tree] program.p")
    path = args[0]
    with open(path) as f:
        text = f.read()
    try:
        tokens = scan(text)
        if mode == "-tokens":
            for token in tokens:
                print(token)
            return
        program = Parser(tokens).program()
        if mode == "-tree":
            print("\n".join(show_tree(program)))
            return
        Resolver(program).resolve()
        sys.stdout.write(Generator(text.splitlines()).program(program))
    except CompileError as error:
        report(path, text, error)
        sys.exit(1)


if __name__ == "__main__":
    main()
