#!/usr/bin/env python3
"""
A compiler for pascal/0, a small Pascal, to P4 code.

pascal/0 is the part of Pascal that the P4 machine shows best:
integers, booleans and characters, arrays, and procedures and functions
nested in each other, with value and var parameters:

    program squares(output);
    var i: integer;

        function square(x: integer): integer;
        begin
            square := x * x
        end;

    begin
        for i := 1 to 5 do
            writeln(i:2, square(i):4)
    end.

The language is in LANG.md. Every pascal/0 program is a Pascal program,
and does the same with any Pascal compiler.

Chapter 10's compiler for enkel/0 works in stages: it reads the whole
program into a tree, then resolves it, then writes code. This one works
as Wirth's compilers did, PL/0's and P4's among them: in one pass. It
reads a little, and at once writes the code for it. That is why, in
Pascal, everything must be declared before it is used, and why the size
of a frame is given by a label (ent 1 l5) whose value (l5=7) only comes
after the code that needed it.

    usage: pascal.py [-tokens] program.pas
"""

import sys


class CompileError(Exception):

    def __init__(self, message, token):
        super().__init__(message)
        self.line = token.line
        self.col = token.col


# Scanning.

KEYWORDS = {
    "and", "array", "begin", "case", "const", "div", "do", "downto",
    "else", "end", "for", "function", "if", "mod", "not", "of", "or",
    "procedure", "program", "repeat", "then", "to", "type", "until",
    "var", "while",
}

SYMBOLS = [":=", "..", "<=", ">=", "<>", "+", "-", "*", "(", ")", "[",
           "]", ",", ";", ":", ".", "=", "<", ">"]


class Token:

    def __init__(self, kind, text, line, col):
        self.kind = kind        # "name", "number", "string", a keyword, a symbol, or "end of file"
        self.text = text
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.line}:{self.col}  {self.kind:<10} {self.text!r}"


def scan(text):
    tokens = []
    i, line, col = 0, 1, 1

    def advance(n):
        nonlocal i, line, col
        for c in text[i:i + n]:
            if c == "\n":
                line, col = line + 1, 1
            else:
                col += 1
        i += n

    while i < len(text):
        c = text[i]
        if c in " \t\r\n":
            advance(1)
        elif c == "{" or text.startswith("(*", i):
            start = Token("comment", "", line, col)
            close = "}" if c == "{" else "*)"
            end = text.find(close, i)
            if end < 0:
                raise CompileError("this comment never ends", start)
            advance(end + len(close) - i)
        elif c.isalpha():
            j = i
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j].lower()    # Pascal ignores case in names
            tokens.append(Token(word if word in KEYWORDS else "name", word, line, col))
            advance(j - i)
        elif c.isdigit():
            j = i
            while j < len(text) and text[j].isdigit():
                j += 1
            tokens.append(Token("number", text[i:j], line, col))
            advance(j - i)
        elif c == "'":
            token = Token("string", "", line, col)
            j, value = i + 1, ""
            while True:
                if j >= len(text) or text[j] == "\n":
                    raise CompileError("this string never ends", token)
                if text[j] == "'":
                    if text.startswith("''", j):
                        value, j = value + "'", j + 2
                        continue
                    break
                value, j = value + text[j], j + 1
            if not value:
                raise CompileError("an empty string", token)
            token.text = value
            tokens.append(token)
            advance(j + 1 - i)
        else:
            for s in SYMBOLS:
                if text.startswith(s, i):
                    tokens.append(Token(s, s, line, col))
                    advance(len(s))
                    break
            else:
                raise CompileError(f"what is {c!r}?", Token("", c, line, col))
    tokens.append(Token("end of file", "", line, col))
    return tokens


# Types, and what names mean.

class Simple:

    def __init__(self, name, letter):
        self.name = name
        self.letter = letter    # the type letter of the instructions: lodi, lodb, lodc
        self.size = 1

    def __repr__(self):
        return self.name


INTEGER = Simple("integer", "i")
BOOLEAN = Simple("boolean", "b")
CHAR = Simple("char", "c")


