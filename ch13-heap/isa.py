"""
The instruction set, as data.

Both the assembler and the disassembler read this table, so they
cannot disagree about what an instruction is called, what number it
has, or what operands it takes.

Each operand has a kind:

    "n"     a number
    "addr"  an address in the program: a label, or a number
    "k"     the number of a local in the current frame
"""

INSTRUCTIONS = [
    # (code, name, operand kinds)
    (0, "HALT", ()),
    (1, "PUSH", ("n",)),
    (2, "ADD", ()),
    (3, "SUB", ()),
    (4, "MUL", ()),
    (5, "PRINT", ()),
    (6, "JMP", ("addr",)),
    (7, "JZ", ("addr",)),
    (8, "DUP", ()),
    (9, "DROP", ()),
    (10, "SWAP", ()),
    (11, "OVER", ()),
    (12, "ROT", ()),
    (13, "LT", ()),
    (14, "EQ", ()),
    (15, "LOAD", ("k",)),
    (16, "STORE", ("k",)),
    (17, "CALL", ("addr", "n")),
    (18, "RET", ()),
    (19, "DIV", ()),
    (20, "MOD", ()),
    (21, "AND", ()),
    (22, "OR", ()),
    (23, "XOR", ()),
    (24, "LOADM", ()),
    (25, "STOREM", ()),
    (26, "EMIT", ()),
    (27, "NEW", ()),
    (28, "GETF", ()),
    (29, "SETF", ()),
    (30, "LEN", ()),
]

BY_NAME = {name: (code, kinds) for code, name, kinds in INSTRUCTIONS}
BY_CODE = {code: (name, kinds) for code, name, kinds in INSTRUCTIONS}
