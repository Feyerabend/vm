"""
A small Java Virtual Machine: enough to run static methods on ints,
arrays of ints, and printing.

It reads a .class file as javac wrote it: the constant pool, where
every name, string and reference to another class or method is kept,
and the methods, each with its bytecode, its number of local
variables, and the deepest its operand stack can get. Then it runs
main.

What is here: int arithmetic, local variables, comparisons and jumps,
calls of static methods in the same class, arrays of ints, string
constants, and System.out's print and println. What is not: objects,
fields, other types than int, exceptions that a program catches, and
the verifier. A division by zero ends the program as the real machine
does, with the same message and the same stack trace.

    python3 jvm.py [-c] Class.class
"""

import struct
import sys

# The instructions this machine knows, with the size of their operands.
OPCODES = {
    0x00: ("nop", 0), 0x02: ("iconst_m1", 0), 0x03: ("iconst_0", 0),
    0x04: ("iconst_1", 0), 0x05: ("iconst_2", 0), 0x06: ("iconst_3", 0),
    0x07: ("iconst_4", 0), 0x08: ("iconst_5", 0), 0x10: ("bipush", 1),
    0x11: ("sipush", 2), 0x12: ("ldc", 1), 0x15: ("iload", 1),
    0x19: ("aload", 1), 0x1A: ("iload_0", 0), 0x1B: ("iload_1", 0),
    0x1C: ("iload_2", 0), 0x1D: ("iload_3", 0), 0x2A: ("aload_0", 0),
    0x2B: ("aload_1", 0), 0x2C: ("aload_2", 0), 0x2D: ("aload_3", 0),
    0x2E: ("iaload", 0), 0x36: ("istore", 1), 0x3A: ("astore", 1),
    0x3B: ("istore_0", 0), 0x3C: ("istore_1", 0), 0x3D: ("istore_2", 0),
    0x3E: ("istore_3", 0), 0x4B: ("astore_0", 0), 0x4C: ("astore_1", 0),
    0x4D: ("astore_2", 0), 0x4E: ("astore_3", 0), 0x4F: ("iastore", 0),
    0x57: ("pop", 0), 0x59: ("dup", 0), 0x60: ("iadd", 0),
    0x64: ("isub", 0), 0x68: ("imul", 0), 0x6C: ("idiv", 0),
    0x70: ("irem", 0), 0x74: ("ineg", 0), 0x84: ("iinc", 2),
    0x99: ("ifeq", 2), 0x9A: ("ifne", 2), 0x9B: ("iflt", 2),
    0x9C: ("ifge", 2), 0x9D: ("ifgt", 2), 0x9E: ("ifle", 2),
    0x9F: ("if_icmpeq", 2), 0xA0: ("if_icmpne", 2), 0xA1: ("if_icmplt", 2),
    0xA2: ("if_icmpge", 2), 0xA3: ("if_icmpgt", 2), 0xA4: ("if_icmple", 2),
    0xA7: ("goto", 2), 0xAC: ("ireturn", 0), 0xB1: ("return", 0),
    0xB2: ("getstatic", 2), 0xB6: ("invokevirtual", 2),
    0xB7: ("invokespecial", 2), 0xB8: ("invokestatic", 2), 0xBC: ("newarray", 1), 0xBE: ("arraylength", 0),
}

BRANCHES = {
    "ifeq": lambda v: v == 0, "ifne": lambda v: v != 0,
    "iflt": lambda v: v < 0, "ifge": lambda v: v >= 0,
    "ifgt": lambda v: v > 0, "ifle": lambda v: v <= 0,
}
COMPARES = {
    "if_icmpeq": lambda a, b: a == b, "if_icmpne": lambda a, b: a != b,
    "if_icmplt": lambda a, b: a < b, "if_icmpge": lambda a, b: a >= b,
    "if_icmpgt": lambda a, b: a > b, "if_icmple": lambda a, b: a <= b,
}


class Error(Exception):
    pass


class JavaException(Exception):
    """An exception the program does not catch: it unwinds every frame,
    and each adds a line to the stack trace."""

    def __init__(self, name, message):
        super().__init__(message)
        self.name = name
        self.message = message
        self.trace = []


def to_int(v):
    """Wrap to a 32-bit int, as Java's int arithmetic does."""
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v & 0x80000000 else v


