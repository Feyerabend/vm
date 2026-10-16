#!/usr/bin/env python3
"""
Write random programs, to test the verifier.

If the verifier ever accepts a program it should refuse, the machine
runs it without the checks that would have caught it, and may read or
write outside its stack. To find such a program, if there is one,
fuzz.sh runs every program made here twice, once verified and once
with every check, on a machine built with AddressSanitizer, and
compares.

Purely random programs almost never verify, so these are made with a
bias: the generator keeps count of the stack depth, chooses mostly
instructions the depth allows, and jumps mostly back to places where
the depth was the same. Now and then it breaks the rules on purpose,
so that the verifier has something to refuse.

    usage: fuzz.py seed count directory
"""

import os
import random
import struct
import sys

import isa

POPS = {"ADD": 2, "SUB": 2, "MUL": 2, "DIV": 2, "MOD": 2, "AND": 2, "OR": 2, "XOR": 2,
        "LT": 2, "EQ": 2, "PRINT": 1, "DUP": 1, "DROP": 1, "SWAP": 2, "OVER": 2,
        "ROT": 3, "NEW": 1, "GETF": 2, "SETF": 3, "LEN": 1, "LOADM": 1, "STOREM": 2}
PUSHES = {"ADD": 1, "SUB": 1, "MUL": 1, "DIV": 1, "MOD": 1, "AND": 1, "OR": 1, "XOR": 1,
          "LT": 1, "EQ": 1, "PRINT": 0, "DUP": 2, "DROP": 0, "SWAP": 2, "OVER": 3,
          "ROT": 3, "NEW": 1, "GETF": 1, "SETF": 0, "LEN": 1, "LOADM": 1, "STOREM": 0}


def program(rng):
    code, depth_at = [], {}
    d = 0
    cheat = rng.random() < 0.3
    for _ in range(rng.randint(5, 60)):
        depth_at[len(code)] = d
        r = rng.random()
        if r < 0.25 or d == 0:
            code += [isa.BY_NAME["PUSH"][0], rng.choice([0, 1, 2, 3, -1, 7, 100, 4095, 70000])]
            d += 1
        elif r < 0.35:
            k = rng.randrange(d + (2 if cheat else 0))
            code += [isa.BY_NAME["LOAD"][0], k]
            d += 1
        elif r < 0.42 and d >= 2:
            k = rng.randrange(d - 1 + (2 if cheat else 0))
            code += [isa.BY_NAME["STORE"][0], k]
            d -= 1
        elif r < 0.50:
            same = [a for a, x in depth_at.items() if x == (d - 1 if True else d)]
            if same and d >= 1:
                code += [isa.BY_NAME["JZ"][0], rng.choice(same) if not cheat else rng.randrange(len(code) + 3)]
                d -= 1
            else:
                code += [isa.BY_NAME["DUP"][0]]
                d += 1
        else:
            name = rng.choice(list(POPS))
            if POPS[name] > d and not cheat:
                continue
            code += [isa.BY_NAME[name][0]]
            d = max(d - POPS[name], 0) + PUSHES[name]
        if d > 250:
            break
    code += [isa.BY_NAME["HALT"][0]]
    if cheat and rng.random() < 0.3:
        code = code[:-1]                    # run off the end
    return code


def main():
    seed, count, directory = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    os.makedirs(directory, exist_ok=True)
    for n in range(count):
        code = program(rng)
        with open(os.path.join(directory, f"p{n:05d}.vm"), "wb") as f:
            f.write(b"SVM\x01" + struct.pack("<i", len(code)) + struct.pack(f"<{len(code)}i", *code))


if __name__ == "__main__":
    main()
