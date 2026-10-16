# The machine: specification, version 2

This document says what the machine does. An implementation that
does something else is wrong, however sensible its own behaviour may
seem. Where this document is silent, the machine's behaviour is not
specified, and a program that depends on it is wrong.

The two implementations in this chapter, [`vm.c`](vm.c) and
[`vm.py`](vm.py), follow it. The test suite in [`suite/`](suite)
checks that they do.

Version 2 adds memory and the instructions `AND`, `OR`, `XOR`,
`LOADM`, `STOREM` and `EMIT` (codes 21 to 26). Everything in
version 1 is unchanged, so a version 1 program behaves the same,
unless it relied on codes 21 to 26 trapping as unknown instructions.
The file format is unchanged too.


## 1. Values

A *value* is a signed 32-bit integer, from −2147483648 to 2147483647.

Arithmetic *wraps*: a result is reduced into that range modulo 2³².
So 2147483647 + 1 gives −2147483648, and 65536 × 65536 gives 0.


## 2. The state of the machine

| Part | What it is |
|------|------------|
| code | a sequence of n values, at addresses 0 to n − 1, fixed when the program is loaded |
| pc | the address of the next instruction, initially 0 |
| stack | a sequence of at most 256 values, initially empty; its last element is the *top* |
| frames | a sequence of at most 256 frames, initially empty |
| fp | the frame pointer: a position in the stack, initially 0 |
| memory | 4096 values, at addresses 0 to 4095, initially all 0 |

A *frame* is a pair (*return address*, *saved fp*).

The values on the stack at positions fp and above belong to the
current call; they are its *locals*, and local k is the value at
position fp + k. Positions below fp belong to callers and cannot be
reached.


## 3. Running

The machine repeats the following until it halts or traps:

1. If pc is not an address in the code, trap: *ran off the end of
   the program*.
2. Let *start* = pc. Read the value at pc as the *opcode*, and add 1
   to pc.
3. Carry out the instruction with that opcode, as given in section 5.
   If there is none, trap: *unknown instruction*.

When the machine halts, it exits with status 0.


## 4. Basic operations

The instructions in section 5 are described in terms of these
operations. Each either succeeds or traps.

**operand**: if pc is not an address in the code, trap: *missing
operand*. Otherwise the result is the value at pc, and pc increases
by 1.

**address**: take an operand. If it is not an address in the code,
trap: *jump out of program*. Otherwise it is the result.

**push v**: if the stack holds 256 values, trap: *stack overflow*.
Otherwise append v.

**pop**: if the stack holds exactly fp values (the current call has
no locals left), trap: *stack underflow*. Otherwise remove the top
value; it is the result.

The steps of an instruction happen in the order given, and the first
one to trap ends the instruction. Order matters: `JZ 9999` traps with
*jump out of program* even when the stack is empty, because the
address is taken before anything is popped.


## 5. Instructions

`a b` means: pop b, then pop a. So for `SUB`, a is the value that was
under the top, and b the value that was on top.

