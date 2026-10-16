# Chapter 17: Registers

A stack machine's instructions are small because they name nothing.
`ADD` does not say what to add or where to put the result: the stack
says. The price is that values must be moved onto the stack before
they are used and off it afterwards. Here is one round of
`bench/loop.asm`, thirteen instructions:

```
loop:   LOAD 0
        JZ done
        LOAD 1
        LOAD 0
        PUSH 7
        AND
        ADD
        STORE 1
        LOAD 0
        PUSH 1
        SUB
        STORE 0
        JMP loop
```

A *register machine* names its operands. Here is the same round:

```
S4:     JZ r0, S27
        ANDI r3, r0, 7
        ADD r1, r1, r3
        SUBI r0, r0, 1
        JMP S4
```

Five instructions. Each is bigger, but there are far fewer of them,
and every one does real work. Lua, Dalvik (Android's original virtual
machine) and the BEAM (Erlang's) are register machines; the JVM,
.NET, CPython and WebAssembly are stack machines. Which is better was
argued for decades, and this chapter measures it on our own machine.

## From stack to registers

Nobody wrote the register code above. [`translate.py`](translate.py)
made it from the stack code, in two stages.

**Stage one: slots become registers.** In a well-behaved program, the
stack is equally deep at an instruction whichever way the program got
there. If the depth is known before running, "the top of the stack"
at an instruction where the depth is 5 just means "slot 4", and slot
k can be called register k:

```
LOAD 0      depth 2 -> 3      MOV  r2, r0
LOAD 1      depth 3 -> 4      MOV  r3, r1
ADD         depth 4 -> 3      ADD  r2, r2, r3
STORE 1     depth 3 -> 2      MOV  r1, r2
```

Working out the depths is a *data-flow analysis*. Start at address 0
with depth 0, and at each function, the target of a `CALL`, with depth
equal to its number of arguments. Follow every path, adding up each
instruction's effect on the depth. Where two paths meet, they must
agree. This gives as many register instructions as there were stack
instructions, minus the `DROP`s, which become nothing.

**Stage two: remove the copying.** Within each straight run of code:

- *Copy propagation*: after `MOV r2, r0`, a later read of r2 can read
  r0 directly, if neither has changed in between.
- *Constants*: after `MOVI r4, 7`, `AND r3, r3, r4` can be
  `ANDI r3, r3, 7`, with the 7 inside the instruction.
- *Dead code*: a `MOV` into a register nobody reads again can go.
  Which registers might still be read? The stack discipline answers
  for free: those below the depth at that point. Everything at or
  above it was popped.
- *Coalescing*: `ADD r2, r1, r3` followed by `MOV r1, r2` is
  `ADD r1, r1, r3`.

`translate.py -l` shows the result, and `-naive` skips stage two.

## What is refused

Some programs have no register translation:

- a program where the depth at some point depends on the path taken
  ([`tests/shared.asm`](tests/shared.asm));
- code shared between two functions, which would need two window sizes;
- a jump into the middle of an instruction;
- `CALLI`: its target is a value computed while the program runs, so
  where functions begin cannot be known in advance.

Everything else is translated, *including* programs that are certain
to trap. An `ADD` reached with one value in the frame becomes a `TRAP`
instruction with the stack machine's message, and every register
instruction carries the address of the stack instruction it came from.
So traps report the same thing on both machines, and the conformance
suite of chapter 8 tests the pair:

```
./rvm-run: 66 of 71 passed
  calli: a known failure
  garbage: a known failure
  trap-calli-address: a known failure
  trap-calli-args: a known failure
  trap-calli-reference: a known failure
```

The five known failures are the four `CALLI` programs, refused, and
`garbage`: the register machine has chapter 13's heap, without a
collector. Twelve real programs, compiled by the enkel/0 and basal/0
compilers of chapters 10 and 11, give exactly the same output on both
machines.

## The register machine

[`rvm.c`](rvm.c). Each instruction is five numbers: an opcode, three
operands, and the address it came from. Registers are numbered within
a *window*, the current call's part of a register file of 256. A call
`CALL f, window r2, size 4` starts the new window at the caller's r2,
exactly where the arguments are, so passing arguments copies nothing.
The result comes back in the first register of the window, which is
the caller's r2. Lua does the same.

## Measured

Instructions run, counted with `-c`:

|       | stack | register, naive | register |
|-------|------:|----------------:|---------:|
| fib   | 26,925,370 | 26,925,370 | 14,808,955 |
| loop  | 260,000,007 | 260,000,007 | 100,000,005 |
| sieve | 33,826,936 | 33,826,406 | 17,152,655 |

Time, best of three, milliseconds, built with Clang 18 `-O2`:

|       | stack | register, naive | register |
|-------|------:|----------------:|---------:|
| fib   |  76 |  75 |  41 |
| loop  | 607 | 595 | 236 |
| sieve |  96 |  81 |  37 |

With GCC 13 the register machine wins by about the same factor, and
the naive translation already gains more.

Half the instructions, and two to three times as fast. This matches
the classic study, *Virtual Machine Showdown: Stack versus Registers*
by Shi, Gregg, Beatty and Ertl (2005), which found about 47 percent
fewer instructions and a clear gain in time, despite bigger code.

Part of the gain is not about registers at all. The register machine
checks nothing about its stack while running: no underflow, no
`LOAD` outside the frame. The translator proved, before running, that
those cannot happen. That idea is worth a chapter of its own:
chapter 19.

Not every program gains as much. basal/0 code keeps its variables in
memory, through `LOADM` and `STOREM`, and registers do nothing for
that: `basal-table` runs 22 percent fewer instructions, `enkel-bits`
48 percent fewer.

## Run it

```
make test
make bench
```

## Exercises

1. Copy propagation works only within a straight run of code. In
   `fib`, which copies does it miss because of that?
2. Add `JLT r1, r2, label`, a compare-and-jump, and make the translator
   use it for `LT` followed by `JZ`. How many instructions does `loop`
   run now?
3. The register machine needs no `DUP`, `SWAP` or `DROP` in its code.
   Count, in the samples, how many stack instructions only move values
   around. What fraction of a stack machine's work is that?
4. Let enkel/0 compile straight to register code, without the stack
   machine in between. What does the compiler need to decide that the
   stack machine decided for it?
