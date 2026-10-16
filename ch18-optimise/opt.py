#!/usr/bin/env python3
"""
A peephole optimiser for the stack machine's assembly language.

A peephole optimiser looks at the program through a small window, a
few instructions at a time, and replaces what it sees there with
something shorter that does the same:

    PUSH 2                      PUSH 6
    PUSH 3          ==>
    MUL

It repeats until nothing more changes, since one improvement often
makes room for another. The rules:

    constant folding    PUSH a, PUSH b, op            ->  PUSH (a op b)
    no effect           PUSH a, DROP / DUP, DROP / LOAD k, DROP / SWAP, SWAP  ->  nothing
    double negation     LT or EQ, then PUSH 0, EQ twice  ->  LT or EQ
    jump threading      a jump to a JMP goes straight to where that JMP goes
    jump to next        JMP to the very next instruction  ->  nothing
    dead code           what no path can reach            ->  nothing

The rules must not change what a program does, and that includes how
it fails. 'PUSH 0, DROP' looks harmless, but on a full stack PUSH
traps with "stack overflow", and without it, nothing does. So the
first five rules are used only where chapter 17's analysis says how
deep the stack is: then the optimiser can see that the PUSH has room,
and that no instruction in the window would trap. Nothing is assumed
about values: 'x + 0' is not simplified to 'x', since if x is a
reference, the ADD traps.

Where the analysis knows nothing, for a program that uses CALLI, only
jump threading and dead code removal are done. A program that uses
numbers instead of labels for code addresses (JMP 17) is left as it is,
since moving code would make those numbers wrong.

Addresses change, so a trap in an optimised program names a different
address. The trap itself, and everything before it, are the same.

    usage: opt.py [-s] program.asm > optimised.asm

-s prints, on stderr, how many instructions each rule removed.
"""

import collections
import re
import sys

import asm
import flow
import isa

BINARY = {"ADD", "SUB", "MUL", "DIV", "MOD", "AND", "OR", "XOR", "LT", "EQ"}
NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class Item:
    """One instruction, and the labels in front of it."""

    def __init__(self, labels, op, operands):
        self.labels = labels
        self.op = op            # upper case; None for labels at the very end
        self.operands = operands

    def text(self):
        return " ".join([self.op] + self.operands)


def wrap(n):
    return (n + 2**31) % 2**32 - 2**31


def fold(op, a, b):
    """a op b as the machine computes it, or None if it would trap."""
    if op in ("DIV", "MOD"):
        if b == 0:
            return None
        q = abs(a) // abs(b)
        q = q if (a < 0) == (b < 0) else -q
        return wrap(q) if op == "DIV" else wrap(a - b * q)
    return wrap({"ADD": a + b, "SUB": a - b, "MUL": a * b, "AND": a & b,
                 "OR": a | b, "XOR": a ^ b, "LT": int(a < b), "EQ": int(a == b)}[op])


def number(word):
    try:
        return int(word, 0)
    except ValueError:
        return None


def parse(text, path):
    items, pending = [], []
    for k, line in enumerate(text.splitlines(), 1):
        parsed = asm.parse_line(k, line)
        pending += parsed.labels
        if parsed.op is not None:
            op = parsed.op if parsed.op.lower() == ".word" else parsed.op.upper()
            items.append(Item(pending, op, parsed.operands))
            pending = []
    if pending:
        items.append(Item(pending, None, []))       # labels at the very end
    return items


def render(items):
    lines = []
    for item in items:
        for label in item.labels:
            lines.append(f"{label}:")
        if item.op is not None:
            lines.append(f"        {item.text()}")
    return "\n".join(lines) + "\n"


def code_addresses_are_labels(items):
    for item in items:
        if item.op in ("JMP", "JZ", "CALL") and number(item.operands[0]) is not None:
            return False
    return True


def analyse(items):
    """The depth before each item, by index, and the items certain to
    trap; or None, None if the program cannot be analysed."""
    assembler = asm.Assembler("(optimiser)")
    lines, code = assembler.assemble(render(items))
    if assembler.errors:
        raise SystemExit("\n".join(m for _, m in assembler.errors))
    # The rendered text has a line for each label and one for each
    # instruction; the instruction lines are the items, in order.
    addresses = iter([line.address for line in lines if line.op is not None])
    try:
        depth, traps, _ = flow.analyse(code)
    except flow.Refused:
        return None, None
    by_item, trapping = [], []
    for item in items:
        if item.op is None:             # labels at the end: never touched
            by_item.append(None)
            trapping.append(True)
            continue
        a = next(addresses)
        by_item.append(depth.get(a))
        trapping.append(a in traps)
    return by_item, trapping