| Code | Name  | Steps |
|------|-------|-------|
| 0    | HALT  | Halt. |
| 1    | PUSH  | n = operand; push n. |
| 2    | ADD   | pop b, pop a; push a + b, wrapped. |
| 3    | SUB   | pop b, pop a; push a − b, wrapped. |
| 4    | MUL   | pop b, pop a; push a × b, wrapped. |
| 5    | PRINT | pop a; write a in decimal, with a leading `-` if negative, then a newline, to standard output. |
| 6    | JMP   | t = address; pc = t. |
| 7    | JZ    | t = address; pop a; if a = 0, pc = t. |
| 8    | DUP   | pop a; push a; push a. |
| 9    | DROP  | pop a. |
| 10   | SWAP  | pop b, pop a; push b; push a. |
| 11   | OVER  | pop b, pop a; push a; push b; push a. |
| 12   | ROT   | pop c, pop b, pop a; push b; push c; push a. |
| 13   | LT    | pop b, pop a; push 1 if a < b, else 0. |
| 14   | EQ    | pop b, pop a; push 1 if a = b, else 0. |
| 15   | LOAD  | k = operand; if k < 0, or fp + k is not a position in the stack, trap: *no such local*; push local k. |
| 16   | STORE | k = operand; pop a; if k < 0, or fp + k is not a position in the stack, trap: *no such local*; local k = a. |
| 17   | CALL  | t = address; n = operand; if n < 0, or the current call has fewer than n locals, trap: *not enough arguments*; if there are 256 frames, trap: *too many nested calls*; add the frame (pc, fp); fp = (size of stack) − n; pc = t. |
| 18   | RET   | if there are no frames, trap: *return without call*; pop a; remove every value from position fp up; remove the last frame (r, f) and set pc = r, fp = f; push a. |
| 19   | DIV   | pop b, pop a; if b = 0, trap: *division by zero*; push the quotient a ÷ b rounded towards zero, wrapped. |
| 20   | MOD   | pop b, pop a; if b = 0, trap: *division by zero*; push a − b × q, where q is the quotient of `DIV`, wrapped. |
| 21   | AND   | pop b, pop a; push the bitwise *and* of a and b, as 32-bit two's complement values. |
| 22   | OR    | pop b, pop a; push the bitwise *or*. |
| 23   | XOR   | pop b, pop a; push the bitwise *exclusive or*. |
| 24   | LOADM | pop a; if a is not a memory address, trap: *no such memory address*; push the value at memory address a. |
| 25   | STOREM | pop v, pop a; if a is not a memory address, trap: *no such memory address*; store v at memory address a. |
| 26   | EMIT  | pop a; if a < 0 or a > 255, trap: *not a character*; write the single byte a to standard output. |

Some consequences, all checked by the suite:

- `DIV` rounds towards zero: −7 ÷ 2 is −3, and −7 `MOD` 2 is −1. The
  remainder has the sign of a.
- −2147483648 ÷ −1 is 2147483648, which wraps to −2147483648; the
  remainder is 0.
- In `CALL t n`, the n values on top of the stack become locals 0 to
  n − 1 of the called function, with the deepest as local 0.
- `RET` discards everything the call left on the stack, including its
  arguments, and gives the caller exactly one value.
- `STORE` pops before it checks, so `STORE 0` with a single value in
  the frame traps: after the pop, there is no local 0 left to store
  into.
- Memory belongs to no call. A value stored by one function can be
  loaded by any other, and survives every `RET`.
- `STOREM` takes the address from under the value: push the address
  first, then compute the value, then `STOREM`.
- `EMIT` writes a byte, not a character in any particular encoding.
  `PRINT` and `EMIT` write to the same standard output, in the order
  they run.


## 6. Traps

A trap stops the machine. It writes

```
trap: <reason> at <start>
```

to standard error, where *reason* is the text given in italics above
and *start* is the address of the instruction that trapped. Anything
already written to standard output stays written, and appears before
the trap message when the two go to the same place. The machine exits
with status 1.


## 7. Program files

A program is loaded from a file in the format of
[`ch05-files/FORMAT.md`](../ch05-files/FORMAT.md). If the file cannot
be opened, or breaks that format, the machine writes

```
<path>: <reason>
```

to standard error, where *path* is the file name as given and
*reason* is one of: *cannot open*, *too short to be a program*,
*not a program (wrong magic number)*, *unknown format version*,
*bad code length*, *code ends early*, *extra bytes after the code*.
It exits with status 2, without running anything.

The checks are made in the order of that list.


## 8. Tracing

An implementation may offer tracing with `-t`. If it does, then after
each instruction that does not trap, including the final `HALT`, it
writes one line to standard error:

- the step number, counting from 1, right-aligned in 6 characters,
- a space, then the instruction's start address, right-aligned in 5,
- two spaces, then the instruction: its name and its operands,
  separated by single spaces,
- then, if the stack is not empty or there is at least one frame:
  spaces to fill the instruction out to 14 characters (none if it is
  already longer), two more spaces, and the stack.

Memory is not shown. The stack is written bottom first, values separated by single spaces,
with a `|` before the first value of each call's locals. A call with
no locals still gets its `|`, at the position where its locals would
begin.

Before writing each line, the machine flushes standard output, so
that a program's output and its trace interleave correctly.


## 9. What is left unspecified

- How the machine is started, and its messages for wrong usage.
- The `-d` debugger of [`vm.c`](vm.c).
- What happens if a value written to standard output cannot be
  written.
