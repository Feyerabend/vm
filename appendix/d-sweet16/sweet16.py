"""
SWEET16, Steve Wozniak's 16-bit machine inside the Apple II (1977).

Sixteen 16-bit registers in memory: R0 is the accumulator, R12 the
stack pointer for subroutine calls, R13 holds the result of a compare,
R14 the status, R15 the program counter. A register instruction is one
byte, the operation in the high four bits and the register in the low
four. The other instructions, with high bits 0, branch.

    SET Rn,v   Rn := v                  1n  (two bytes of v follow)
    LD Rn      R0 := Rn                 2n
    ST Rn      Rn := R0                 3n
    LD @Rn     R0 := byte at Rn, Rn++   4n
    ST @Rn     byte at Rn := R0, Rn++   5n
    LDD @Rn    R0 := word at Rn, Rn+=2  6n
    STD @Rn    word at Rn := R0, Rn+=2  7n
    POP @Rn    Rn--, R0 := byte at Rn   8n
    STP @Rn    Rn--, byte at Rn := R0   9n
    ADD Rn     R0 += Rn                 An
    SUB Rn     R0 -= Rn                 Bn
    POPD @Rn   Rn-=2, R0 := word at Rn  Cn
    CPR Rn     R13 := R0 - Rn           Dn
    INR Rn     Rn++                     En
    DCR Rn     Rn--                     Fn

    RTN  00   BR  01   BNC 02   BC  03   BP 04   BM 05   BZ 06
    BNZ  07   BM1 08   BNM1 09  BK  0A   RS 0B   BS 0C

A branch is followed by one byte, a distance from the next
instruction. It tests the register that the last instruction changed
(the "prior result"): positive, negative, zero, minus one; or the
carry, which ADD, SUB and CPR set. BS calls, pushing the return
address at R12, and RS returns.

On the Apple II, RTN goes back to 6502 code. Here it stops the machine,
which then shows the registers, and any memory asked for with -m, in hexadecimal.

    python3 sweet16.py [-t] [-m from:to] program.s16
"""

import sys

REGISTER_OPS = {"SET": 0x1, "LD": 0x2, "ST": 0x3, "ADD": 0xA, "SUB": 0xB,
                "CPR": 0xD, "INR": 0xE, "DCR": 0xF}
INDIRECT_OPS = {"LD": 0x4, "ST": 0x5, "LDD": 0x6, "STD": 0x7, "POP": 0x8,
                "STP": 0x9, "POPD": 0xC}
BRANCHES = {"BR": 0x1, "BNC": 0x2, "BC": 0x3, "BP": 0x4, "BM": 0x5,
            "BZ": 0x6, "BNZ": 0x7, "BM1": 0x8, "BNM1": 0x9, "BS": 0xC}
ALONE = {"RTN": 0x0, "BK": 0xA, "RS": 0xB}
ORIGIN = 0x0800
PC, SR, CMP, SP = 15, 14, 13, 12


class Error(Exception):
    pass


def number(text, labels=None):
    if labels is not None and text in labels:
        return labels[text]
    if text.startswith("$"):
        return int(text[1:], 16)
    return int(text, 0)


def register(text):
    if text.upper().startswith("R") and text[1:].isdigit() and int(text[1:]) < 16:
        return int(text[1:])
    raise Error(f"{text!r} is not a register")


