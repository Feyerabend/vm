# C: CHIP-8

In 1977, RCA sold the COSMAC VIP, a small computer kit built around its
1802 processor. To make it easy to write games for, Joseph Weisbecker
designed CHIP-8: a virtual machine, with its interpreter in the VIP's
first 512 bytes of memory. That is why CHIP-8 programs still start at
address 0x200. Programs were typed in as hexadecimal, and a game such
as Pong fitted in a few hundred bytes.

CHIP-8 outlived its computer. It was carried to the HP-48 graphing
calculators in 1990, and from there to almost every computer since:
writing a CHIP-8 interpreter is one of the most common first projects
in emulation. ([`archive/chip8`](../../archive/chip8) has one in C, by
Dustin Roepsch, which draws on the terminal and takes the keyboard.)

## The machine

[`chip8.py`](chip8.py) is the whole machine, about 300 lines. It has:

- 4096 bytes of memory, with the program at 0x200 and a font of the
  sixteen hexadecimal digits at 0x050;
- sixteen 8-bit registers, `V0` to `VF`, and a 12-bit address
  register `I`;
- a stack of up to sixteen return addresses;
- two timers, which count down 60 times a second;
- a screen of 64 by 32 pixels, and sixteen keys.

Every instruction is two bytes, read as four hexadecimal digits: the
first says what to do, the rest are a register (`X`, `Y`), a byte
(`NN`) or an address (`NNN`). `6XNN` puts `NN` in `VX`, `8XY4` adds
`VY` to `VX`, `DXYN` draws. There are 35 of them.

This version has no window and no keys. It runs until the program
jumps to itself (the usual way a CHIP-8 program ends), and prints the
screen. Here is [`samples/answer.hex`](samples/answer.hex), which works
out six times seven by adding, since CHIP-8 has no multiplication:

```
....................####.#..#.####..............................
....................#..#.#..#....#..............................
....................#..#.####.####..............................
....................#..#....#.#.................................
....................####....#.####..............................
```

There is no instruction to print a number. `FX33` splits `VX` into its
three decimal digits in memory, `FX29` points `I` at the font's picture
of a digit, and `DXYN` draws it.

## Drawing by XOR

`DXYN` draws a sprite: `N` bytes from memory at `I`, each a row of
eight pixels. It does not just set pixels: it flips them. And if any
pixel that was on is turned off, `VF` becomes 1.

That one rule does two jobs. A sprite is erased by drawing it again,
so moving one is drawing it twice. And `VF` tells a game that two
things have collided, with no extra code.
[`samples/collide.hex`](samples/collide.hex) draws a block twice,
overlapping: the overlap goes dark, and `VF`, drawn on the right, is 1.

```
........####....####......................#.....................
........####....####.....................##.....................
```

## Compared with ours

CHIP-8 is a register machine with a stack only for return addresses.
Its instructions are fixed in size and packed tightly, with registers
in the instruction itself, as in chapter 17's register machine. And
its instruction set is chosen for its use: drawing, keys, timers and
decimal digits are built in, and there is no multiplication.

The deeper difference is that CHIP-8 has no specification. The VIP's
interpreter *was* the definition. When CHIP-8 was rewritten for the
HP-48, a few instructions came out differently: `8XY6`, which shifted
`VY` into `VX`, became a shift of `VX` itself, and `FX55` and `FX65`
moved `I` differently, and later not at all. Programs written for
one version break on the other, and to this day a CHIP-8 interpreter
needs settings for these *quirks*. This one does what the VIP did.

Chapter 8 exists to prevent exactly this. A written specification,
and a suite of tests that every machine must pass, would have caught
the difference the day the second interpreter was written.

## Run it

```
make test
python3 chip8.py samples/answer.hex
python3 chip8.py -t samples/answer.hex
```

With `-t`, the machine shows every instruction, in words, with `I`
and the registers. `-n` sets how many instructions it may run, and
`-s` seeds the random numbers of `CXNN`, so that a run can be
repeated.

## Exercises

1. Write an assembler for CHIP-8, so that `samples/answer.hex` can be
   written as `V0 := 0`, `loop: V0 += 6`, and so on. (Octo, a popular
   CHIP-8 environment, has a language much like this.)
2. Add a setting for the HP-48 quirks, and write a program that shows
   the difference.
3. Give the machine a window and keys. With Python's `curses` module
   it can run in a terminal, as the C version in the archive does. Then
   run a real game, from one of the collections of public domain
   CHIP-8 programs.
4. CHIP-8 has no traps: on the VIP, an unknown instruction did whatever
   the interpreter happened to do with it (this one stops). Which of
   chapter 4's traps would make sense for CHIP-8, and which would
   break existing programs?
