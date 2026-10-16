"""
The stack-depth analysis of chapter 17's translate.py, on its own.

For every instruction that can be reached, it works out how deep the
stack is when the instruction runs, and which instructions are certain
to trap. A program whose depth at some point depends on the path taken
there, or that uses CALLI, is refused: then nothing is known.
"""

import isa


class Refused(Exception):
    pass


# How each stack instruction changes the depth: values taken, values left.
EFFECT = {
    "HALT": (0, 0), "PUSH": (0, 1), "PRINT": (1, 0), "EMIT": (1, 0),
    "ADD": (2, 1), "SUB": (2, 1), "MUL": (2, 1), "DIV": (2, 1), "MOD": (2, 1),
    "AND": (2, 1), "OR": (2, 1), "XOR": (2, 1), "LT": (2, 1), "EQ": (2, 1),
    "JMP": (0, 0), "JZ": (1, 0), "DUP": (1, 2), "DROP": (1, 0), "SWAP": (2, 2),
    "OVER": (2, 3), "ROT": (3, 3), "LOAD": (0, 1), "STORE": (1, 0), "RET": (1, 0),
    "LOADM": (1, 1), "STOREM": (2, 0), "NEW": (1, 1), "GETF": (2, 1),
    "SETF": (3, 0), "LEN": (1, 1),
}

REGISTERS = 256         # the most values the stack can hold


def decode(code):
    """Every instruction start reachable by straight-line decoding from 0."""
    out = {}
    pc = 0
    while pc < len(code):
        entry = isa.BY_CODE.get(code[pc])
        if entry is None:
            out[pc] = (".word", [])
            pc += 1
            continue
        name, kinds = entry
        if pc + len(kinds) >= len(code):
            out[pc] = (".cut", [])
            break
        out[pc] = (name, code[pc + 1:pc + 1 + len(kinds)])
        pc += 1 + len(kinds)
    return out


def analyse(code):
    """The depth before each reachable instruction, the instructions
    certain to trap, and the functions with their numbers of arguments. A function is named by its entry address.

    Some instructions can be seen, from the depth alone, to trap
    whenever they are reached: an ADD with one value in the frame, a
    jump to address 9999. Those are not refused: they become a TRAP
    instruction, with the message and address the stack machine would
    give, checked in the order the specification gives. What is refused
    is only what the register machine cannot express: a stack whose
    depth depends on the path taken, code shared between functions,
    a jump into the middle of an instruction, and CALLI."""
    instructions = decode(code)
    depth, owner, traps = {}, {}, {}
    entries = {0: 0}
    work = [(0, 0, 0)]                 # (address, depth, function)
    while work:
        pc, d, fn = work.pop()
        if pc in depth:
            if depth[pc] != d:
                raise Refused(f"at {pc} the stack can be {depth[pc]} or {d} deep")
            if owner[pc] != fn:
                raise Refused(f"the code at {pc} is shared by the functions at {owner[pc]} and {fn}")
            continue
        depth[pc], owner[pc] = d, fn
        if pc == len(code):
            traps[pc] = "ran off the end of the program"
            continue
        if pc not in instructions:
            raise Refused(f"a jump to {pc}, which is not the start of an instruction")
        name, ops = instructions[pc]

        def stop(message):
            traps[pc] = message

        if name == ".word":
            stop("unknown instruction")
            continue
        if name == ".cut":
            stop("missing operand")
            continue
        if name == "CALLI":
            raise Refused(f"at {pc}: CALLI, whose targets cannot be known before running")
        nxt = pc + 1 + len(ops)
        if name == "CALL":
            target, n = ops
            if not 0 <= target < len(code):
                stop("jump out of program")
                continue
            if n < 0 or n > d:
                stop("not enough arguments")
                continue
            if target in entries and entries[target] != n:
                raise Refused(f"the function at {target} is called with {entries[target]} and with {n} arguments")
            if target not in entries:
                entries[target] = n
                work.append((target, n, target))
            work.append((nxt, d - n + 1, fn))
            continue
        if name in ("JMP", "JZ") and not 0 <= ops[0] < len(code):
            stop("jump out of program")
            continue
        if name == "RET" and fn == 0:
            stop("return without call")
            continue
        taken, left = EFFECT[name]
        if name == "LOAD" and not 0 <= ops[0] < d:
            stop("no such local")
            continue
        if d < taken:
            stop("stack underflow")
            continue
        if name == "STORE" and not 0 <= ops[0] < d - 1:
            stop("no such local")
            continue
        after = d - taken + left
        if after > REGISTERS:
            stop("stack overflow")
            continue
        if name in ("JMP", "JZ"):
            work.append((ops[0], after, fn))
        if name not in ("JMP", "HALT", "RET"):
            work.append((nxt, after, fn))
    return depth, traps, entries


