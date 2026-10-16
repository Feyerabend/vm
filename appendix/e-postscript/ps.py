"""
A small PostScript: the stack machine inside a printer (Adobe, 1984).

A PostScript program is a stream of tokens. Numbers, strings, literal
names (/name) and procedures ({ ... }) are pushed on the operand
stack. Any other name is looked up in the dictionary stack, and what
it names is executed: an operator, or a procedure. "def" puts a name
in a dictionary; that is all a variable or a function is.

The painting operators build a path (moveto, lineto, arc, closepath)
in the coordinates of the current transformation (translate, rotate,
scale), and stroke or fill it. Here the paint goes to an SVG file
instead of paper. The size of the page is taken from a
"%%BoundingBox: 0 0 width height" comment, as printers did.

    python3 ps.py program.ps [out.svg]
"""

import math
import sys


class Error(Exception):
    pass


class Name(str):
    """A name. A literal name (/x) is pushed; an executable one is
    looked up and run."""

    def __new__(cls, text, literal=False):
        name = super().__new__(cls, text)
        name.literal = literal
        return name


class Procedure(list):
    pass


class String(str):
    pass


class Mark:
    pass


class Exit(Exception):
    pass


def tokens(text):
    """Split the program into numbers, strings, names, and the
    brackets of procedures and arrays."""
    i = 0
    while i < len(text):
        c = text[i]
        if c.isspace():
            i += 1
        elif c == "%":
            while i < len(text) and text[i] != "\n":
                i += 1
        elif c in "{}[]":
            yield c
            i += 1
        elif c == "(":
            depth, j, out = 1, i + 1, []
            while j < len(text) and depth:
                if text[j] == "\\" and j + 1 < len(text):
                    out.append({"n": "\n", "t": "\t"}.get(text[j + 1], text[j + 1]))
                    j += 2
                    continue
                depth += {"(": 1, ")": -1}.get(text[j], 0)
                if depth:
                    out.append(text[j])
                j += 1
            if depth:
                raise Error("a string with no end")
            yield String("".join(out))
            i = j
        else:
            j = i
            while j < len(text) and not text[j].isspace() and text[j] not in "{}[]()%":
                j += 1
            if j == i:
                j += 1
            word = text[i:j]
            i = j
            try:
                yield int(word)
            except ValueError:
                try:
                    yield float(word)
                except ValueError:
                    if word.startswith("/"):
                        yield Name(word[1:], literal=True)
                    else:
                        yield Name(word)


def parse(stream):
    """Gather procedures into Procedure lists; everything else stays
    one token."""
    out = []
    stack = []
    for t in stream:
        if t == "{" and not isinstance(t, String):
            stack.append(out)
            out = Procedure()
        elif t == "}" and not isinstance(t, String):
            if not stack:
                raise Error("} with no {")
            done = out
            out = stack.pop()
            out.append(done)
        elif isinstance(t, str) and not isinstance(t, (Name, String)):
            out.append(Name(t))             # [ and ] are operators
        else:
            out.append(t)
    if stack:
        raise Error("{ with no }")
    return out


def show(x, syntax=False):
    """A value as = prints it, or, with syntax, as == does."""
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, float):
        text = f"{x:.6g}"
        return text if any(c in text for c in ".e") else text + ".0"
    if isinstance(x, String):
        return f"({x})" if syntax else str(x)
    if isinstance(x, Name):
        return ("/" if syntax and x.literal else "") + str(x)
    if isinstance(x, Procedure):
        return "{" + " ".join(show(y, True) for y in x) + "}"
    if isinstance(x, list):
        return "[" + " ".join(show(y, True) for y in x) + "]"
    if isinstance(x, dict):
        return "-dict-"
    if isinstance(x, Mark):
        return "-mark-"
    if callable(x):
        return "--" + x.__name__.strip("_") + "--"
    return str(x)


def multiply(m, n):
    """The matrix m, then n: [a b c d e f] as in PostScript."""
    a, b, c, d, e, f = m
    p, q, r, s, t, u = n
    return [a * p + b * r, a * q + b * s, c * p + d * r, c * q + d * s,
            e * p + f * r + t, e * q + f * s + u]