def pass_peephole(items, depth, trapping, removed):
    """One sweep of the window rules. Returns True if anything changed."""
    out, i, changed = [], 0, False

    def plain(k):
        """Item k exists, has no label (nothing jumps into the window
        there), and is not certain to trap."""
        return k < len(items) and not items[k].labels and not trapping[k]

    while i < len(items):
        item = items[i]
        known = depth[i] is not None and not trapping[i]
        if known and item.op == "PUSH" and plain(i + 1) and plain(i + 2):
            a, b = number(item.operands[0]), (number(items[i + 1].operands[0])
                                              if items[i + 1].op == "PUSH" else None)
            op = items[i + 2].op
            if a is not None and b is not None and op in BINARY and depth[i] + 2 <= flow.REGISTERS:
                r = fold(op, a, b)
                if r is not None:
                    out.append(Item(item.labels, "PUSH", [str(r)]))
                    removed["constant folding"] += 2
                    i += 3
                    changed = True
                    continue
        if known and plain(i + 1) and items[i + 1].op == "DROP":
            if (item.op == "PUSH" and depth[i] + 1 <= flow.REGISTERS) or item.op in ("DUP", "LOAD"):
                if item.labels:
                    carry(items, i + 2, item.labels)
                removed["no effect"] += 2
                i += 2
                changed = True
                continue
        if known and item.op == "SWAP" and plain(i + 1) and items[i + 1].op == "SWAP":
            if item.labels:
                carry(items, i + 2, item.labels)
            removed["no effect"] += 2
            i += 2
            changed = True
            continue
        if (known and item.op in ("LT", "EQ") and all(plain(i + k) for k in range(1, 5))
                and [items[i + k].text() for k in range(1, 5)] == ["PUSH 0", "EQ", "PUSH 0", "EQ"]):
            out.append(item)
            removed["double negation"] += 4
            i += 5
            changed = True
            continue
        out.append(item)
        i += 1
    items[:] = out
    return changed


def carry(items, k, labels):
    """Labels on removed instructions move on to the next one."""
    if k < len(items):
        items[k].labels = labels + items[k].labels
    else:
        items.append(Item(labels, None, []))


def pass_jumps(items, removed):
    changed = False
    at = {}
    for k, item in enumerate(items):
        for label in item.labels:
            at[label] = k
    for k, item in enumerate(items):
        if item.op in ("JMP", "JZ") and item.operands[0] in at:
            seen = set()
            target = item.operands[0]
            while target in at and items[at[target]].op == "JMP" and target not in seen:
                seen.add(target)
                nxt = items[at[target]].operands[0]
                if nxt == target or nxt not in at:
                    break
                target = nxt
            if target != item.operands[0]:
                item.operands[0] = target
                removed["jumps threaded"] += 1
                changed = True
    out = []
    for k, item in enumerate(items):
        if (item.op == "JMP" and k + 1 < len(items)
                and item.operands[0] in items[k + 1].labels):
            if item.labels:
                carry(items, k + 1, item.labels)
            removed["jump to next"] += 1
            changed = True
            continue
        out.append(item)
    items[:] = out
    return changed


def pass_dead(items, removed):
    """Remove instructions no path can reach. Paths start at the first
    instruction and at every label the program uses as a value (PUSH
    label: the start of a closure's code)."""
    at = {}
    for k, item in enumerate(items):
        for label in item.labels:
            at[label] = k
    work = [0] + [at[i.operands[0]] for i in items if i.op == "PUSH" and i.operands[0] in at]
    seen = set()
    while work:
        k = work.pop()
        if k in seen or k >= len(items):
            continue
        seen.add(k)
        item = items[k]
        if item.op in ("JMP", "JZ", "CALL") and item.operands[0] in at:
            work.append(at[item.operands[0]])
        if item.op not in ("JMP", "HALT", "RET", None):
            work.append(k + 1)
    used = {i.operands[0] for i in items if i.op in ("JMP", "JZ", "CALL", "PUSH")}
    out = []
    for k, item in enumerate(items):
        if k not in seen:
            removed["dead code"] += 1
            continue
        item.labels = [label for label in item.labels if label in used]
        out.append(item)
    changed = len(out) != len(items)
    items[:] = out
    return changed


def optimise(items):
    removed = collections.Counter()
    if not code_addresses_are_labels(items):
        return items, removed, "uses numbers as code addresses: left as it is"
    note = None
    for _ in range(100):
        changed = pass_jumps(items, removed)
        changed |= pass_dead(items, removed)
        depth, trapping = analyse(items)
        if depth is None:
            note = "cannot be analysed: only jumps and dead code were optimised"
        else:
            changed |= pass_peephole(items, depth, trapping, removed)
        if not changed:
            break
    return items, removed, note


def main():
    args = sys.argv[1:]
    stats = args[:1] == ["-s"]
    if stats:
        args = args[1:]
    if len(args) != 1:
        sys.exit("usage: opt.py [-s] program.asm > optimised.asm")
    with open(args[0]) as f:
        items = parse(f.read(), args[0])
    before = len(items)
    items, removed, note = optimise(items)
    sys.stdout.write(render(items))
    if stats:
        print(f"{args[0]}: {before} instructions, {len(items)} after", file=sys.stderr)
        for rule, n in sorted(removed.items()):
            if n:
                print(f"  {rule}: {n}", file=sys.stderr)
        if note:
            print(f"  {note}", file=sys.stderr)


if __name__ == "__main__":
    main()
