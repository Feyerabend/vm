# Chapter 8: A specification

What *is* this machine? Until now the answer was "whatever `vm.c`
does". That answer has two problems.

First, `vm.c` does some things by accident. Ask chapter 7's machine
for `-2147483648 / -1` and, on an ordinary PC, the whole machine dies
with a hardware exception, taking the program's earlier output with
it. Nobody decided that; it is what the C compiler and the processor
happen to do with a case C leaves undefined.

Second, there can only ever be one machine. A second implementation,
in Python, in JavaScript, in hardware, can only copy `vm.c`, bugs
included, and nobody can say which differences matter.

So this chapter writes the machine down: [`SPEC.md`](SPEC.md). Then it
builds a second machine from the document, not from the C, and a test
suite that holds both to it.

## What writing it down decided

Some questions have no answer until somebody writes one:

- **Overflow.** `2147483647 + 1` is now `-2147483648`, by definition:
  arithmetic wraps at 32 bits. The C machine computes with unsigned
  numbers to get there without undefined behaviour.
- **Division.** Rounds towards zero, and the remainder takes the sign
  of the dividend, as in C. `-2147483648 / -1` wraps to
  `-2147483648`; it no longer crashes anything.
- **Order.** `JZ 9999` on an empty stack: is that a bad jump or a
  stack underflow? The spec gives every instruction its steps in
  order, and the first failing step wins. (A bad jump.)
- **A bug.** In chapter 7, `STORE` checked which local to write
  *before* popping the value. So `STORE 0` with one value in the frame
  wrote into the slot it was about to free. Writing the steps out in
  order showed it. `STORE` now pops first.

Equally important is what the spec does *not* fix: usage messages,
the debugger, anything a program cannot observe. Those are up to each
implementation.

## Two machines

[`vm.c`](vm.c) is chapter 7's machine with the changes above.

[`vm.py`](vm.py) is a new machine in Python, written from the spec.
It is not a line-by-line translation, and the differences are where
the lessons are. Python's integers never overflow, so it has to wrap
by hand. Python's `//` rounds towards minus infinity, so `-7 // 2` is
`-4` in Python but must be `-3` here. It supports tracing (`-t`) in
exactly the format of section 8 of the spec, but not the debugger,
which the spec leaves out.

## The conformance suite

[`suite/`](suite) holds 31 small programs, each with an `.expect`
file saying what the spec says must happen: what it prints, its exit
status, and its error message. There is at least one test for every
instruction and every trap, for the exact limits (256 values on the
stack are fine and 257 are not, and the same for frames), and for
each rule above. [`conform.py`](conform.py) runs them all, plus nine
damaged program files, against any machine:

```
$ python3 conform.py ./vm
./vm: 40 of 40 passed
$ python3 conform.py python3 vm.py
python3 vm.py: 40 of 40 passed
```

The expectations were written from the spec, before running either
machine. Run against chapter 7's machine, the suite fails three tests,
exactly the three changes above. Run against a Python machine that
uses Python's `//`, it fails one test, the division test.

## Comparing traces

Two machines can print the same answers by different routes.
[`compare.py`](compare.py) runs both with `-t` and compares the traces
line by line, every step and every stack:

```
$ python3 compare.py ./vm "python3 vm.py" build/*.vm samples/*.vm
44 of 44 programs traced identically
```

When they differ, it shows the first step where they part ways:

```
build/division.vm: the machines differ
  first different line, number 7:
      ./vm:      7    10  DIV             -3
    vm.py:      7    10  DIV             -4
```

Testing one implementation against another like this is called
*differential testing*. It finds bugs that nobody thought to write a
test for, as long as the two machines were written independently.

## Run it

```
make test
```

## Exercises

1. Write a third machine, in any language you like, from `SPEC.md`
   alone, without looking at the other two. Run `conform.py` on it.
   Which tests failed the first time, and was it your machine or the
   spec that was unclear?
2. Find something the spec still leaves open that a program *can*
   observe. (Hint: section 9 lists one. Are there others?)
3. Write a program that generates random programs, and use
   `compare.py` to run them on both machines. This is *fuzzing*.
   What do you need to do so that the random programs halt?
4. The suite has 40 tests. Is every line of `vm.c` run by at least one
   of them? Use `gcc --coverage` and `gcov` to find out.