class Interpreter:

    def __init__(self, height):
        self.stack = []
        self.system = {}
        self.dicts = [self.system, {}]
        self.height = height
        self.paths = []                 # what has been painted, as SVG
        self.state = {"ctm": [1, 0, 0, 1, 0, 0], "gray": "#000000", "width": 1}
        self.saved = []
        self.path = []                  # the current path, in device space
        self.point = None
        self.install()

    # The stack

    def pop(self, *kinds):
        if not self.stack:
            raise Error("stackunderflow")
        x = self.stack.pop()
        if kinds and (not isinstance(x, kinds) or isinstance(x, bool) and bool not in kinds):
            raise Error(f"typecheck: {show(x, True)}")
        return x

    def number(self):
        return self.pop(int, float)

    def push(self, x):
        self.stack.append(x)

    # Running

    def lookup(self, name):
        for d in reversed(self.dicts):
            if name in d:
                return d[name]
        raise Error(f"undefined: {name}")

    def execute(self, x):
        """Run one object, as the interpreter meets it."""
        if isinstance(x, Name) and not x.literal:
            value = self.lookup(x)
            if callable(value):
                value()
            elif isinstance(value, Procedure):
                self.call(value)
            else:
                self.push(value)
        else:
            self.push(x)

    def call(self, procedure):
        """Run a procedure. A procedure inside it is not run, but
        pushed, to be used by if, def, repeat and the rest."""
        if not isinstance(procedure, Procedure):
            raise Error(f"typecheck: {show(procedure, True)} is not a procedure")
        for x in procedure:
            self.execute(x)

    def run(self, text):
        for x in parse(tokens(text)):
            self.execute(x)

    # The operators, put in the system dictionary by name

    def install(self):
        s = self.system
        binary = {
            "add": lambda a, b: a + b, "sub": lambda a, b: a - b,
            "mul": lambda a, b: a * b,
        }
        for name, f in binary.items():
            s[name] = self.arithmetic(name, f)
        compare = {
            "eq": lambda a, b: a == b, "ne": lambda a, b: a != b,
            "gt": lambda a, b: a > b, "ge": lambda a, b: a >= b,
            "lt": lambda a, b: a < b, "le": lambda a, b: a <= b,
        }
        for name, f in compare.items():
            s[name] = self.comparison(name, f)
        for name in dir(self):
            if name.startswith("op_"):
                op = getattr(self, name)
                s[op.__name__[3:].rstrip("_")] = op
        s["["] = self.op_mark
        s["]"] = self.end_array
        s["="] = self.print_value
        s["=="] = self.print_syntax
        s["true"] = True
        s["false"] = False

    def arithmetic(self, name, f):
        def op():
            b, a = self.number(), self.number()
            self.push(f(a, b))
        op.__name__ = name
        return op

    def comparison(self, name, f):
        def op():
            b, a = self.pop(), self.pop()
            self.push(f(a, b))
        op.__name__ = name
        return op

    def op_div(self):
        b, a = self.number(), self.number()
        if b == 0:
            raise Error("undefinedresult: division by zero")
        self.push(a / b)

    def op_idiv(self):
        b, a = self.pop(int), self.pop(int)
        if b == 0:
            raise Error("undefinedresult: division by zero")
        q = abs(a) // abs(b)
        self.push(q if (a < 0) == (b < 0) else -q)

    def op_mod(self):
        b, a = self.pop(int), self.pop(int)
        if b == 0:
            raise Error("undefinedresult: division by zero")
        r = abs(a) % abs(b)
        self.push(-r if a < 0 else r)

    def op_neg(self):
        self.push(-self.number())

    def op_abs(self):
        self.push(abs(self.number()))

    def op_sqrt(self):
        self.push(math.sqrt(self.number()))

    def op_sin(self):
        self.push(math.sin(math.radians(self.number())))

    def op_cos(self):
        self.push(math.cos(math.radians(self.number())))

    def op_not(self):
        x = self.pop(bool, int)
        self.push(not x if isinstance(x, bool) else ~x)

    def op_and(self):
        b, a = self.pop(bool, int), self.pop(bool, int)
        self.push(a and b if isinstance(a, bool) else a & b)

    def op_or(self):
        b, a = self.pop(bool, int), self.pop(bool, int)
        self.push(a or b if isinstance(a, bool) else a | b)

    def op_pop(self):
        self.pop()

    def op_dup(self):
        x = self.pop()
        self.push(x)
        self.push(x)

    def op_exch(self):
        b, a = self.pop(), self.pop()
        self.push(b)
        self.push(a)

    def op_copy(self):
        n = self.pop(int)
        if n < 0 or n > len(self.stack):
            raise Error("rangecheck: copy")
        self.stack += self.stack[len(self.stack) - n:]

    def op_index(self):
        n = self.pop(int)
        if n < 0 or n >= len(self.stack):
            raise Error("rangecheck: index")
        self.push(self.stack[-1 - n])

    def op_roll(self):
        j, n = self.pop(int), self.pop(int)
        if n < 0 or n > len(self.stack):
            raise Error("rangecheck: roll")
        if n:
            top = self.stack[len(self.stack) - n:]
            j %= n
            self.stack[len(self.stack) - n:] = top[n - j:] + top[:n - j]

    def op_clear(self):
        self.stack.clear()

    def op_count(self):
        self.push(len(self.stack))

    def op_mark(self):
        self.push(Mark())

    def end_array(self):
        items = []
        while True:
            x = self.pop()
            if isinstance(x, Mark):
                break
            items.append(x)
        self.push(items[::-1])

    def op_length(self):
        self.push(len(self.pop(list, String, dict)))

    def op_get(self):
        k = self.pop()
        a = self.pop(list, String, dict)
        try:
            self.push(ord(a[k]) if isinstance(a, String) else a[k])
        except (IndexError, KeyError, TypeError):
            raise Error(f"rangecheck: get {show(k, True)}")

    def op_put(self):
        v, k = self.pop(), self.pop()
        a = self.pop(list, dict)
        try:
            a[k] = v
        except (IndexError, TypeError):
            raise Error(f"rangecheck: put {show(k, True)}")

    def op_forall(self):
        proc = self.pop(Procedure)
        items = self.pop(list, String)
        for x in items:
            self.push(ord(x) if isinstance(items, String) else x)
            try:
                self.call(proc)
            except Exit:
                break

    def op_string(self):
        n = self.pop(int)
        if n < 0:
            raise Error("rangecheck: string")
        self.push(String(" " * n))

    def op_cvs(self):
        room = self.pop(String)
        text = show(self.pop())
        if len(text) > len(room):
            raise Error("rangecheck: cvs")
        self.push(String(text))

    def op_def(self):
        value = self.pop()
        name = self.pop(Name)
        self.dicts[-1][Name(name)] = value

    def op_dict(self):
        self.pop(int)
        self.push({})

    def op_begin(self):
        self.dicts.append(self.pop(dict))

    def op_end(self):
        if len(self.dicts) <= 2:
            raise Error("dictstackunderflow")
        self.dicts.pop()

    def op_load(self):
        self.push(self.lookup(self.pop(Name)))

    def op_bind(self):
        pass                            # the procedure stays as it is

    def op_exec(self):
        x = self.pop()
        if isinstance(x, Procedure):
            self.call(x)
        else:
            self.execute(x)

    def op_if(self):
        proc = self.pop(Procedure)
        if self.pop(bool):
            self.call(proc)

    def op_ifelse(self):
        no, yes = self.pop(Procedure), self.pop(Procedure)
        self.call(yes if self.pop(bool) else no)

    def op_repeat(self):
        proc = self.pop(Procedure)
        for _ in range(self.pop(int)):
            try:
                self.call(proc)
            except Exit:
                break

    def op_for(self):
        proc = self.pop(Procedure)
        limit, step, i = self.number(), self.number(), self.number()
        if step == 0:
            raise Error("rangecheck: for with step 0")
        while (i <= limit) if step > 0 else (i >= limit):
            self.push(i)
            try:
                self.call(proc)
            except Exit:
                break
            i += step

    def op_loop(self):
        proc = self.pop(Procedure)
        while True:
            try:
                self.call(proc)
            except Exit:
                break

    def op_exit(self):
        raise Exit()

    def print_value(self):
        print(show(self.pop()))

    def print_syntax(self):
        print(show(self.pop(), True))

    def op_print(self):
        print(self.pop(String), end="")

    def op_pstack(self):
        for x in reversed(self.stack):
            print(show(x, True))

    # Painting

    def device(self, x, y):
        a, b, c, d, e, f = self.state["ctm"]
        return (a * x + c * y + e, b * x + d * y + f)

    def concat(self, m):
        self.state["ctm"] = multiply(m, self.state["ctm"])

    def op_translate(self):
        ty, tx = self.number(), self.number()
        self.concat([1, 0, 0, 1, tx, ty])

    def op_scale(self):
        sy, sx = self.number(), self.number()
        self.concat([sx, 0, 0, sy, 0, 0])

    def op_rotate(self):
        r = math.radians(self.number())
        self.concat([math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0, 0])

    def op_gsave(self):
        self.saved.append((dict(self.state), list(self.path), self.point))

    def op_grestore(self):
        if self.saved:
            state, self.path, self.point = self.saved.pop()
            self.state = state

    def op_setlinewidth(self):
        self.state["width"] = self.number()

    def op_setgray(self):
        g = round(255 * min(1, max(0, self.number())))
        self.state["gray"] = f"#{g:02x}{g:02x}{g:02x}"

    def op_setrgbcolor(self):
        b, g, r = self.number(), self.number(), self.number()
        self.state["gray"] = "#" + "".join(f"{round(255 * min(1, max(0, v))):02x}" for v in (r, g, b))

    def op_newpath(self):
        self.path = []
        self.point = None

    def op_moveto(self):
        y, x = self.number(), self.number()
        self.point = (x, y)
        self.path.append(("M", self.device(x, y)))

    def op_lineto(self):
        y, x = self.number(), self.number()
        if self.point is None:
            raise Error("nocurrentpoint")
        self.point = (x, y)
        self.path.append(("L", self.device(x, y)))

    def op_rmoveto(self):
        dy, dx = self.number(), self.number()
        if self.point is None:
            raise Error("nocurrentpoint")
        self.push(self.point[0] + dx)
        self.push(self.point[1] + dy)
        self.op_moveto()

    def op_rlineto(self):
        dy, dx = self.number(), self.number()
        if self.point is None:
            raise Error("nocurrentpoint")
        self.push(self.point[0] + dx)
        self.push(self.point[1] + dy)
        self.op_lineto()

    def op_arc(self):
        """An arc, as short straight lines: from angle a1 to a2,
        anticlockwise, around x y. A bigger arc gets more of them."""
        a2, a1, r, y, x = (self.number() for _ in range(5))
        while a2 < a1:
            a2 += 360
        a, b, c, d, _, _ = self.state["ctm"]
        size = r * math.sqrt(abs(a * d - b * c))      # the radius on the page
        steps = max(2, math.ceil((a2 - a1) / 360 * min(48, max(8, 2 * size))))
        for k in range(steps + 1):
            t = math.radians(a1 + (a2 - a1) * k / steps)
            px, py = x + r * math.cos(t), y + r * math.sin(t)
            self.path.append(("L" if self.point is not None else "M", self.device(px, py)))
            self.point = (px, py)

    def op_closepath(self):
        if self.path:
            self.path.append(("Z", None))

    def paint(self, how):
        if not self.path:
            return
        d = []
        for op, p in self.path:
            d.append(op if p is None else f"{op}{fmt(p[0])} {fmt(self.height - p[1])}")
        a, b, c, d_, e, f = self.state["ctm"]
        width = self.state["width"] * math.sqrt(abs(a * d_ - b * c))
        colour = self.state["gray"]
        if how == "fill":
            self.paths.append(f'<path d="{"".join(d)}" fill="{colour}"/>')
        else:
            self.paths.append(f'<path d="{"".join(d)}" fill="none" stroke="{colour}" '
                              f'stroke-width="{fmt(width)}" stroke-linecap="round" stroke-linejoin="round"/>')
        self.op_newpath()

    def op_stroke(self):
        self.paint("stroke")

    def op_fill(self):
        self.paint("fill")

    def op_showpage(self):
        pass

    def svg(self, width):
        body = "\n".join(self.paths)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(width)}" height="{fmt(self.height)}" '
                f'viewBox="0 0 {fmt(width)} {fmt(self.height)}">\n'
                f'<rect width="100%" height="100%" fill="#ffffff"/>\n{body}\n</svg>\n')


def fmt(v):
    text = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


def page_size(text):
    for line in text.splitlines():
        if line.startswith("%%BoundingBox:"):
            parts = line.split()[1:]
            if len(parts) == 4:
                return float(parts[2]), float(parts[3])
    return 612.0, 792.0


def main(args):
    if len(args) not in (1, 2):
        sys.exit("usage: ps.py program.ps [out.svg]")
    with open(args[0]) as f:
        text = f.read()
    width, height = page_size(text)
    interpreter = Interpreter(height)
    try:
        interpreter.run(text)
    except Error as e:
        sys.exit(f"ps: {e}")
    except Exit:
        sys.exit("ps: exit outside a loop")
    except RecursionError:
        sys.exit("ps: execstackoverflow")
    if len(args) == 2:
        with open(args[1], "w") as f:
            f.write(interpreter.svg(width))


if __name__ == "__main__":
    main(sys.argv[1:])
