# Chapter 4: Traps

Until now, "what happens if..." had only one answer: *whatever the C
underneath happens to do*. Pop an empty stack and the machine reads
whatever lies before the array. Jump to address 1000 in a twenty-word
program and it runs whatever is there. Sometimes it crashes, sometimes
it prints nonsense, and sometimes, worst of all, it seems to work.

A *trap* replaces all of that with one rule: before doing anything
that could go wrong, check; if it would go wrong, stop, and say what
and where.

```
$ ./vm divzero
trap: division by zero at 4
```

The address is the start of the instruction that failed, not wherever
`pc` has moved on to, because that is the address a person debugging
the program needs.

## What is checked

| Trap | When |
|------|------|
| stack overflow | a push onto a full stack |
| stack underflow | a pop below the current frame |
| too many nested calls | a `CALL` with all frames in use |
| not enough arguments | `CALL addr n` with fewer than n values in the frame |
| no such local | `LOAD k` or `STORE k` outside the current frame |
| return without call | `RET` at the top level |
| division by zero | `DIV` or `MOD` by 0 |
| unknown instruction | an opcode the machine does not have |
| jump out of program | a `JMP`, `JZ` or `CALL` target outside the code |
| missing operand | an instruction cut off by the end of the code |
| ran off the end of the program | `pc` leaves the code without a `HALT` |

*Stack underflow* is checked against the current frame, not against
the bottom of the stack. A function cannot pop its caller's values,
even by accident. This is a choice; chapter 3's machine would have let
it.

## The cost

Every instruction now does extra comparisons, so the machine is
slower. How much that costs is measured in chapter 19. Chapter 19 shows
another way: check a program *once*, before it runs, and leave out
most of the checks while it runs. That is what the Java Virtual
Machine's verifier does.

## New instructions

| Code | Name | Effect |
|------|------|--------|
| 19   | DIV  | a b -> a / b, rounded toward zero; trap if b = 0 |
| 20   | MOD  | a b -> a % b, with the sign of a; trap if b = 0 |

## Run it

`./vm` runs Euclid's algorithm. `./vm divzero`, `./vm deep` and the
others run programs that are broken on purpose; the list is at the
bottom of [`vm.c`](vm.c).

```
make test
```

The test checks that the good program prints the right numbers, and
that every broken one stops with exit status 1 and the right message.

## Exercises

1. `ADD` and `MUL` can overflow a C `int`, and in C that is undefined
   behaviour. Make them trap instead. (Hint: `__builtin_add_overflow`
   in GCC and Clang, or check before adding.)
2. `INT_MIN / -1` also overflows. Find it, then trap on it.
3. Some languages prefer to *recover* from errors rather than stop.
   What would the machine need so that a program could catch a
   division by zero itself?
