# Chapter 20: Native code

An interpreter, however good, spends much of its time on the same
small job: fetch the next instruction, find out what it is, jump to
the code for it. Chapters 16 to 19 made that cheaper. This chapter
removes it, by translating the program, once, into the processor's
own code. That is what a JIT compiler does while a program runs, and
what an ahead-of-time compiler does before.

This chapter does it ahead of time, and through C. [`vm2c.py`](vm2c.py)
turns a `.vm` file into a C program, and a C compiler turns that into
native code. Going through C means the result runs wherever there is
a C compiler: on an x86 PC, on an ARM Mac, on a Raspberry Pi. A JIT
that writes machine code itself must be written again for each kind
of processor. Compiling to C is how early C++ (Cfront), Nim, Chicken
Scheme and many others began.

## From instructions to C

Every instruction becomes the C code the interpreter would have run
for it, with its operands written in as constants, behind a label
named after its address:

```c
A12: start = 12;                        /* JZ 17 */
    { struct value v = pop(); if (!v.is_ref && v.n == 0) goto A17; }
    goto A14;
A14: start = 14;                        /* LOAD 0 */
    push(stack[local_at(0)]);
    goto A16;
```

A jump to a known address is a `goto`. After `RET` and `CALLI`, where
the address is known only while running, the code goes through a
`switch` on it. Nothing else is left of the interpreter: no loop, no
fetching, no decoding.

The machine's state and everything that can fail come from
[`runtime.h`](runtime.h), which is chapter 19's interpreter with its
run loop taken out: the same values and tags, the same stack and
frames, both garbage collectors, the same arithmetic, the same
`trap()`. So a compiled program fails exactly as the interpreted one
does, with the same message, at the same address.

Two details keep that exact:

- **Every address gets a label**, not only those where an instruction
  starts when the program is read from the beginning. A program may
  jump into the middle of an instruction, and the specification says
  what happens then.
- **A damaged file** is reported by `vm2c.py` word for word as the
  machine would report it.

## The same machine, proved again

[`vmc`](vmc) compiles a program, compiles the C, and runs the result,
so the whole chain can be tested as if it were a machine:

```
./vmc: 71 of 71 passed
./vmc -g copy -S: 71 of 71 passed
```

Every program in the conformance suite of chapter 8, as extended
since, compiled to native code: same output, same traps at the same
addresses, same exit status, with both collectors and under stress.

## Verified programs need fewer checks

A program that passes the analysis of chapters 17 and 19, in
[`flow.py`](flow.py), with no instruction that is certain to trap, is
compiled without the checks the analysis made. Pops do not test for
underflow, `LOAD` and `STORE` do not test their locals, `RET` does not
test for a frame, and only the instructions that can be reached get
any code. Programs that do not verify, such as those using `CALLI`,
get every check. `vm2c.py -C` puts every check in anyway.

## Measured

Native code against the fastest interpreter so far, chapter 19's,
which itself verifies and leaves out checks. Best of five,
milliseconds:

Built with Clang 18, `-O2`:

|             | interpreted | native | faster |
|-------------|------:|------:|------:|
| fib         |  41 |  14 |  2.8× |
| loop        | 848 |  50 | 16.7× |
| sieve       |  53 |  15 |  3.4× |
| closures    |  57 |  42 |  1.3× |
| enkel-sieve | 153 |   7 | 20.4× |
| basal-loop  |  30 |   8 |  3.5× |

Built with GCC 13, `-O2`:

|             | interpreted | native | faster |
|-------------|------:|------:|------:|
| fib         |  72 |  35 |  2.0× |
| loop        | 742 | 267 |  2.7× |
| sieve       |  82 |  58 |  1.4× |
| closures    | 134 | 113 |  1.1× |
| enkel-sieve | 154 |  37 |  4.1× |
| basal-loop  |  40 |  16 |  2.4× |

The biggest gains are in loops of plain arithmetic, where a C
compiler can see the whole loop at once: it keeps the stack pointer
in a register, and removes checks it can prove redundant from one
instruction to the next. `closures` gains least. Every call there
goes through `CALLI` and the `switch`, which the C compiler cannot see
through, and most of its time is spent making blocks and collecting
them, which compiling does not change.

And the C compiler matters enormously. On this kind of code, a long
function full of `goto`s and small checks, Clang does far better than
GCC. Telling both that `trap()` never returns changed nothing
measurable; finding out why GCC does not keep `sp` in a register here
would be a study of its own.

## What a JIT would add

A JIT compiles while the program runs. It can wait to see which code
is *hot*, and compile only that; it can see which values actually
arrive, and compile code specialised for them, with a cheap check
that falls back to the interpreter if they ever change. That is how
the JVM's HotSpot, V8 and LuaJIT reach speeds near C. The price is a
compiler inside the machine, writing machine code for one particular
processor. Exercise 3 starts one.

## Run it

```
make test
make bench
make NATIVE_CFLAGS="-O2" CC=clang bench
```

## Exercises

1. Keep the top few stack values in C local variables instead of in
   `stack[]`, for verified code, where the depth at each instruction
   is known. (What must happen before a call, or a garbage
   collection?) How much faster is `loop`?
2. Compile `CALL`s to known functions into C function calls, and
   `RET` into `return`. What does this do for `fib`? What happens to
   `frames[]`?
3. Write a small JIT for x86-64 or ARM64: translate `PUSH`, `ADD`,
   `LOAD`, `STORE`, `JZ` and `JMP` straight into machine code in memory
   made executable with `mmap`, and fall back to the interpreter for
   everything else.
4. Compile to WebAssembly instead of C. (Chapter 21 runs the machine
   in a browser. Compare the two approaches.)
