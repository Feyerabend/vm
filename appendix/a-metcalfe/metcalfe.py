"""
A parsing machine, after Howard Metcalfe (1964).

The machine reads a tape of tokens and writes a tape of output. Its
only memory is one flag, which says whether the last test succeeded,
and a stack of calls. Each call remembers where on both tapes it
started, so that a rule which fails can be undone: the input goes
back to where the rule began, and what it wrote is taken away.

    call L      call the rule at L
    return      return; if the flag is false, undo the rule
    match x     if the next token is x, take it and set the flag;
                otherwise clear the flag. "match ?" takes any name
                or number.
    print x     write x on the output; "print ?" writes the token
                that "match ?" took last
    true L      jump to L if the flag is set
    false L     jump to L if the flag is clear
    flag true   set the flag
    flag false  clear the flag
    stop        stop

A program is a list of these, with labels ("name:"). It is run once
for each line of standard input, and says what it wrote, or that the
line was not accepted. The end of every line is the token "$".

    python3 metcalfe.py [-t] program.mc < lines
"""

import sys

OPS = {"call": 1, "return": 0, "match": 1, "print": 1, "true": 1,
       "false": 1, "flag": 1, "stop": 0}


class Error(Exception):
    pass


def assemble(text):
    """Turn the program into a list of (op, argument), and its labels
    into addresses in that list."""
    code = []
    labels = {}
    lines = []
    for number, line in enumerate(text.splitlines(), 1):
        line = line.split("#")[0].strip()
        while line and line.split()[0].endswith(":"):
            label, line = line.split(":", 1)
            labels[label] = len(code)
            line = line.strip()
        if not line:
            continue
        words = line.split()
        op = words[0]
        if op not in OPS:
            raise Error(f"line {number}: unknown instruction {op!r}")
        if len(words) - 1 != OPS[op]:
            raise Error(f"line {number}: {op} takes {OPS[op]} operand(s)")
        argument = words[1] if OPS[op] else None
        if op == "flag" and argument not in ("true", "false"):
            raise Error(f"line {number}: flag is true or false")
        code.append((op, argument))
        lines.append(number)
    for k, (op, argument) in enumerate(code):
        if op in ("call", "true", "false"):
            if argument not in labels:
                raise Error(f"line {lines[k]}: no label {argument!r}")
            code[k] = (op, labels[argument])
    return code


def tokens(line):
    """Names and numbers are one token each; any other character is a
    token by itself."""
    result = []
    i = 0
    while i < len(line):
        c = line[i]
        if c.isspace():
            i += 1
        elif c.isalnum():
            j = i
            while j < len(line) and line[j].isalnum():
                j += 1
            result.append(line[i:j])
            i = j
        else:
            result.append(c)
            i += 1
    return result + ["$"]


def run(code, tape, trace=False):
    """Run the program on one tape. Return the output, or None if the
    input was not accepted."""
    pc = 0
    flag = False
    at = 0              # the next token on the input tape
    out = []            # the output tape
    last = None         # what "match ?" took
    calls = []          # (return address, input position, output length)
    while True:
        op, argument = code[pc]
        if trace:
            shown = "" if argument is None else f" {argument}"
            print(f"  {pc:3}  {op + shown:12} {' '.join(tape[at:]):24} {' '.join(out)}")
        pc += 1
        if op == "call":
            calls.append((pc, at, len(out)))
            pc = argument
        elif op == "return":
            if not calls:
                raise Error("return with no call")
            pc, start, written = calls.pop()
            if not flag:
                at = start
                del out[written:]
        elif op == "match":
            token = tape[at] if at < len(tape) else None
            if argument == "?":
                flag = token is not None and token.isalnum()
            else:
                flag = token == argument
            if flag:
                last = token
                at += 1
        elif op == "print":
            out.append(last if argument == "?" else argument)
        elif op == "true":
            if flag:
                pc = argument
        elif op == "false":
            if not flag:
                pc = argument
        elif op == "flag":
            flag = argument == "true"
        elif op == "stop":
            return out if flag and at == len(tape) else None


def main(args):
    trace = "-t" in args
    args = [a for a in args if a != "-t"]
    if len(args) != 1:
        sys.exit("usage: metcalfe.py [-t] program.mc < lines")
    try:
        with open(args[0]) as f:
            code = assemble(f.read())
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            out = run(code, tokens(line), trace)
            if out is None:
                print(f"{line}  =>  not accepted")
            else:
                print(f"{line}  =>  {' '.join(out)}")
    except Error as e:
        sys.exit(f"metcalfe: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