class Array:

    def __init__(self, low, high, index, element):
        self.low, self.high = low, high     # the bounds, as numbers
        self.index = index                  # INTEGER or CHAR
        self.element = element
        self.size = (high - low + 1) * element.size
        self.letter = None

    def __repr__(self):
        return f"array [{self.low}..{self.high}] of {self.element}"


def a(type):
    """A type's name, with "a" or "an" before it."""
    return ("an " if str(type)[0] in "aeiou" else "a ") + str(type)


class Const:
    def __init__(self, type, value):
        self.type, self.value = type, value


class Var:
    def __init__(self, type, level, offset, by_reference=False):
        self.type, self.level, self.offset = type, level, offset
        self.by_reference = by_reference    # a var parameter: the word holds an address


class Proc:
    def __init__(self, name, level, label, result=None):
        self.name = name
        self.level = level          # where it is declared; its own variables are one deeper
        self.label = label
        self.params = []            # (type, by_reference)
        self.result = result        # the type of a function's result, or None


class TypeName:
    def __init__(self, type):
        self.type = type


class Scope:

    def __init__(self, outer):
        self.outer = outer
        self.names = {}

    def declare(self, token, meaning):
        if token.text in self.names:
            raise CompileError(f"'{token.text}' is declared twice here", token)
        self.names[token.text] = meaning

    def find(self, name):
        scope = self
        while scope:
            if name in scope.names:
                return scope.names[name]
            scope = scope.outer
        return None


MAXINT = 2147483647
STANDARD_FUNCTIONS = {"abs", "sqr", "odd", "ord", "chr", "succ", "pred", "eoln", "eof"}
STANDARD_PROCEDURES = {"write", "writeln", "read", "readln"}
INPUT, OUTPUT = 5, 6
WIDTH = {INTEGER: 11, BOOLEAN: 5, CHAR: 1}   # as Free Pascal writes them in ISO mode
STRING = 16                                     # the length of a string in lca


class Frame:
    """What the compiler keeps for the procedure whose code it writes now."""

    def __init__(self, level, start, proc=None, outer=None):
        self.level = level
        self.size = start           # the next free word of the frame
        self.depth = 0              # how deep the stack is now, above the variables
        self.deepest = 0
        self.proc = proc
        self.outer = outer          # the frame of the procedure this one is declared in


# The compiler.