class Reader:

    def __init__(self, data):
        self.data = data
        self.at = 0

    def take(self, fmt):
        values = struct.unpack_from(">" + fmt, self.data, self.at)
        self.at += struct.calcsize(">" + fmt)
        return values[0] if len(values) == 1 else values

    def bytes(self, n):
        b = self.data[self.at:self.at + n]
        self.at += n
        return b


class Method:

    def __init__(self, name, descriptor, flags):
        self.name = name
        self.descriptor = descriptor
        self.flags = flags
        self.code = b""
        self.max_stack = 0
        self.max_locals = 0
        self.lines = []             # (bytecode offset, source line)

    def line_at(self, pc):
        line = None
        for start, number in self.lines:
            if start <= pc:
                line = number
        return line


class ClassFile:
    """The parts of a class file this machine uses."""

    def __init__(self, data):
        r = Reader(data)
        if r.take("I") != 0xCAFEBABE:
            raise Error("not a class file")
        self.minor, self.major = r.take("HH")
        self.pool = [None]
        count = r.take("H")
        while len(self.pool) < count:
            tag = r.take("B")
            if tag == 1:
                self.pool.append(("Utf8", r.bytes(r.take("H")).decode("utf-8", "replace")))
            elif tag in (3, 4):
                self.pool.append(("Integer" if tag == 3 else "Float", r.take("i" if tag == 3 else "f")))
            elif tag in (5, 6):
                self.pool.append(("Long" if tag == 5 else "Double", r.take("q" if tag == 5 else "d")))
                self.pool.append(None)      # these take two places
            elif tag in (7, 8, 16, 19, 20):
                kind = {7: "Class", 8: "String", 16: "MethodType", 19: "Module", 20: "Package"}[tag]
                self.pool.append((kind, r.take("H")))
            elif tag in (9, 10, 11, 12, 17, 18):
                kind = {9: "Fieldref", 10: "Methodref", 11: "InterfaceMethodref",
                        12: "NameAndType", 17: "Dynamic", 18: "InvokeDynamic"}[tag]
                self.pool.append((kind, r.take("HH")))
            elif tag == 15:
                self.pool.append(("MethodHandle", r.take("BH")))
            else:
                raise Error(f"unknown constant pool tag {tag}")
        self.flags, this, self.super = r.take("HHH")
        self.name = self.class_name(this)
        r.bytes(2 * r.take("H"))                    # interfaces
        for _ in range(r.take("H")):                # fields
            r.take("HHH")
            self.skip_attributes(r)
        self.methods = {}
        for _ in range(r.take("H")):
            flags, name, descriptor = r.take("HHH")
            m = Method(self.utf8(name), self.utf8(descriptor), flags)
            for _ in range(r.take("H")):
                attribute, length = r.take("HI")
                body = Reader(r.bytes(length))
                if self.utf8(attribute) == "Code":
                    m.max_stack, m.max_locals = body.take("HH")
                    m.code = body.bytes(body.take("I"))
                    body.bytes(8 * body.take("H"))  # exception table
                    for _ in range(body.take("H")):
                        inner, size = body.take("HI")
                        data = Reader(body.bytes(size))
                        if self.utf8(inner) == "LineNumberTable":
                            m.lines = [data.take("HH") for _ in range(data.take("H"))]
            self.methods[(m.name, m.descriptor)] = m
        self.source = None
        for _ in range(r.take("H")):
            attribute, length = r.take("HI")
            body = Reader(r.bytes(length))
            if self.utf8(attribute) == "SourceFile":
                self.source = self.utf8(body.take("H"))

    def skip_attributes(self, r):
        for _ in range(r.take("H")):
            r.take("H")
            r.bytes(r.take("I"))

    def utf8(self, i):
        kind, value = self.pool[i]
        if kind != "Utf8":
            raise Error(f"constant {i} is {kind}, not Utf8")
        return value

    def class_name(self, i):
        return self.utf8(self.pool[i][1])

    def member(self, i):
        """A Fieldref or Methodref: (class, name, descriptor)."""
        kind, (cls, nat) = self.pool[i]
        _, (name, descriptor) = self.pool[nat]
        return self.class_name(cls), self.utf8(name), self.utf8(descriptor)

    def constant(self, i):
        """What ldc pushes."""
        kind, value = self.pool[i]
        if kind == "Integer":
            return value
        if kind == "String":
            return self.utf8(value)
        raise Error(f"ldc of a {kind} is not supported")


