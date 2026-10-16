#!/usr/bin/env python3
"""
Translate a program for the stack machine into one for the register
machine, rvm.c.

The stack machine's instructions name no places: ADD takes the two
values on top and leaves its result on top. But in a well-behaved
program, how deep the stack is at each instruction does not depend on
how the program got there. If the depth is known before running, then
"the value on top" at an instruction where the depth is 5 is simply
"the value in slot 4", and the instruction can say so:

    stack           depth       register
    LOAD 0          2 -> 3      MOV  r2, r0
    LOAD 1          3 -> 4      MOV  r3, r1
    ADD             4 -> 3      ADD  r2, r2, r3
    STORE 1         3 -> 2      MOV  r1, r2

That is the first stage, and it gives exactly as many instructions as
it started with. The second stage notices that r2 and r3 were only
copies of r0 and r1, used once, and that slots at or above the depth
are never read again. What is left:

    ADD  r1, r0, r1

Four instructions became one.

Working out the depths is a data-flow analysis. Start at each entry
point with a known depth: address 0 with depth 0, and the target of
each CALL with depth equal to its number of arguments. Follow every
path, adding up each instruction's effect. Where two paths meet, they
must agree. A program where they do not, or where the depth could go
below zero, or that jumps into the middle of an instruction, or uses
CALLI, whose targets cannot be known in advance, is refused.

    usage: translate.py [-l] [-naive] program.vm program.rvm

-l prints the register code. -naive skips the second stage.
"""

import struct
import sys

import isa
import vmfile


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

