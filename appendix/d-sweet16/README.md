# D: SWEET16

The 6502 processor of the Apple II is an 8-bit processor, and doing
anything with 16-bit numbers, such as addresses, takes many
instructions: add the low bytes, then the high bytes with the carry,
and store each separately. In 1977 Steve Wozniak, writing Integer
BASIC for the Apple II, got tired of that, and wrote himself a better
processor: SWEET16, a 16-bit machine interpreted by about 300 bytes of
6502 code in the Apple II's ROM.[^1]

What makes SWEET16 unusual is how it was used. A 6502 program calls
`SWEET16` as a subroutine, and the bytes that follow the call are
SWEET16 code, not 6502 code. When the SWEET16 code says `RTN`, the
interpreter returns to running 6502 code after it. A program changes
machines in the middle of a routine: native code where speed matters,
SWEET16 where 16-bit work makes the native code long.

## The machine

[`sweet16.py`](sweet16.py) is the machine and an assembler for it. It
has sixteen 16-bit registers (on the Apple II, they lived in the first
32 bytes of memory). Some have jobs: `R0` is the accumulator, `R12`
the stack pointer for subroutine calls, `R13` gets the result of a
compare, and `R15` is the program counter.

Most instructions are one byte. The high four bits say what to do, and
the low four which register:

| Code | Instruction | Does |
|------|-------------|------|
| `1n` | `SET Rn, v` | `Rn := v` (two more bytes) |
| `2n`, `3n` | `LD Rn`, `ST Rn` | `R0 := Rn`, `Rn := R0` |
| `4n`, `5n` | `LD @Rn`, `ST @Rn` | a byte to or from the address in `Rn`, then `Rn += 1` |
| `6n`, `7n` | `LDD @Rn`, `STD @Rn` | the same with a 16-bit word, then `Rn += 2` |
| `8n`, `9n`, `Cn` | `POP @Rn`, `STP @Rn`, `POPD @Rn` | back down: `Rn` first, then the byte or word |
| `An`, `Bn` | `ADD Rn`, `SUB Rn` | `R0 += Rn`, `R0 -= Rn` |
| `Dn` | `CPR Rn` | `R13 := R0 - Rn`, to compare |
| `En`, `Fn` | `INR Rn`, `DCR Rn` | `Rn += 1`, `Rn -= 1` |

Codes `00` to `0C` are `RTN`, the branches, and `BS` and `RS` to call
and return. A branch is two bytes: the code, and a distance, from -128
to 127, from the next instruction.

The auto-increment is where SWEET16 saves the most. Here is the loop
that copies a block of bytes, from
[`samples/copy.s16`](samples/copy.s16):

```
copy:   LD @R1          ; R0 := the byte at R1, and move R1 on
        ST @R2          ; the byte at R2 := R0, and move R2 on
        DCR R3
        BNZ copy
```

Five bytes. On the 6502, with 16-bit addresses and a 16-bit count, the
same loop is several times as long.

## The prior result

`BNZ` above does not say which register to test. SWEET16 remembers
which register the last instruction changed, the *prior result*, and
the branches test that: after `DCR R3`, `BNZ` tests `R3`. After an
arithmetic instruction it is `R0`; after `CPR`, `R13`. `BC` and `BNC`
test the carry, which `ADD`, `SUB` and `CPR` set.
[`samples/fib.s16`](samples/fib.s16) uses the carry to stop when a
Fibonacci number grows past 16 bits.

The original kept the prior result and the carry in `R14`; this
version keeps them apart, but the branches do the same.

## Compared with ours

SWEET16 makes the trade of chapters 16 and 20 the other way round.
Those chapters made the machine faster, in the end by turning
programs into native code. SWEET16 is much slower than the 6502 code
it replaces, and that is accepted: what it buys is *size*, on a
computer whose ROM had room for very little. Dense code was also the
p-System's reason for p-code (study B), and one byte per instruction,
with the register packed into it, is how SWEET16 gets there. Our
instructions are 32-bit words, which is simple, and roomy.

The way it is entered is chapter 21's *embedding* taken to its
extreme. Our WebAssembly core is called by a host through a few
functions. SWEET16's host and its programs are mixed in the same
stream of bytes, and the processor changes machines at a call.

And its conditions are a third design, next to ours and CHIP-8's. Our
`JZ` tests the value on top of the stack, and pops it. CHIP-8 has no
conditional jumps, only instructions that skip the next one. SWEET16
remembers where the last result went, as real processors do with
condition flags.

## Run it

```
make test
python3 sweet16.py -m 0900:090F samples/copy.s16
python3 sweet16.py -t samples/copy.s16
```

When the program ends, the machine shows the registers, and with `-m`
the memory between two addresses, in hexadecimal. `samples/fib.s16`
writes its table as 16-bit words, low byte first, as the 6502 does:
`90 00 E9 00` are 144 and 233. With `-t`, it shows every
instruction.

## Exercises

1. SWEET16 has no shifts, so no fast multiplication. Write a 16-bit
   multiply with `ADD R0`-style doubling, and a subroutine. How many
   instructions does 300 times 200 take?
2. SWEET16 cannot print: on the Apple II, the 6502 code around it
   did. Give it a way out to the host, using the unused code `0D` to
   print `R0` in decimal, and print the table of `samples/fib.s16`.
   Would it have been better to return to the host with `RTN`, and
   let it print?
3. The original used one trick to save space in its dispatch: it
   pushed the address of the routine for an instruction on the 6502's
   stack, and "returned" to it. Find out how, and why it is shorter
   than a table of jumps.
4. Write SWEET16 in C, with the registers in an array of bytes, as on
   the Apple II. Is the prior result easier to keep as a register
   number, or as an address?

[^1]: Steve Wozniak, "SWEET16: The 6502 Dream Machine", *BYTE*,
November 1977.