def assemble(text):
    """Two passes: the first finds the address of every label, the
    second writes the bytes. Besides instructions there is DB, for
    bytes or a "string", and DW, for 16-bit words."""
    lines = []
    for number_, line in enumerate(text.splitlines(), 1):
        line = line.split(";")[0].strip()
        label = None
        if line and line.split()[0].endswith(":"):
            label, line = line.split(":", 1)
            line = line.strip()
        words = line.split(None, 1)
        op = words[0].upper() if words else None
        rest = words[1].strip() if len(words) > 1 else ""
        if op == "DB" and rest.startswith('"') and rest.endswith('"') and len(rest) > 1:
            operands = [str(ord(c)) for c in rest[1:-1]]
        else:
            operands = [w.strip() for w in rest.split(",")] if rest else []
        lines.append((number_, label, op, operands))

    def size(op, operands):
        if op is None:
            return 0
        if op == "DB":
            return len(operands)
        if op == "DW":
            return 2 * len(operands)
        if op == "SET":
            return 3
        if op in BRANCHES:
            return 2
        return 1

    labels = {}
    address = ORIGIN
    for number_, label, op, operands in lines:
        if label:
            labels[label] = address
        address += size(op, operands)

    code = bytearray()
    for number_, label, op, operands in lines:
        try:
            here = ORIGIN + len(code)
            if op is None:
                continue
            if op == "DB":
                code += bytes(number(o, labels) & 0xFF for o in operands)
            elif op == "DW":
                for o in operands:
                    v = number(o, labels) & 0xFFFF
                    code += bytes((v & 0xFF, v >> 8))
            elif op in ALONE and not operands:
                code.append(ALONE[op])
            elif op in BRANCHES and len(operands) == 1:
                distance = number(operands[0], labels) - (here + 2)
                if not -128 <= distance <= 127:
                    raise Error(f"{operands[0]} is too far away")
                code += bytes((BRANCHES[op], distance & 0xFF))
            elif op == "SET" and len(operands) == 2:
                v = number(operands[1], labels) & 0xFFFF
                code += bytes((0x10 | register(operands[0]), v & 0xFF, v >> 8))
            elif op in INDIRECT_OPS and len(operands) == 1 and operands[0].startswith("@"):
                code.append(INDIRECT_OPS[op] << 4 | register(operands[0][1:]))
            elif op in REGISTER_OPS and len(operands) == 1:
                code.append(REGISTER_OPS[op] << 4 | register(operands[0]))
            else:
                raise Error(f"cannot read {op} {', '.join(operands)}")
        except (Error, ValueError) as e:
            raise Error(f"line {number_}: {e}")
    return bytes(code)


class Machine:

    def __init__(self, code):
        self.memory = bytearray(65536)
        self.memory[ORIGIN:ORIGIN + len(code)] = code
        self.r = [0] * 16
        self.r[PC] = ORIGIN
        self.r[SP] = 0x0100     # the subroutine stack grows up from here
        self.prior = 0          # the register the last instruction changed
        self.carry = 0
        self.steps = 0

    def byte(self):
        b = self.memory[self.r[PC]]
        self.r[PC] = (self.r[PC] + 1) & 0xFFFF
        return b

    def word_at(self, a):
        return self.memory[a] | self.memory[(a + 1) & 0xFFFF] << 8

    def put_word(self, a, v):
        self.memory[a] = v & 0xFF
        self.memory[(a + 1) & 0xFFFF] = v >> 8

    def step(self):
        """Run one instruction; return False when the machine stops."""
        r = self.r
        self.steps += 1
        op = self.byte()
        high, n = op >> 4, op & 0xF
        if high == 0:
            if n == 0x0:                                    # RTN
                return False
            if n == 0xA:                                    # BK
                return False
            if n == 0xB:                                    # RS
                r[SP] = (r[SP] - 2) & 0xFFFF
                r[PC] = self.word_at(r[SP])
                return True
            if n > 0xC:
                raise Error(f"unknown instruction {op:02X} at {(r[PC] - 1) & 0xFFFF:04X}")
            d = self.byte()
            d = d - 256 if d > 127 else d
            v = r[self.prior]
            taken = {0x1: True, 0x2: not self.carry, 0x3: bool(self.carry),
                     0x4: v < 0x8000, 0x5: v >= 0x8000, 0x6: v == 0,
                     0x7: v != 0, 0x8: v == 0xFFFF, 0x9: v != 0xFFFF,
                     0xC: True}[n]
            if n == 0xC:                                    # BS
                self.put_word(r[SP], r[PC])
                r[SP] = (r[SP] + 2) & 0xFFFF
            if taken:
                r[PC] = (r[PC] + d) & 0xFFFF
            return True
        if high == 0x1:
            lo = self.byte()
            r[n] = lo | self.byte() << 8
            self.prior = n
        elif high == 0x2:
            r[0] = r[n]
            self.prior = 0
        elif high == 0x3:
            r[n] = r[0]
            self.prior = n
        elif high == 0x4:
            r[0] = self.memory[r[n]]
            r[n] = (r[n] + 1) & 0xFFFF
            self.prior = 0
        elif high == 0x5:
            self.memory[r[n]] = r[0] & 0xFF
            r[n] = (r[n] + 1) & 0xFFFF
            self.prior = 0
        elif high == 0x6:
            r[0] = self.word_at(r[n])
            r[n] = (r[n] + 2) & 0xFFFF
            self.prior = 0
        elif high == 0x7:
            self.put_word(r[n], r[0])
            r[n] = (r[n] + 2) & 0xFFFF
            self.prior = 0
        elif high == 0x8:
            r[n] = (r[n] - 1) & 0xFFFF
            r[0] = self.memory[r[n]]
            self.prior = 0
        elif high == 0x9:
            r[n] = (r[n] - 1) & 0xFFFF
            self.memory[r[n]] = r[0] & 0xFF
            self.prior = 0
        elif high == 0xA:
            total = r[0] + r[n]
            self.carry = int(total > 0xFFFF)
            r[0] = total & 0xFFFF
            self.prior = 0
        elif high == 0xB:
            self.carry = int(r[0] >= r[n])
            r[0] = (r[0] - r[n]) & 0xFFFF
            self.prior = 0
        elif high == 0xC:
            r[n] = (r[n] - 2) & 0xFFFF
            r[0] = self.word_at(r[n])
            self.prior = 0
        elif high == 0xD:
            self.carry = int(r[0] >= r[n])
            r[CMP] = (r[0] - r[n]) & 0xFFFF
            self.prior = CMP
        elif high == 0xE:
            r[n] = (r[n] + 1) & 0xFFFF
            self.prior = n
        elif high == 0xF:
            r[n] = (r[n] - 1) & 0xFFFF
            self.prior = n
        return True


