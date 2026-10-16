"""
CHIP-8, the virtual machine of the COSMAC VIP (1977).

Sixteen 8-bit registers V0 to VF, an address register I, 4 KB of
memory with the program at 0x200, a stack of return addresses, two
timers, and a screen of 64 by 32 pixels, drawn by XOR. Instructions are
two bytes, written as four hexadecimal digits: the first says what,
and the rest are a register (X, Y), a byte (NN) or an address (NNN).

Where later machines changed the meaning of an instruction, this one
does what the VIP did: 8XY6 and 8XYE shift VY into VX, and FX55 and
FX65 move I past what they stored or loaded.

This machine has no window and no keyboard: it runs until the program
jumps to itself, the usual way a CHIP-8 program ends, or waits for a
key, or has run the most instructions it may. Then it prints the
screen. The timers count down once every ten instructions, standing in
for 60 times a second.

A program is a text file of hexadecimal words, one instruction or two
bytes of data to a line; anything after ";" is a comment.

    python3 chip8.py [-t] [-n steps] [-s seed] program.hex
"""

import sys

FONT = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,  0x20, 0x60, 0x20, 0x20, 0x70,
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  0xF0, 0x10, 0xF0, 0x10, 0xF0,
    0x90, 0x90, 0xF0, 0x10, 0x10,  0xF0, 0x80, 0xF0, 0x10, 0xF0,
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  0xF0, 0x10, 0x20, 0x40, 0x40,
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  0xF0, 0x90, 0xF0, 0x10, 0xF0,
    0xF0, 0x90, 0xF0, 0x90, 0x90,  0xE0, 0x90, 0xE0, 0x90, 0xE0,
    0xF0, 0x80, 0x80, 0x80, 0xF0,  0xE0, 0x90, 0x90, 0x90, 0xE0,
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  0xF0, 0x80, 0xF0, 0x80, 0x80,
]
FONT_AT = 0x050
START = 0x200
WIDTH, HEIGHT = 64, 32


class Error(Exception):
    pass


def load(text):
    """The bytes of a program written as hexadecimal words."""
    data = []
    for number, line in enumerate(text.splitlines(), 1):
        for word in line.split(";")[0].split():
            if len(word) != 4:
                raise Error(f"line {number}: {word!r} is not four hexadecimal digits")
            try:
                value = int(word, 16)
            except ValueError:
                raise Error(f"line {number}: {word!r} is not hexadecimal")
            data += [value >> 8, value & 0xFF]
    if START + len(data) > 4096:
        raise Error("program too big")
    return data


def describe(w):
    """What an instruction does, in words, for the trace."""
    x, y = (w >> 8) & 0xF, (w >> 4) & 0xF
    nn, nnn = w & 0xFF, w & 0xFFF
    top = w >> 12
    if w == 0x00E0:
        return "clear the screen"
    if w == 0x00EE:
        return "return"
    if top == 0x1:
        return f"jump {nnn:03X}"
    if top == 0x2:
        return f"call {nnn:03X}"
    if top == 0x3:
        return f"skip if V{x:X} = {nn}"
    if top == 0x4:
        return f"skip if V{x:X} != {nn}"
    if top == 0x5 and w & 0xF == 0:
        return f"skip if V{x:X} = V{y:X}"
    if top == 0x6:
        return f"V{x:X} := {nn}"
    if top == 0x7:
        return f"V{x:X} += {nn}"
    if top == 0x8:
        how = {0: "{x} := {y}", 1: "{x} |= {y}", 2: "{x} &= {y}",
               3: "{x} ^= {y}", 4: "{x} += {y}", 5: "{x} -= {y}",
               6: "{x} := {y} >> 1", 7: "{x} := {y} - {x}",
               0xE: "{x} := {y} << 1"}.get(w & 0xF)
        if how:
            return how.format(x=f"V{x:X}", y=f"V{y:X}")
    if top == 0x9 and w & 0xF == 0:
        return f"skip if V{x:X} != V{y:X}"
    if top == 0xA:
        return f"I := {nnn:03X}"
    if top == 0xB:
        return f"jump {nnn:03X} + V0"
    if top == 0xC:
        return f"V{x:X} := random & {nn}"
    if top == 0xD:
        return f"draw {w & 0xF} rows at V{x:X}, V{y:X}"
    if top == 0xE and nn == 0x9E:
        return f"skip if key V{x:X} is down"
    if top == 0xE and nn == 0xA1:
        return f"skip if key V{x:X} is up"
    if top == 0xF:
        what = {0x07: f"V{x:X} := delay", 0x0A: f"V{x:X} := wait for a key",
                0x15: f"delay := V{x:X}", 0x18: f"sound := V{x:X}",
                0x1E: f"I += V{x:X}", 0x29: f"I := digit V{x:X}",
                0x33: f"decimal digits of V{x:X} at I",
                0x55: f"store V0 to V{x:X} at I",
                0x65: f"load V0 to V{x:X} from I"}.get(nn)
        if what:
            return what
    return "unknown"