class Compiler:

    def __init__(self, tokens, lines):
        self.tokens = tokens
        self.pos = 0
        self.lines = lines
        self.last_line = None
        self.out = []
        self.labels = 0
        self.frame = None
        self.scope = Scope(None)
        for name, meaning in (("integer", TypeName(INTEGER)), ("boolean", TypeName(BOOLEAN)),
                              ("char", TypeName(CHAR)), ("true", Const(BOOLEAN, True)),
                              ("false", Const(BOOLEAN, False)), ("maxint", Const(INTEGER, MAXINT))):
            self.scope.names[name] = meaning

    # Reading tokens.

    def peek(self):
        return self.tokens[self.pos]

    def at(self, *kinds):
        return self.peek().kind in kinds

    def take(self, kind):
        token = self.peek()
        if token.kind != kind:
            found = token.kind if token.kind in ("name", "number", "string", "end of file") else f"'{token.text}'"
            raise CompileError(f"expected {kind if kind in ('name', 'number') else repr(kind)}, found {found}", token)
        self.pos += 1
        return token

    def skip(self, kind):
        if self.at(kind):
            self.pos += 1
            return True
        return False

    # Writing code. Each instruction says how it changes the depth of
    # the stack, so the compiler knows the most a procedure needs, for
    # its ent 2.

    def emit(self, instruction, change):
        self.out.append(" " + instruction)
        f = self.frame
        f.depth += change
        f.deepest = max(f.deepest, f.depth)

    def new_label(self):
        self.labels += 1
        return self.labels

    def place(self, label, value=None):
        self.out.append(f"l {label}" if value is None else f"l {label}={value}")

    def note(self, token):
        """Put the source line in the code as a comment, once."""
        if token.line != self.last_line and token.line <= len(self.lines):
            self.last_line = token.line
            self.out.append(f"i {token.line:3}: {self.lines[token.line - 1].strip()}")

    # Declarations.

    def program(self):
        self.take("program")
        self.take("name")
        if self.skip("("):
            self.take("name")
            while self.skip(","):
                self.take("name")
            self.take(")")
        self.take(";")
        main = self.new_label()
        # The main program's variables follow the files, at 9.
        self.block(Frame(1, 9), main)
        self.take(".")
        self.take("end of file")
        self.out += ["q", " mst 0", f" cup 0 l {main}", " stp", "q"]
        return "\n".join(self.out) + "\n"

    def block(self, frame, entry, params=()):
        self.scope = Scope(self.scope)
        for name, var in params:
            self.scope.declare(name, var)
        outer, self.frame = self.frame, frame
        if self.skip("const"):
            while self.at("name"):
                name = self.take("name")
                self.take("=")
                self.scope.declare(name, self.constant())
                self.take(";")
        if self.skip("type"):
            while self.at("name"):
                name = self.take("name")
                self.take("=")
                self.scope.declare(name, TypeName(self.type()))
                self.take(";")
        if self.skip("var"):
            while self.at("name"):
                names = [self.take("name")]
                while self.skip(","):
                    names.append(self.take("name"))
                self.take(":")
                type = self.type()
                for name in names:
                    self.scope.declare(name, self.allocate(type))
                self.take(";")
        while self.at("procedure", "function"):
            self.procedure()
        if frame.level == 1 and frame.size > 13000:
            raise CompileError("the variables do not fit in the store", self.peek())
        size, room = self.new_label(), self.new_label()
        self.place(entry)
        self.emit(f"ent 1 l {size}", 0)
        self.emit(f"ent 2 l {room}", 0)
        self.compound()
        self.emit("ret" + (frame.proc.result.letter if frame.proc and frame.proc.result else "p"), 0)
        self.place(size, frame.size)
        self.place(room, frame.deepest)
        self.scope = self.scope.outer
        self.frame = outer

    def allocate(self, type):
        f = self.frame
        var = Var(type, f.level, f.size)
        f.size += type.size
        return var

    def constant(self):
        """A constant: a number, a character, or a constant's name, with a sign."""
        sign = -1 if self.skip("-") else 1
        if sign == 1:
            self.skip("+")
        token = self.peek()
        if self.skip("number"):
            value = int(token.text)
            if value > MAXINT:
                raise CompileError(f"{token.text} is more than maxint", token)
            return Const(INTEGER, sign * value)
        if self.skip("string"):
            if len(token.text) != 1:
                raise CompileError("a string constant must be one character", token)
            if sign == -1:
                raise CompileError("a character has no sign", token)
            return Const(CHAR, token.text)
        name = self.take("name")
        meaning = self.scope.find(name.text)
        if not isinstance(meaning, Const):
            raise CompileError(f"'{name.text}' is not a constant", name)
        if sign == -1 and meaning.type is not INTEGER:
            raise CompileError("only a number can have a sign", name)
        return Const(meaning.type, sign * meaning.value if sign == -1 else meaning.value)

    def type(self):
        token = self.peek()
        if self.skip("array"):
            self.take("[")
            bounds = [self.bounds()]
            while self.skip(","):
                bounds.append(self.bounds())
            self.take("]")
            self.take("of")
            type = self.type()
            for low, high, index in reversed(bounds):
                type = Array(low, high, index, type)
            return type
        name = self.take("name")
        meaning = self.scope.find(name.text)
        if not isinstance(meaning, TypeName):
            raise CompileError(f"'{name.text}' is not a type", token)
        return meaning.type

    def bounds(self):
        token = self.peek()
        low = self.constant()
        self.take("..")
        high = self.constant()
        if low.type is not high.type or low.type is BOOLEAN:
            raise CompileError("the bounds must be two numbers or two characters", token)
        lo, hi = (ord(low.value), ord(high.value)) if low.type is CHAR else (low.value, high.value)
        if lo > hi:
            raise CompileError("the lower bound is above the upper", token)
        return lo, hi, low.type

    def procedure(self):
        is_function = self.take(self.peek().kind).kind == "function"
        name = self.take("name")
        proc = Proc(name.text, self.frame.level, self.new_label())
        self.scope.declare(name, proc)
        frame = Frame(self.frame.level + 1, 5, proc, self.frame)
        params = []
        if self.skip("("):
            while True:
                by_reference = self.skip("var")
                names = [self.take("name")]
                while self.skip(","):
                    names.append(self.take("name"))
                self.take(":")
                token = self.peek()
                type = self.type_name()
                if isinstance(type, Array) and not by_reference:
                    raise CompileError("pascal/0 passes arrays only as var parameters", token)
                for n in names:
                    params.append((n, type, by_reference))
                if not self.skip(";"):
                    break
            self.take(")")
        if is_function:
            self.take(":")
            token = self.peek()
            proc.result = self.type_name()
            if isinstance(proc.result, Array):
                raise CompileError("a function returns a simple value", token)
        self.take(";")
        # The parameters are the first variables of the new frame, after
        # the five words of the mark.
        proc.params = [(type, by_reference) for _, type, by_reference in params]
        frame.size = 5 + len(params)
        self.block(frame, proc.label,
                   [(n, Var(type, frame.level, 5 + k, by_reference))
                    for k, (n, type, by_reference) in enumerate(params)])
        self.take(";")

    def type_name(self):
        name = self.take("name")
        meaning = self.scope.find(name.text)
        if not isinstance(meaning, TypeName):
            raise CompileError(f"'{name.text}' is not a type", name)
        return meaning.type

    # Statements.

    def compound(self):
        self.take("begin")
        self.statement()
        while self.skip(";"):
            self.statement()
        self.take("end")

    def statement(self):
        token = self.peek()
        if token.kind not in ("begin", "end", ";", "until", "else"):
            self.note(token)
        if token.kind == "begin":
            self.compound()
        elif token.kind == "if":
            self.pos += 1
            self.condition()
            otherwise, done = self.new_label(), self.new_label()
            self.take("then")
            self.emit(f"fjp l {otherwise}", -1)
            self.statement()
            if self.skip("else"):
                self.emit(f"ujp l {done}", 0)
                self.place(otherwise)
                self.statement()
                self.place(done)
            else:
                self.place(otherwise)
        elif token.kind == "while":
            self.pos += 1
            top, done = self.new_label(), self.new_label()
            self.place(top)
            self.condition()
            self.take("do")
            self.emit(f"fjp l {done}", -1)
            self.statement()
            self.emit(f"ujp l {top}", 0)
            self.place(done)
        elif token.kind == "repeat":
            self.pos += 1
            top = self.new_label()
            self.place(top)
            self.statement()
            while self.skip(";"):
                self.statement()
            self.take("until")
            self.condition()
            self.emit(f"fjp l {top}", -1)
        elif token.kind == "for":
            self.for_statement()
        elif token.kind == "case":
            self.case_statement()
        elif token.kind == "name":
            self.name_statement()
        # anything else is the empty statement

    def condition(self):
        token = self.peek()
        if self.expression() is not BOOLEAN:
            raise CompileError("a condition must be a boolean", token)

    def name_statement(self):
        token = self.peek()
        meaning = self.scope.find(token.text)
        if meaning is None and token.text in STANDARD_PROCEDURES:
            self.pos += 1
            return self.standard_procedure(token)
        if isinstance(meaning, Proc) and not self.peek_assign():
            self.pos += 1
            if meaning.result:
                raise CompileError(f"'{token.text}' is a function: use its value", token)
            return self.call(meaning, token)
        # An assignment: to a variable, or to the function's result.
        if isinstance(meaning, Proc):
            self.pos += 1
            self.function_result(meaning, token)
            return
        target = self.variable()
        self.take(":=")
        self.assign(target, token)

    def peek_assign(self):
        return self.tokens[self.pos + 1].kind == ":="

    def function_result(self, proc, token):
        """f := e, inside f: the result goes in word 0 of f's frame."""
        if not proc.result or not self.inside(proc):
            raise CompileError(f"'{token.text}' can be given a value only inside it", token)
        self.take(":=")
        value = self.peek()
        if self.expression() is not proc.result:
            raise CompileError(f"the result of '{proc.name}' is {a(proc.result)}", value)
        self.emit(f"str{proc.result.letter} {self.frame.level - (proc.level + 1)} 0", -1)

    def inside(self, proc):
        """Is the code being written now inside proc, or in a procedure
        declared inside it?"""
        f = self.frame
        while f and f.proc is not proc:
            f = f.outer
        return f is not None

    def assign(self, target, token):
        kind, type, var = target
        value = self.peek()
        if isinstance(type, Array):
            if kind == "direct":
                self.address(var)
            source = self.peek()
            if not source.kind == "name":
                raise CompileError("an array can only be given another array", source)
            other = self.variable()
            if other[1] is not type:
                raise CompileError(f"the array is {type}, not {other[1]}", source)
            if other[0] == "direct":
                self.address(other[2])
            self.emit(f"mov {type.size}", -2)
            return
        got = self.expression()
        if got is not type:
            raise CompileError(f"{a(type)} cannot be given {a(got)}", value)
        if kind == "direct":
            self.store(var)
        else:
            self.emit(f"sto{type.letter}", -2)

    def for_statement(self):
        self.take("for")
        token = self.take("name")
        var = self.scope.find(token.text)
        if not isinstance(var, Var) or var.by_reference or var.type not in (INTEGER, CHAR):
            raise CompileError("a for loop needs a local integer or char variable", token)
        self.take(":=")
        start = self.peek()
        if self.expression() is not var.type:
            raise CompileError(f"the loop starts at {a(var.type)}", start)
        self.store(var)
        down = self.take(self.peek().kind if self.at("to", "downto") else "to").kind == "downto"
        end = self.peek()
        if self.expression() is not var.type:
            raise CompileError(f"the loop ends at {a(var.type)}", end)
        limit = self.allocate(var.type)     # the end is computed once, and kept here
        self.store(limit)
        self.take("do")
        top, done = self.new_label(), self.new_label()
        t = var.type.letter
        self.place(top)
        self.load(var)
        self.load(limit)
        self.emit(("geq" if down else "leq") + t, -1)
        self.emit(f"fjp l {done}", -1)
        self.statement()
        self.load(var)
        self.step(var.type, -1 if down else 1)
        self.store(var)
        self.emit(f"ujp l {top}", 0)
        self.place(done)

    def step(self, type, by):
        op = "inci" if by > 0 else "deci"
        if type is CHAR:
            self.emit("ord", 0)
            self.emit(f"{op} 1", 0)
            self.emit("chr", 0)
        else:
            self.emit(f"{op} 1", 0)

    def case_statement(self):
        """As P4 did it: the value is on the stack, the branches follow,
        and after them a jump through a table, one entry per value."""
        token = self.take("case")
        type = self.expression()
        if type not in (INTEGER, CHAR):
            raise CompileError("case needs an integer or a char", token)
        if type is CHAR:
            self.emit("ord", 0)
        self.take("of")
        test, done = self.new_label(), self.new_label()
        self.emit(f"ujp l {test}", 0)
        branches = {}
        while True:
            branch = self.new_label()
            while True:
                label = self.peek()
                c = self.constant()
                if c.type is not type:
                    raise CompileError(f"a case label here is {a(type)}", label)
                value = ord(c.value) if type is CHAR else c.value
                if value in branches:
                    raise CompileError("this case label is used twice", label)
                branches[value] = branch
                if not self.skip(","):
                    break
            self.take(":")
            self.place(branch)
            self.statement()
            self.emit(f"ujp l {done}", 0)
            if not self.skip(";") or self.at("end"):
                break
        self.take("end")
        low, high = min(branches), max(branches)
        if high - low > 1000:
            raise CompileError("the case labels are too far apart for a table", token)
        table = self.new_label()
        self.place(test)
        self.emit(f"chki {low} {high}", 0)
        if low:
            self.emit(f"deci {low}", 0)
        self.emit(f"xjp l {table}", -1)
        self.place(table)
        for v in range(low, high + 1):
            self.emit(f"ujp l {branches[v]}" if v in branches else "ujc", 0)
        self.place(done)

    # Procedures and functions.

    def call(self, proc, token):
        self.emit(f"mst {self.frame.level - proc.level}", 5)
        args = []
        if self.skip("("):
            args.append(self.peek())
            self.argument(proc, 0, args[0])
            while self.skip(","):
                args.append(self.peek())
                self.argument(proc, len(args) - 1, args[-1])
            self.take(")")
        if len(args) != len(proc.params):
            raise CompileError(f"'{proc.name}' takes {len(proc.params)} arguments, not {len(args)}", token)
        n = len(args)
        self.emit(f"cup {n} l {proc.label}", -(n + 5) + (1 if proc.result else 0))
        return proc.result

    def argument(self, proc, k, token):
        if k >= len(proc.params):
            raise CompileError(f"'{proc.name}' takes {len(proc.params)} arguments", token)
        type, by_reference = proc.params[k]
        if by_reference:
            if token.kind != "name" or not isinstance(self.scope.find(token.text), Var):
                raise CompileError("a var parameter needs a variable", token)
            kind, got, var = self.variable()
            if kind == "direct":
                self.address(var)
        else:
            got = self.expression()
        if got is not type:
            raise CompileError(f"argument {k + 1} of '{proc.name}' is {a(type)}, not {a(got)}", token)

    def standard_procedure(self, token):
        name = token.text
        if name in ("write", "writeln"):
            if self.skip("("):
                self.write_item()
                while self.skip(","):
                    self.write_item()
                self.take(")")
            if name == "writeln":
                self.emit(f"lao {OUTPUT}", 1)
                self.emit("csp wln", -1)
        else:
            if self.skip("("):
                self.read_item()
                while self.skip(","):
                    self.read_item()
                self.take(")")
            if name == "readln":
                self.emit(f"lao {INPUT}", 1)
                self.emit("csp rln", -1)

    def write_item(self):
        token = self.peek()
        if token.kind == "string" and len(token.text) > 1:
            self.pos += 1
            width = self.width()
            text = token.text
            if width and len(text) > STRING:
                raise CompileError(f"a width is only for strings up to {STRING} long", token)
            for k in range(0, len(text), STRING):
                self.write_string(text[k:k + STRING], width)
            return
        type = self.expression()
        width = self.width()
        if isinstance(type, Array):
            raise CompileError("write cannot write an array", token)
        if type is BOOLEAN:
            if width == "computed":
                raise CompileError("a boolean's width must be a number", token)
            # P4 cannot write a boolean, so the compiler writes a word.
            no, done = self.new_label(), self.new_label()
            self.emit(f"fjp l {no}", -1)
            self.write_string("true", width or WIDTH[BOOLEAN])
            self.emit(f"ujp l {done}", 0)
            self.place(no)
            self.write_string("false", width or WIDTH[BOOLEAN])
            self.place(done)
            return
        if width is None:
            self.emit(f"ldci {WIDTH[type]}", 1)
        elif width != "computed":
            self.emit(f"ldci {width}", 1)
        self.emit(f"lao {OUTPUT}", 1)
        self.emit("csp wri" if type is INTEGER else "csp wrc", -3)

    def width(self):
        """An optional :width: None if there is none, the number if it is
        one, or "computed" if it is an expression, now on the stack."""
        if not self.skip(":"):
            return None
        token = self.peek()
        if token.kind == "number" and self.tokens[self.pos + 1].kind in (",", ")"):
            self.pos += 1
            return int(token.text)
        if self.expression() is not INTEGER:
            raise CompileError("a width is an integer", token)
        return "computed"

    def write_string(self, text, width):
        if width == "computed":
            raise CompileError("a string's width must be a number", self.peek())
        self.emit(f"lca'{text.ljust(STRING)}'", 1)
        self.emit(f"ldci {width or len(text)}", 1)
        self.emit(f"ldci {len(text)}", 1)
        self.emit(f"lao {OUTPUT}", 1)
        self.emit("csp wrs", -4)

    def read_item(self):
        token = self.peek()
        if token.kind != "name" or not isinstance(self.scope.find(token.text), Var):
            raise CompileError("read needs a variable", token)
        kind, type, var = self.variable()
        if type not in (INTEGER, CHAR):
            raise CompileError("read reads integers and characters", token)
        if kind == "direct":
            self.address(var)
        self.emit(f"lao {INPUT}", 1)
        self.emit("csp rdi" if type is INTEGER else "csp rdc", -2)

    # Variables.

    def variable(self):
        """A variable, with any [index] after it. Returns ("direct", type,
        var) if no code has been written for it yet, or ("address",
        type, None) if its address is now on the stack."""
        token = self.take("name")
        var = self.scope.find(token.text)
        if not isinstance(var, Var):
            raise CompileError(f"'{token.text}' is not a variable", token)
        kind, type = "direct", var.type
        if var.by_reference:
            self.address(var)
            kind = "address"
        while self.at("["):
            open_ = self.take("[")
            while True:
                if not isinstance(type, Array):
                    raise CompileError(f"'{token.text}' has no more indexes", open_)
                if kind == "direct":
                    self.address(var)
                    kind = "address"
                index = self.peek()
                if self.expression() is not type.index:
                    raise CompileError(f"the index is {a(type.index)}", index)
                if type.index is CHAR:
                    self.emit("ord", 0)
                self.emit(f"chki {type.low} {type.high}", 0)
                if type.low:
                    self.emit(f"deci {type.low}", 0)
                self.emit(f"ixa {type.element.size}", -1)
                type = type.element
                if not self.skip(","):
                    break
            self.take("]")
        return kind, type, (var if kind == "direct" else None)

    def address(self, var):
        if var.by_reference:
            self.emit(f"loda {self.frame.level - var.level} {var.offset}", 1)
        elif var.level == 1:
            self.emit(f"lao {var.offset}", 1)
        else:
            self.emit(f"lda {self.frame.level - var.level} {var.offset}", 1)

    def load(self, var):
        t = var.type.letter
        if var.level == 1:
            self.emit(f"ldo{t} {var.offset}", 1)
        else:
            self.emit(f"lod{t} {self.frame.level - var.level} {var.offset}", 1)

    def store(self, var):
        t = var.type.letter
        if var.level == 1:
            self.emit(f"sro{t} {var.offset}", -1)
        else:
            self.emit(f"str{t} {self.frame.level - var.level} {var.offset}", -1)

    # Expressions. Each returns its type.

    def expression(self):
        left = self.simple_expression()
        token = self.peek()
        if token.kind in ("=", "<>", "<", "<=", ">", ">="):
            self.pos += 1
            right = self.simple_expression()
            if left is not right or isinstance(left, Array):
                raise CompileError(f"cannot compare {a(left)} with {a(right)}", token)
            op = {"=": "equ", "<>": "neq", "<": "les", "<=": "leq", ">": "grt", ">=": "geq"}[token.kind]
            self.emit(op + left.letter, -1)
            return BOOLEAN
        return left

    def simple_expression(self):
        token = self.peek()
        sign = self.skip("-") and "-" or (self.skip("+") and "+")
        type = self.term()
        if sign:
            self.expect(type, INTEGER, token)
            if sign == "-":
                self.emit("ngi", 0)
        while self.at("+", "-", "or"):
            op = self.take(self.peek().kind)
            right = self.term()
            want = BOOLEAN if op.kind == "or" else INTEGER
            self.expect(type, want, op)
            self.expect(right, want, op)
            self.emit({"+": "adi", "-": "sbi", "or": "ior"}[op.kind], -1)
        return type

    def term(self):
        type = self.factor()
        while self.at("*", "div", "mod", "and"):
            op = self.take(self.peek().kind)
            right = self.factor()
            want = BOOLEAN if op.kind == "and" else INTEGER
            self.expect(type, want, op)
            self.expect(right, want, op)
            self.emit({"*": "mpi", "div": "dvi", "mod": "mod", "and": "and"}[op.kind], -1)
        return type

    def expect(self, got, want, token):
        if got is not want:
            raise CompileError(f"'{token.text}' needs {a(want)}, not {a(got)}", token)

    def factor(self):
        token = self.peek()
        if self.skip("number"):
            value = int(token.text)
            if value > MAXINT:
                raise CompileError(f"{token.text} is more than maxint", token)
            self.emit(f"ldci {value}", 1)
            return INTEGER
        if self.skip("string"):
            if len(token.text) != 1:
                raise CompileError("a string can only be written, with write", token)
            self.char(token.text)
            return CHAR
        if self.skip("("):
            type = self.expression()
            self.take(")")
            return type
        if self.skip("not"):
            self.expect(self.factor(), BOOLEAN, token)
            self.emit("not", 0)
            return BOOLEAN
        if token.kind != "name":
            raise CompileError("expected a value", token)
        meaning = self.scope.find(token.text)
        if meaning is None and token.text in STANDARD_FUNCTIONS:
            self.pos += 1
            return self.standard_function(token)
        if isinstance(meaning, Const):
            self.pos += 1
            if meaning.type is INTEGER:
                self.emit(f"ldci {meaning.value}", 1)
            elif meaning.type is BOOLEAN:
                self.emit(f"ldcb {int(meaning.value)}", 1)
            else:
                self.char(meaning.value)
            return meaning.type
        if isinstance(meaning, Proc):
            self.pos += 1
            if not meaning.result:
                raise CompileError(f"'{token.text}' is a procedure, and has no value", token)
            return self.call(meaning, token)
        if meaning is None:
            raise CompileError(f"'{token.text}' is not declared", token)
        kind, type, var = self.variable()
        if isinstance(type, Array):
            raise CompileError("an array is not a value here", token)
        if kind == "direct":
            self.load(var)
        else:
            self.emit(f"ind{type.letter} 0", 0)
        return type

    def char(self, c):
        if c == "'" or not c.isprintable():
            self.emit(f"ldci {ord(c)}", 1)
            self.emit("chr", 0)
        else:
            self.emit(f"ldcc '{c}'", 1)

    def standard_function(self, token):
        name = token.text
        if name in ("eoln", "eof"):
            self.emit(f"lao {INPUT}", 1)
            self.emit("csp eln" if name == "eoln" else "eof", 0)
            return BOOLEAN
        self.take("(")
        arg = self.peek()
        type = self.expression()
        self.take(")")
        if name in ("abs", "sqr"):
            self.expect(type, INTEGER, arg)
            self.emit("abi" if name == "abs" else "sqi", 0)
            return INTEGER
        if name == "odd":
            self.expect(type, INTEGER, arg)
            self.emit("odd", 0)
            return BOOLEAN
        if name == "ord":
            if type not in (INTEGER, CHAR, BOOLEAN):
                raise CompileError("ord needs an integer, a char or a boolean", arg)
            self.emit("ord", 0)
            return INTEGER
        if name == "chr":
            self.expect(type, INTEGER, arg)
            self.emit("chr", 0)
            return CHAR
        if type not in (INTEGER, CHAR):         # succ and pred
            raise CompileError(f"{name} needs an integer or a char", arg)
        self.step(type, 1 if name == "succ" else -1)
        return type


def report(path, text, error):
    lines = text.splitlines()
    source = lines[error.line - 1] if 0 < error.line <= len(lines) else ""
    print(f"{path}:{error.line}:{error.col}: {error}", file=sys.stderr)
    print(f"    {source.expandtabs(4)}", file=sys.stderr)
    column = len(source[:error.col - 1].expandtabs(4))
    print(f"    {' ' * column}^", file=sys.stderr)


def main():
    args = sys.argv[1:]
    mode = args.pop(0) if args and args[0] == "-tokens" else None
    if len(args) != 1:
        sys.exit("usage: pascal.py [-tokens] program.pas")
    path = args[0]
    with open(path) as f:
        text = f.read()
    try:
        tokens = scan(text)
        if mode == "-tokens":
            for token in tokens:
                print(token)
            return
        sys.stdout.write(Compiler(tokens, text.splitlines()).program())
    except CompileError as error:
        report(path, text, error)
        sys.exit(1)


if __name__ == "__main__":
    main()