def arguments(descriptor):
    """How many arguments a method takes: "(II)I" takes two."""
    inside = descriptor[1:descriptor.index(")")]
    count, i = 0, 0
    while i < len(inside):
        while inside[i] == "[":
            i += 1
        if inside[i] == "L":
            i = inside.index(";", i)
        i += 1
        count += 1
    return count


class PrintStream:
    pass


OUT = PrintStream()


class Machine:

    def __init__(self, cls):
        self.cls = cls
        self.depth = 0

    def invoke(self, method, args):
        if not method.code:
            raise Error(f"{method.name} has no code")
        self.depth += 1
        if self.depth > 2000:
            raise JavaException("java.lang.StackOverflowError", None)
        locals_ = list(args) + [None] * (method.max_locals - len(args))
        stack = []
        code = method.code
        pc = 0
        try:
            while True:
                at = pc
                op = code[pc]
                if op not in OPCODES:
                    raise Error(f"instruction {op:#04x} at {at} in {method.name} is not supported")
                name, size = OPCODES[op]
                pc += 1 + size
                if name.startswith("iconst_"):
                    stack.append(-1 if name == "iconst_m1" else int(name[7:]))
                elif name == "bipush":
                    stack.append(struct.unpack_from(">b", code, at + 1)[0])
                elif name == "sipush":
                    stack.append(struct.unpack_from(">h", code, at + 1)[0])
                elif name == "ldc":
                    stack.append(self.cls.constant(code[at + 1]))
                elif name in ("iload", "aload"):
                    stack.append(locals_[code[at + 1]])
                elif name[1:6] == "load_":
                    stack.append(locals_[int(name[6:])])
                elif name in ("istore", "astore"):
                    locals_[code[at + 1]] = stack.pop()
                elif name[1:7] == "store_":
                    locals_[int(name[7:])] = stack.pop()
                elif name == "iinc":
                    k = code[at + 1]
                    locals_[k] = to_int(locals_[k] + struct.unpack_from(">b", code, at + 2)[0])
                elif name in ("iadd", "isub", "imul", "idiv", "irem"):
                    b, a = stack.pop(), stack.pop()
                    if name in ("idiv", "irem") and b == 0:
                        raise JavaException("java.lang.ArithmeticException", "/ by zero")
                    if name == "iadd":
                        stack.append(to_int(a + b))
                    elif name == "isub":
                        stack.append(to_int(a - b))
                    elif name == "imul":
                        stack.append(to_int(a * b))
                    else:
                        q = abs(a) // abs(b)            # rounds towards zero
                        q = q if (a < 0) == (b < 0) else -q
                        stack.append(to_int(q) if name == "idiv" else to_int(a - q * b))
                elif name == "ineg":
                    stack.append(to_int(-stack.pop()))
                elif name == "pop":
                    stack.pop()
                elif name == "dup":
                    stack.append(stack[-1])
                elif name in BRANCHES:
                    if BRANCHES[name](stack.pop()):
                        pc = at + struct.unpack_from(">h", code, at + 1)[0]
                elif name in COMPARES:
                    b, a = stack.pop(), stack.pop()
                    if COMPARES[name](a, b):
                        pc = at + struct.unpack_from(">h", code, at + 1)[0]
                elif name == "goto":
                    pc = at + struct.unpack_from(">h", code, at + 1)[0]
                elif name == "newarray":
                    n = stack.pop()
                    if code[at + 1] != 10:
                        raise Error("only arrays of int are supported")
                    if n < 0:
                        raise JavaException("java.lang.NegativeArraySizeException", str(n))
                    stack.append([0] * n)
                elif name == "arraylength":
                    stack.append(len(self.array(stack.pop())))
                elif name == "iaload":
                    i, a = stack.pop(), self.array(stack.pop())
                    self.index(a, i)
                    stack.append(a[i])
                elif name == "iastore":
                    v, i, a = stack.pop(), stack.pop(), self.array(stack.pop())
                    self.index(a, i)
                    a[i] = v
                elif name == "getstatic":
                    member = self.cls.member(struct.unpack_from(">H", code, at + 1)[0])
                    if member != ("java/lang/System", "out", "Ljava/io/PrintStream;"):
                        raise Error(f"getstatic {'.'.join(member[:2])} is not supported")
                    stack.append(OUT)
                elif name == "invokevirtual":
                    self.virtual(self.cls.member(struct.unpack_from(">H", code, at + 1)[0]), stack)
                elif name == "invokestatic":
                    cls, mname, descriptor = self.cls.member(struct.unpack_from(">H", code, at + 1)[0])
                    if cls != self.cls.name or (mname, descriptor) not in self.cls.methods:
                        raise Error(f"{cls}.{mname}{descriptor} is not supported")
                    n = arguments(descriptor)
                    args = stack[len(stack) - n:]
                    del stack[len(stack) - n:]
                    result = self.invoke(self.cls.methods[(mname, descriptor)], args)
                    if not descriptor.endswith("V"):
                        stack.append(result)
                elif name == "invokespecial":
                    raise Error("objects are not supported (invokespecial)")
                elif name == "ireturn":
                    return stack.pop()
                elif name == "return":
                    return None
                if len(stack) > method.max_stack:
                    raise Error(f"{method.name} went past its max_stack of {method.max_stack}")
        except JavaException as e:
            line = method.line_at(at)
            where = f"{self.cls.source}:{line}" if line is not None else "Unknown Source"
            e.trace.append(f"{self.cls.name.replace('/', '.')}.{method.name}({where})")
            raise
        finally:
            self.depth -= 1

    def array(self, a):
        if a is None:
            raise JavaException("java.lang.NullPointerException", None)
        return a

    def index(self, a, i):
        if not 0 <= i < len(a):
            raise JavaException("java.lang.ArrayIndexOutOfBoundsException",
                                f"Index {i} out of bounds for length {len(a)}")

    def virtual(self, member, stack):
        cls, name, descriptor = member
        if cls != "java/io/PrintStream" or name not in ("print", "println"):
            raise Error(f"{cls}.{name} is not supported")
        n = arguments(descriptor)
        value = stack.pop() if n else None
        if stack.pop() is not OUT:
            raise Error(f"{name} on something that is not System.out")
        if descriptor == "(C)V":
            text = chr(value)
        elif descriptor in ("(I)V", "(Ljava/lang/String;)V"):
            text = str(value)
        elif descriptor == "()V":
            text = ""
        else:
            raise Error(f"PrintStream.{name}{descriptor} is not supported")
        sys.stdout.write(text + ("\n" if name == "println" else ""))