def disassemble(memory, a):
    op = memory[a]
    high, n = op >> 4, op & 0xF
    if high == 0:
        for name, code in list(ALONE.items()) + list(BRANCHES.items()):
            if code == n:
                if name in BRANCHES:
                    d = memory[(a + 1) & 0xFFFF]
                    d = d - 256 if d > 127 else d
                    return f"{name} {(a + 2 + d) & 0xFFFF:04X}"
                return name
        return "?"
    if high == 1:
        return f"SET R{n}, {memory[a + 1] | memory[a + 2] << 8:04X}"
    for name, code in INDIRECT_OPS.items():
        if code == high:
            return f"{name} @R{n}"
    for name, code in REGISTER_OPS.items():
        if code == high:
            return f"{name} R{n}"
    return "?"


def main(args):
    trace = False
    dump = None
    files = []
    while args:
        a = args.pop(0)
        if a == "-t":
            trace = True
        elif a == "-m" and args:
            low, high = args.pop(0).split(":")
            dump = (int(low, 16), int(high, 16))
        else:
            files.append(a)
    if len(files) != 1:
        sys.exit("usage: sweet16.py [-t] [-m from:to] program.s16")
    try:
        with open(files[0]) as f:
            machine = Machine(assemble(f.read()))
        while True:
            if machine.steps >= 1000000:
                raise Error("still running after 1000000 instructions")
            if trace:
                a = machine.r[PC]
                print(f"  {a:04X}  {disassemble(machine.memory, a):14}"
                      f"  R0={machine.r[0]:04X} R1={machine.r[1]:04X} R2={machine.r[2]:04X}"
                      f" R3={machine.r[3]:04X} carry={machine.carry}")
            if not machine.step():
                break
    except Error as e:
        sys.exit(f"sweet16: {e}")
    r = machine.r
    for row in range(4):
        print("  ".join(f"R{4 * row + k:<2} {r[4 * row + k]:04X}" for k in range(4)))
    if dump:
        low, high = dump
        for a in range(low, high + 1, 16):
            chunk = machine.memory[a:min(a + 16, high + 1)]
            text = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            print(f"{a:04X}  {' '.join(f'{b:02X}' for b in chunk):47}  {text}")
    print(f"stopped after {machine.steps} instructions")


if __name__ == "__main__":
    main(sys.argv[1:])