REGISTERS = 256         # the register file, as big as the stack machine's stack


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
    """The depth before each reachable instruction, and which function
    each belongs to. A function is named by its entry address.

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
    for pc in traps:
        instructions[pc] = ("TRAP", [traps[pc]])
    return instructions, depth, owner, entries


TRAPS = ["unknown instruction", "missing operand", "ran off the end of the program",
         "jump out of program", "stack underflow", "no such local",
         "not enough arguments", "return without call", "stack overflow"]


# The register machine's instructions. Each is five numbers: an
# opcode, up to three operands, and the address of the stack
# instruction it came from, which is what a trap reports.

ROPS = ["HALT", "MOVI", "MOV", "SWAPR", "ROTR",
        "ADD", "SUB", "MUL", "DIV", "MOD", "AND", "OR", "XOR", "LT", "EQ",
        "ADDI", "SUBI", "MULI", "DIVI", "MODI", "ANDI", "ORI", "XORI", "LTI", "EQI",
        "PRINT", "EMIT", "JMP", "JZ", "CALL", "RET",
        "LOADM", "STOREM", "NEW", "GETF", "SETF", "LEN", "TRAP"]
RCODE = {name: k for k, name in enumerate(ROPS)}
BINARY = ["ADD", "SUB", "MUL", "DIV", "MOD", "AND", "OR", "XOR", "LT", "EQ"]


def naive(code):
    """Stage one: every stack slot becomes a register, one for one."""
    instructions, depth, owner, entries = analyse(code)
    # The size of each function's register window: the deepest its
    # stack ever gets.
    size = {fn: 1 for fn in entries}
    for pc, d in depth.items():
        name, ops = instructions[pc]
        taken, left = EFFECT.get(name, (0, 0))
        size[owner[pc]] = max(size[owner[pc]], d, d - taken + left)
    # Only addresses that something jumps to or calls need a label.
    # They are also where basic blocks begin.
    targets = {0}
    for pc in depth:
        name, ops = instructions[pc]
        if name in ("JMP", "JZ", "CALL"):
            targets.add(ops[0])
    out = []    # (label, [opcode, operands...], origin, depth before, depth after)
    for pc in sorted(depth):
        name, ops = instructions[pc]
        d = depth[pc]
        label = pc if pc in targets else None
        taken, left = EFFECT.get(name, (0, 0))
        if name == "CALL":
            after = d - ops[1] + 1
        elif name in ("RET", "HALT", "TRAP"):
            after = 0
        else:
            after = d - taken + left

        def put(*ins, label_=None):
            out.append((label_, list(ins), pc, d, after))
        first = len(out)
        if name == "PUSH":
            put("MOVI", d, ops[0])
        elif name in BINARY:
            put(name, d - 2, d - 2, d - 1)
        elif name in ("PRINT", "EMIT"):
            put(name, d - 1)
        elif name == "JMP":
            put("JMP", ("addr", ops[0]))
        elif name == "JZ":
            put("JZ", d - 1, ("addr", ops[0]))
        elif name == "DUP":
            put("MOV", d, d - 1)
        elif name == "DROP":
            pass
        elif name == "SWAP":
            put("SWAPR", d - 2, d - 1)
        elif name == "OVER":
            put("MOV", d, d - 2)
        elif name == "ROT":
            put("ROTR", d - 3, d - 2, d - 1)
        elif name == "LOAD":
            put("MOV", d, ops[0])
        elif name == "STORE":
            put("MOV", ops[0], d - 1)
        elif name == "CALL":
            target, n = ops
            put("CALL", ("addr", target), d - n, size[target])
        elif name == "RET":
            put("RET", d - 1)
        elif name == "HALT":
            put("HALT")
        elif name == "TRAP":
            put("TRAP", TRAPS.index(ops[0]))
        elif name == "LOADM":
            put("LOADM", d - 1, d - 1)
        elif name == "STOREM":
            put("STOREM", d - 2, d - 1)
        elif name == "NEW":
            put("NEW", d - 1, d - 1)
        elif name == "GETF":
            put("GETF", d - 2, d - 2, d - 1)
        elif name == "SETF":
            put("SETF", d - 3, d - 2, d - 1)
        elif name == "LEN":
            put("LEN", d - 1, d - 1)
        # Every stack address that starts an instruction keeps a label,
        # even one that became nothing, like DROP.
        if len(out) == first:
            put("NOP")
        out[first] = (label,) + out[first][1:]
    return out, depth, entries, size


def reads_writes(ins):
    """The registers an instruction reads, and the registers it writes."""
    op, a = ins[0], ins[1:]
    if op in ("NOP", "JMP", "HALT", "TRAP"):
        return [], []
    if op == "MOVI":
        return [], [a[0]]
    if op == "MOV":
        return [a[1]], [a[0]]
    if op in BINARY or op == "GETF":
        return [a[1], a[2]], [a[0]]
    if op.endswith("I") and op[:-1] in BINARY:
        return [a[1]], [a[0]]
    if op in ("LOADM", "NEW", "LEN"):
        return [a[1]], [a[0]]
    if op in ("PRINT", "EMIT", "RET", "JZ"):
        return [a[0]], []
    if op == "STOREM":
        return [a[0], a[1]], []
    if op == "SETF":
        return [a[0], a[1], a[2]], []
    if op == "SWAPR":
        return [a[0], a[1]], [a[0], a[1]]
    if op == "ROTR":
        return [a[0], a[1], a[2]], [a[0], a[1], a[2]]
    raise ValueError(op)


# Where the registers an instruction reads are, in its list of operands.
READ_AT = {"MOV": [2], "PRINT": [1], "EMIT": [1], "RET": [1], "JZ": [1],
           "STOREM": [1, 2], "SETF": [1, 2, 3], "LOADM": [2], "NEW": [2],
           "LEN": [2], "GETF": [2, 3]}


def improve(out):
    """Stage two, one basic block at a time.

    Copy propagation, forwards: after MOV t, s, a later read of t can
    read s instead, as long as neither has been written since. After
    MOVI t, n, an operation on t can use n directly, in its immediate
    form: ADD r2, r2, r3 with r3 = 1 becomes ADDI r2, r2, 1.

    Dead code, backwards: a MOV or MOVI into a register that is never
    read again can go. Which registers might still be read after an
    instruction? The stack discipline tells: exactly those below the
    stack depth there. Everything at or above it was popped.
    """
    blocks, current = [], []
    for item in out:
        if item[0] is not None and current:
            blocks.append(current)
            current = []
        current.append(item)
        if item[1][0] in ("JMP", "JZ", "CALL", "RET", "HALT", "TRAP"):
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)

    result = []
    for block in blocks:
        block = [(lab, list(ins), org, before, after) for lab, ins, org, before, after in block]
        copy, const = {}, {}
        for lab, ins, org, before, after in block:
            op = ins[0]
            if op == "CALL":
                copy.clear()
                const.clear()
                continue
            positions = READ_AT.get(op, [])
            if op in BINARY:
                positions = [2, 3]
            elif op.endswith("I") and op[:-1] in BINARY:
                positions = [2]
            for p in positions:
                while ins[p] in copy:
                    ins[p] = copy[ins[p]]
            if op in BINARY and ins[3] in const:
                ins[:] = [op + "I", ins[1], ins[2], const[ins[3]]]
            elif op == "MOV" and ins[2] in const:
                ins[:] = ["MOVI", ins[1], const[ins[2]]]
            _, writes = reads_writes(ins)
            for w in writes:
                for r in list(copy):
                    if r == w or copy[r] == w:
                        del copy[r]
                const.pop(w, None)
            if ins[0] == "MOV" and ins[1] != ins[2]:
                copy[ins[1]] = ins[2]
            elif ins[0] == "MOVI":
                const[ins[1]] = ins[2]

        live = set(range(block[-1][4]))
        for k in range(len(block) - 1, -1, -1):
            lab, ins, org, before, after = block[k]
            if ins[0] == "CALL":
                window = ins[2]
                live.discard(window)
                live.update(range(window, before))
                continue
            reads, writes = reads_writes(ins)
            if ins[0] in ("MOV", "MOVI") and writes[0] not in live or ins[0] == "MOV" and ins[1] == ins[2]:
                block[k] = (lab, ["NOP"], org, before, after)
                continue
            # Coalescing: "ADD r2, r1, r3" then "MOV r1, r2", with r2
            # not needed afterwards, is "ADD r1, r1, r3". An
            # instruction reads its operands before it writes, so the
            # new destination may be one of them.
            if ins[0] == "MOV" and ins[2] not in live and k > 0 and lab is None:
                plab, pins, porg, pbefore, pafter = block[k - 1]
                if pins[0] not in ("SWAPR", "ROTR", "CALL", "NOP") and reads_writes(pins)[1] == [ins[2]]:
                    # With the MOV gone, what is live after the merged
                    # instruction is what was live after the MOV: so
                    # the live set stays exactly as it is.
                    pins[1] = ins[1]
                    block[k] = (lab, ["NOP"], org, before, after)
                    block[k - 1] = (plab, pins, porg, pbefore, pafter)
                    continue
            if ins[0] not in ("SWAPR", "ROTR"):
                live.difference_update(writes)
            live.update(reads)
        result += block

    return strip(result)


def strip(out):
    """NOPs go. A label on one moves to the next real instruction."""
    final, pending = [], []
    for lab, ins, org, before, after in out:
        if ins[0] == "NOP":
            if lab is not None:
                pending.append(lab)
            continue
        if pending:
            final.append((None, ["LABELS"] + pending, org, before, after))
            pending = []
        final.append((lab, ins, org, before, after))
    if pending:
        final.append((None, ["LABELS"] + pending, 0, 0, 0))
    return final


def assemble(out):
    """Turn the list into numbers: resolve stack addresses to register
    machine addresses. Each instruction takes five words."""
    where = {}
    count = 0
    for lab, ins, org, *_ in out:
        if ins[0] == "LABELS":
            for l in ins[1:]:
                where[l] = count
            continue
        if lab is not None:
            where[lab] = count
        count += 1
    words = []
    for lab, ins, org, *_ in out:
        if ins[0] == "LABELS":
            continue
        operands = [where[x[1]] if isinstance(x, tuple) else x for x in ins[1:]]
        operands += [0] * (3 - len(operands))
        words += [RCODE[ins[0]]] + operands + [org]
    return words, where


def listing(out):
    lines = []
    for lab, ins, org, *_ in out:
        if ins[0] == "LABELS":
            lines.append(f"S{'/S'.join(str(l) for l in ins[1:])}:")
            continue
        if lab is not None:
            lines.append(f"S{lab}:")
        ops = []
        for x in ins[1:]:
            ops.append(f"S{x[1]}" if isinstance(x, tuple) else str(x))
        text = ins[0]
        if ins[0] in ("MOVI",):
            text += f" r{ops[0]}, {ops[1]}"
        elif ins[0].endswith("I") and ins[0][:-1] in BINARY:
            text += f" r{ops[0]}, r{ops[1]}, {ops[2]}"
        elif ins[0] in ("JMP",):
            text += f" {ops[0]}"
        elif ins[0] == "JZ":
            text += f" r{ops[0]}, {ops[1]}"
        elif ins[0] == "CALL":
            text += f" {ops[0]}, window r{ops[1]}, size {ops[2]}"
        elif ins[0] == "TRAP":
            text += f" \"{TRAPS[int(ops[0])]}\""
        elif ops:
            text += " " + ", ".join(f"r{o}" for o in ops)
        lines.append(f"        {text:<28}; from {org}")
    return "\n".join(lines) + "\n"


def write(path, words):
    with open(path, "wb") as f:
        f.write(b"RVM\x01")
        f.write(struct.pack("<i", len(words)))
        f.write(struct.pack(f"<{len(words)}i", *words))


def main():
    args = sys.argv[1:]
    show = "-l" in args
    plain = "-naive" in args
    args = [a for a in args if a not in ("-l", "-naive")]
    if len(args) != 2:
        sys.exit("usage: translate.py [-l] [-naive] program.vm program.rvm")
    source, target = args
    # A damaged file is reported exactly as the machine reports it.
    try:
        code = vmfile.read(source)
    except OSError:
        print(f"{source}: cannot open", file=sys.stderr)
        sys.exit(2)
    except vmfile.FormatError as e:
        print(f"{source}: {e}", file=sys.stderr)
        sys.exit(2)
    try:
        out, depth, entries, size = naive(code)
        out = strip(out) if plain else improve(out)
    except Refused as e:
        print(f"{source}: refused: {e}", file=sys.stderr)
        sys.exit(3)
    words, _ = assemble(out)
    write(target, words)
    if show:
        sys.stdout.write(listing(out))


if __name__ == "__main__":
    main()