class Machine:

    def __init__(self, program, seed=1):
        self.memory = bytearray(4096)
        self.memory[FONT_AT:FONT_AT + len(FONT)] = bytes(FONT)
        self.memory[START:START + len(program)] = bytes(program)
        self.v = [0] * 16
        self.i = 0
        self.pc = START
        self.stack = []
        self.delay = 0
        self.sound = 0
        self.screen = [[0] * WIDTH for _ in range(HEIGHT)]
        self.seed = seed
        self.steps = 0

    def random(self):
        # A small generator of our own, so that runs can be repeated.
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed >> 16 & 0xFF

    def draw(self, x, y, rows):
        """XOR a sprite onto the screen. VF says whether a pixel that
        was on was turned off: the sprite hit something."""
        x %= WIDTH
        y %= HEIGHT
        self.v[0xF] = 0
        for r in range(rows):
            if y + r >= HEIGHT:
                break
            bits = self.memory[(self.i + r) & 0xFFF]
            for c in range(8):
                if x + c >= WIDTH:
                    break
                if bits & (0x80 >> c):
                    if self.screen[y + r][x + c]:
                        self.v[0xF] = 1
                    self.screen[y + r][x + c] ^= 1

    def step(self):
        """Run one instruction. Return a reason to stop, or None."""
        pc = self.pc
        if pc > 4094:
            raise Error(f"no instruction at {pc:03X}")
        w = self.memory[pc] << 8 | self.memory[pc + 1]
        x, y = (w >> 8) & 0xF, (w >> 4) & 0xF
        nn, nnn = w & 0xFF, w & 0xFFF
        v = self.v
        self.pc += 2
        self.steps += 1
        if self.steps % 10 == 0:
            self.delay = max(0, self.delay - 1)
            self.sound = max(0, self.sound - 1)
        top = w >> 12
        if w == 0x00E0:
            self.screen = [[0] * WIDTH for _ in range(HEIGHT)]
        elif w == 0x00EE:
            if not self.stack:
                raise Error(f"return with no call at {pc:03X}")
            self.pc = self.stack.pop()
        elif top == 0x1:
            if nnn == pc:
                return "the program jumped to itself"
            self.pc = nnn
        elif top == 0x2:
            if len(self.stack) == 16:
                raise Error(f"too many calls at {pc:03X}")
            self.stack.append(self.pc)
            self.pc = nnn
        elif top == 0x3:
            if v[x] == nn:
                self.pc += 2
        elif top == 0x4:
            if v[x] != nn:
                self.pc += 2
        elif top == 0x5 and w & 0xF == 0:
            if v[x] == v[y]:
                self.pc += 2
        elif top == 0x6:
            v[x] = nn
        elif top == 0x7:
            v[x] = (v[x] + nn) & 0xFF
        elif top == 0x8 and w & 0xF in (0, 1, 2, 3):
            v[x] = [v[y], v[x] | v[y], v[x] & v[y], v[x] ^ v[y]][w & 0xF]
        elif top == 0x8 and w & 0xF == 4:
            total = v[x] + v[y]
            v[x] = total & 0xFF
            v[0xF] = int(total > 0xFF)
        elif top == 0x8 and w & 0xF == 5:
            borrow = v[x] < v[y]
            v[x] = (v[x] - v[y]) & 0xFF
            v[0xF] = int(not borrow)
        elif top == 0x8 and w & 0xF == 6:
            bit = v[y] & 1
            v[x] = v[y] >> 1
            v[0xF] = bit
        elif top == 0x8 and w & 0xF == 7:
            borrow = v[y] < v[x]
            v[x] = (v[y] - v[x]) & 0xFF
            v[0xF] = int(not borrow)
        elif top == 0x8 and w & 0xF == 0xE:
            bit = v[y] >> 7
            v[x] = (v[y] << 1) & 0xFF
            v[0xF] = bit
        elif top == 0x9 and w & 0xF == 0:
            if v[x] != v[y]:
                self.pc += 2
        elif top == 0xA:
            self.i = nnn
        elif top == 0xB:
            self.pc = (nnn + v[0]) & 0xFFF
        elif top == 0xC:
            v[x] = self.random() & nn
        elif top == 0xD:
            self.draw(v[x], v[y], w & 0xF)
        elif top == 0xE and nn == 0x9E:
            pass                            # no key is ever down
        elif top == 0xE and nn == 0xA1:
            self.pc += 2
        elif top == 0xF and nn == 0x07:
            v[x] = self.delay
        elif top == 0xF and nn == 0x0A:
            self.pc = pc
            return "the program waits for a key"
        elif top == 0xF and nn == 0x15:
            self.delay = v[x]
        elif top == 0xF and nn == 0x18:
            self.sound = v[x]
        elif top == 0xF and nn == 0x1E:
            self.i = (self.i + v[x]) & 0xFFF
        elif top == 0xF and nn == 0x29:
            self.i = FONT_AT + 5 * (v[x] & 0xF)
        elif top == 0xF and nn == 0x33:
            for k, digit in enumerate((v[x] // 100, v[x] // 10 % 10, v[x] % 10)):
                self.memory[(self.i + k) & 0xFFF] = digit
        elif top == 0xF and nn == 0x55:
            for k in range(x + 1):
                self.memory[(self.i + k) & 0xFFF] = v[k]
            self.i = (self.i + x + 1) & 0xFFF
        elif top == 0xF and nn == 0x65:
            for k in range(x + 1):
                v[k] = self.memory[(self.i + k) & 0xFFF]
            self.i = (self.i + x + 1) & 0xFFF
        else:
            raise Error(f"unknown instruction {w:04X} at {pc:03X}")
        return None

    def picture(self):
        return "\n".join("".join("#" if p else "." for p in row) for row in self.screen)


def main(args):
    trace = False
    limit = 100000
    seed = 1
    files = []
    while args:
        a = args.pop(0)
        if a == "-t":
            trace = True
        elif a == "-n" and args:
            limit = int(args.pop(0))
        elif a == "-s" and args:
            seed = int(args.pop(0))
        else:
            files.append(a)
    if len(files) != 1:
        sys.exit("usage: chip8.py [-t] [-n steps] [-s seed] program.hex")
    try:
        with open(files[0]) as f:
            machine = Machine(load(f.read()), seed)
        why = f"it ran {limit} instructions"
        while machine.steps < limit:
            if trace:
                pc = machine.pc
                w = machine.memory[pc] << 8 | machine.memory[pc + 1]
                registers = " ".join(f"{r:02X}" for r in machine.v)
                print(f"  {pc:03X}  {w:04X}  {describe(w):28} I={machine.i:03X}  {registers}")
            reason = machine.step()
            if reason:
                why = reason
                break
        print(machine.picture())
        print(f"stopped after {machine.steps} instructions: {why}")
    except Error as e:
        sys.exit(f"chip8: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
