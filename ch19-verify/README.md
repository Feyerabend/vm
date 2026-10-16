# Chapter 19: Verify once, then trust

Since chapter 4, every instruction checks, every time it runs, that
nothing has gone wrong: that a pop finds a value in its frame, that a
`LOAD` names a local that exists, that a jump lands inside the
program, that an instruction has all its operands. For nearly every
program, nearly all of these checks can never fail. They are paid for
anyway, millions of times.

Chapter 17's register machine showed another way. Its translator
proved, before running, that the stack could never underflow, and so
the register machine never checked. This chapter brings the idea back
to the stack machine, the way the Java Virtual Machine does it: a
*verifier* examines the whole program once, when it is loaded. A
program that passes runs on a copy of the machine with those checks
taken out.

## The verifier

`verify()` in [`vm.c`](vm.c) follows every path through the program,
from address 0 and from the start of every function, counting how
many values the current frame holds. It refuses the program if, on
any path:

- an instruction is unknown, incomplete, or not where an instruction
  begins when the program is read from the start;
- a jump or call goes outside the program, or the program could run
  off its end;
- an instruction pops more values than the frame holds, or the frame
  could hold more values than the stack has room for;
- `LOAD` or `STORE` names a local that the frame does not have;
- a `CALL` passes more values than the frame holds, or one function
  is called with different numbers of arguments;
- two paths meet with different numbers of values, or one piece of
  code belongs to two functions;
- `RET` appears outside a function;
- `CALLI` is used: its target is a value, not known before running.

Every rule is about the *program*, not about any one run of it. So a
program that passes can never fail any of the checks it covered, on
any input, however it runs.

```
$ ./vm -V suite/trap-underflow.vm
trap-underflow.vm: not verified: at 2: a pop from a frame with too few values
```

[`tests/verdicts.txt`](tests/verdicts.txt) lists the verdict on every
program in the conformance suite. Every ordinary program verifies,
except `calli`. Nearly every `trap-` program is refused, which is
right: each was written to fail in one of these ways.

## Two machines from one

The instructions are still written once, in [`ops.h`](ops.h), and the
run loop once, in [`loop.h`](loop.h). `vm.c` includes them twice. The
first time, `pop()` checks for underflow, `operand()` checks that the
operand exists, and so on. Before the second time, those are
redefined to check nothing:

```c
static inline struct value pop_verified(void) {
    return stack[--sp];
}
#define pop() pop_verified()
```

and a few checks inside instructions, written `CHECK(condition,
message)` in `ops.h`, become empty. That gives two functions,
`run_checked` and `run_verified`, from one set of instructions. The
machine verifies each program and picks one. A program that fails
verification still runs, with every check, and fails exactly as the
specification says, so the whole conformance suite still passes:

```
./vm: 71 of 71 passed
./vm -C: 71 of 71 passed          (-C: never verify)
```

The verified helpers must be real functions, not macros. The first
version used `#define address() (code[pc++])`, and the compiler
warned at once: in `pc = address();` that would change `pc` twice in
one expression, which C leaves undefined.

## What is still checked

A verifier can only remove checks about things that do not depend on
the run. Still checked, every time:

- **stack overflow**, since how deep calls go depends on the data;
- **the kinds of values**: whether `ADD` was given numbers;
- **division by zero**, memory addresses, and block bounds;
- the number of nested calls.

The JVM goes further: its verifier also works out the *type* of every
value on the stack, so that an addition of two integers checks no
tags at all. That is exercise 1.

## Is the verifier right?

This matters more than anything else in the chapter. If the verifier
ever accepts a program it should have refused, that program runs
without the checks that would have stopped it, and the machine reads
or writes outside its own stack. Instead of a trap, there is silent
corruption.

[`fuzz.py`](fuzz.py) writes random programs. Purely random ones
almost never verify, so it cheats: it keeps count of the stack depth
as it writes, and mostly chooses instructions the depth allows. Now
and then it breaks the rules on purpose. [`fuzz.sh`](fuzz.sh) then
runs each program twice, verified and with every check, on a machine
built with AddressSanitizer and UndefinedBehaviorSanitizer, and with
a limit on steps, so that programs that loop forever stop at the same
place both times. Any difference between the two runs, or any
complaint from a sanitizer, means the verifier let something through.

```
600 programs, 418 of them verified
every verified run was the same as the checked run
```

Over 1,500 programs and three seeds while writing this chapter, there
was no difference. To check that the test can fail, the verifier was
broken on purpose, by removing its check for pops from a frame with
too few values. The fuzzer found programs it let through on the first
run, and the sanitizer named the result:

```
runtime error: index -1 out of bounds for type 'value [256]'
```

## Measured

Best of five, milliseconds:

|             | GCC 13, checked | verified | Clang 18, checked | verified |
|-------------|------:|------:|------:|------:|
| fib         | 111 |  81 |  59 |  51 |
| loop        | 844 | 676 | 857 | 812 |
| sieve       |  87 |  68 |  63 |  54 |
| enkel-sieve | 182 | 176 | 152 | 135 |
| basal-loop  |  47 |  45 |  34 |  38 |

Between 5 and 27 percent faster, mostly, with the usual noise. The
remaining cost is in what is still checked: every `push` tests for
overflow, and every `ADD` tests two tags.

## Run it

```
make test
make bench
```

## Exercises

1. Make the verifier track the kind of each value: number, reference,
   or unknown. Then `ADD` on two values known to be numbers needs no
   tag checks. Which of the benchmarks get faster?
2. Overflow can be checked once per call instead of once per push: the
   verifier knows how deep each function's stack can get, so `CALL`
   can check that much room is left. Does this change what the
   machine does, as the specification describes it? (Look at *where*
   a stack overflow would now be reported.)
3. Let the verifier accept `CALLI`, for programs that say, in the file,
   which addresses are functions and how many arguments each takes.
   What must `CALLI` still check while running?
4. Shrink a failing fuzz case automatically: remove instructions one
   at a time while the failure remains, until nothing can be removed.
   This is *delta debugging*.
