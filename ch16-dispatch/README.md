# Chapter 16: Dispatch

Part V is about making the machine better at being a machine: faster,
safer, closer to the hardware. It starts with the loop at its heart.

Every chapter so far has run instructions the same way:

```c
for (;;) {
    op = code[pc++];
    switch (op) {
    case ADD: ...; break;
    case SUB: ...; break;
    ...
    }
}
```

Getting from one instruction to the next (fetch the opcode, check it,
find its code, jump there) is called *dispatch*. Each `ADD` does one
addition and then all of that. In a simple interpreter, dispatch can
be as much work as the instructions themselves, so it is the first
place people look for speed.

## One set of instructions, three loops

[`vm.c`](vm.c) is chapter 15's machine, with its loop rewritten so it
can be built three ways. The instructions are written once, in
[`ops.h`](ops.h):

```c
OP(ADD) {
    struct value w = pop(), v = pop();
    push_int(wrap_add(number(v), number(w)));
    NEXT;
}
```

and `OP` and `NEXT` are macros whose meaning depends on the build.
CPython's and Lua's interpreters are organised exactly like this.

**`vm-switch`.** `OP(ADD)` is `case ADD:`, and `NEXT` goes back to the
top of the loop. The compiler makes the switch into a jump through a
table, after checking that the opcode is in range. All instructions
share that one jump.

**`vm-goto`.** `OP(ADD)` is a label, `L_ADD:`, and `NEXT` fetches the
next opcode and jumps straight through a table of label addresses:

```c
goto *table[code[pc++]];
```

Every instruction now ends with its own jump. The processor's branch
predictor can learn, separately for each one, what tends to come
next: after a `LOAD`, often another `LOAD`; after `LT`, nearly always
`JZ`. This is "labels as values", an extension of GCC and Clang, not
standard C.

**`vm-threaded`.** Before the program runs, every word of it is
replaced, in a second array, by the address of the label that runs
it. `NEXT` is then:

```c
goto *thread[pc++];
```

No table lookup, and no range check: a word that is not an
instruction got the label of the code that traps. This is *direct
threaded code*, the technique of Forth systems since the 1970s.

A subtle point: *every* word gets a label, not just the words where
instructions start. A program may jump into the middle of an
instruction, and the specification says exactly what happens then, so
every build must do it the same way.

## They are the same machine

```
./vm-switch -g mark: 71 of 71 passed
./vm-switch -g copy -S: 71 of 71 passed
./vm-goto -g mark: 71 of 71 passed
./vm-goto -g copy -S: 71 of 71 passed
./vm-threaded -g mark: 71 of 71 passed
./vm-threaded -g copy -S: 71 of 71 passed
```

Speed is worth nothing if the answers change, and the conformance
suite of chapter 8 makes checking that a single command.

## How much faster?

Four programs in [`bench/`](bench): recursive `fib(30)`; a tight
`loop` of 20 million rounds; a `sieve` on the heap; and `closures`, a
compiled lambda/0 program from chapter 15. `make bench` runs each
three times on each build and reports the best. On one computer,
milliseconds:

Built with GCC 13, `-O2`:

|          | switch | goto | threaded |
|----------|-------:|-----:|---------:|
| fib      | 137 |  97 |  86 |
| loop     | 1072 | 883 | 839 |
| sieve    |  77 |  93 |  72 |
| closures | 151 | 129 | 134 |

Built with Clang 18, `-O2`:

|          | switch | goto | threaded |
|----------|-------:|-----:|---------:|
| fib      |  76 |  83 |  57 |
| loop     | 654 | 703 | 553 |
| sieve    |  66 |  57 |  52 |
| closures |  66 |  72 |  53 |

The measurements are noisy (this was a shared machine), but the
pattern held across runs. Threaded code is usually fastest, by 10 to
25 percent. Computed goto sometimes helps and sometimes does not. And
the choice of *compiler* made as much difference as the choice of
technique.

The gains are smaller than the classic papers report, for two
reasons. Processors since about 2013 predict the single jump of a
switch far better than older ones did, which took away much of what
computed goto used to win. And in this machine, dispatch is not the
biggest cost. Look at what `ADD` does besides adding: two calls to
`pop`, each checking for underflow; two calls to `number`, each
checking a tag; one call to `push`, checking for overflow; and all of
it through memory. The next chapters go after those costs: fewer
instructions (chapter 17), better instructions (chapter 18), and
checks done once, before running, instead of on every step
(chapter 19).

## Run it

```
make test        # all three builds, against the suite and the benchmarks
make bench       # the timings
make CC=clang bench
```

## Exercises

1. Count how often each instruction follows each other one in
   `bench/loop.asm`. Which pair is most common? Chapter 18 makes
   that pair into one instruction.
2. Build with `-O0`. How do the three compare now? Why?
3. Make `push`, `pop` and `number` macros, or `static inline`, and
   look at the generated assembly for `L_ADD` (`gcc -S`). How many
   instructions does one `ADD` take?
4. *Subroutine threading*: instead of jumping between labels, turn
   the program into a list of calls to one C function per
   instruction. Is it faster or slower than direct threading here?