def disassemble(cls):
    """The bytecode of every method, much as javap -c shows it."""
    for m in cls.methods.values():
        print(f"{m.name}{m.descriptor}: max_stack {m.max_stack}, max_locals {m.max_locals}")
        pc = 0
        while pc < len(m.code):
            op = m.code[pc]
            name, size = OPCODES.get(op, (f"?{op:#04x}", 0))
            text = name
            if name in BRANCHES or name in COMPARES or name == "goto":
                text += f" {pc + struct.unpack_from('>h', m.code, pc + 1)[0]}"
            elif name in ("getstatic", "invokevirtual", "invokespecial", "invokestatic"):
                c, n, d = cls.member(struct.unpack_from(">H", m.code, pc + 1)[0])
                text += f" {c}.{n}:{d}"
            elif name == "ldc":
                text += f" {cls.constant(m.code[pc + 1])!r}"
            elif name == "bipush":
                text += f" {struct.unpack_from('>b', m.code, pc + 1)[0]}"
            elif name == "sipush":
                text += f" {struct.unpack_from('>h', m.code, pc + 1)[0]}"
            elif name == "iinc":
                text += f" {m.code[pc + 1]}, {struct.unpack_from('>b', m.code, pc + 2)[0]}"
            elif size:
                text += " " + " ".join(str(b) for b in m.code[pc + 1:pc + 1 + size])
            print(f"  {pc:4}  {text}")
            pc += 1 + size
        print()


def main(args):
    listing = "-c" in args
    args = [a for a in args if a != "-c"]
    if len(args) != 1:
        sys.exit("usage: jvm.py [-c] Class.class")
    try:
        with open(args[0], "rb") as f:
            cls = ClassFile(f.read())
        if listing:
            disassemble(cls)
            return
        main_method = cls.methods.get(("main", "([Ljava/lang/String;)V"))
        if main_method is None:
            raise Error(f"{cls.name} has no main method")
        Machine(cls).invoke(main_method, [[]])
    except JavaException as e:
        sys.stdout.flush()
        message = f": {e.message}" if e.message is not None else ""
        print(f'Exception in thread "main" {e.name}{message}', file=sys.stderr)
        for line in e.trace:
            print(f"\tat {line}", file=sys.stderr)
        sys.exit(1)
    except (Error, struct.error, IndexError) as e:
        sys.exit(f"jvm: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
