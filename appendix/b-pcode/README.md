# B: p-code, Pascal's machine

In the early 1970s, Niklaus Wirth's group in Zurich had a problem
every language designer has: Pascal should run on many computers, and
writing a compiler for each one is a great deal of work. Their answer
was the Pascal-P compiler. It compiled Pascal for a machine that did
not exist, a simple stack computer, and its code was called *p-code*.
To bring Pascal to a new computer, you wrote an interpreter for p-code,
a few pages long, instead of a compiler.

A few years later, at the University of California, San Diego, Kenneth
Bowles's group took the idea much further. UCSD Pascal compiled to a
compact, byte-coded p-code, and around it they built a whole system,
the UCSD p-System: editor, compiler, file system, all in p-code, and
all able to move to a new computer by writing one interpreter. It ran
on the Apple II, and was one of the three operating systems offered
with the first IBM PC. Western Digital even built a processor, the
Pascal MicroEngine, whose microcode ran p-code directly, much as
chapter 22 built our machine as hardware.

The p-System did not last, but the idea did. Java's slogan, "write
once, run anywhere", is the p-System's plan, twenty years on.

## The P-machine

The full UCSD p-code is large. Its idea fits in the smaller machine
Wirth used for PL/0, a teaching subset of Pascal, in his book
*Algorithms + Data Structures = Programs* (1976).
[`pmachine.py`](pmachine.py) implements it. It has eight instructions,
each with two fields, a *level* `l` and an argument `a`:

| Instruction | Does |
|-------------|------|
| `lit 0 a` | push `a` |
| `opr 0 n` | return, or an arithmetic operation, by number |
| `lod l a` | push the variable at offset `a`, `l` levels out |
| `sto l a` | pop into the variable at offset `a`, `l` levels out |
| `cal l a` | call the procedure at `a`, declared `l` levels out |
| `int 0 a` | make room for `a` words on the stack |
| `jmp 0 a` | jump |
| `jpc 0 a` | pop, and jump if it was zero |

Much of this is familiar: a stack, `PUSH`, arithmetic, jumps, and calls
with frames, as in chapters 1 to 3. The interesting part is the
*level*.

## Levels and static links

Pascal lets a procedure be declared inside another, and the inner one
may use the outer one's variables. So a variable is found by two
numbers: how many levels out it was declared, and its offset in that
frame.

Every frame starts with three words: the *static link*, the *dynamic
link*, and the return address. The dynamic link is the caller's frame,
like the saved frame pointer of chapter 3. The static link is the
frame of the procedure that this one was *written inside*. To reach a
variable `l` levels out, the machine follows the static link `l`
times.

The two links are different whenever a nested procedure calls itself.
In [`samples/nested.p`](samples/nested.p), `down` is declared inside
`outer`, and counts `outer`'s variable `k` down to zero by calling
itself. Here is the stack after two calls of `down`, from the trace
(`-t`):

```
 0 0 0 5 | 0 0 27 4 | 4 4 22 | 4 8 17
 main      outer      down     down
```

Each `down` frame begins with its static link and its dynamic link.
The first `down` was called by `outer`, at 4, so both links are 4. The
second was called by the first `down`, at 8, so its dynamic link is 8.
Its static link is still 4: it still finds `k` in `outer`.

## Compared with ours

Our machine has no levels. In chapter 15, inner functions reached
outer variables in another way: a closure, a block on the heap that
holds the variables it needs. The difference is about what a language
allows. In Pascal, a procedure can be passed as an argument, but never
returned or stored, so it can never outlive the frame it was declared
in. The frames can stay on the stack, and a static link is enough. In
our lambda language, a function can be returned, and live on after its
maker's frame is gone, so what it needs must move to the heap. This is
the *funarg problem*, and the two machines are its two answers.

The P-machine also has no traps to speak of. Its specification is a
Pascal program in Wirth's book, and what that program does with a bad
jump or a stack overflow is whatever Pascal does. A real interpreter
had to decide, as chapter 4 did.

## Run it

```
make test
python3 pmachine.py samples/nested.p
python3 pmachine.py -t samples/nested.p
```

There is no PL/0 compiler here: the samples are p-code written by
hand, with their PL/0 in a comment, as Wirth's compiler would have
made it. `opr write`, which pops and prints a number, is ours; PL/0
had no output, and Wirth's interpreter printed every value as it
was stored instead.

## P4: the machine Pascal travelled on

The P-machine is the idea. The machine that carried Pascal to new
computers was bigger: the P4 machine of Pascal-P4, from Zurich in
1976, the last of the Pascal-P compilers. (UCSD Pascal had grown from
the one before it, P2.) [`p4.py`](p4.py) is our own implementation of
it, written from the description of what each instruction does, and
it reads P4 code in the text form the original P4 interpreter read.

P4 keeps the P-machine's levels and static links, and adds what Pascal
needs that PL/0 did not:

- **Types.** Most instructions carry a letter: `lodi` loads an
  integer, `lodc` a character, `lodb` a boolean; `equs` compares two
  sets, `equm 8` two blocks of eight words. The machine itself does
  not need the letters, since every word can hold a value of any type,
  but a real implementation does: a real took two words on some
  computers, and a set four.
- **A frame with a mark.** `mst` begins a frame before the arguments
  are pushed: five words, for a function's result, the static link,
  the dynamic link, the caller's stack limit, and the return address.
  The arguments follow, so the called procedure finds them as its
  first variables, at 5, 6 and so on. `cup` jumps, and `ret` returns.
- **Addresses.** `lda` and `lao` push the address of a variable, `ind`
  loads through an address, `sto` stores through one, and `ixa`
  indexes an array: `ixa 3` multiplies the index by 3, the size of an
  element, and adds it to the address below. A `var` parameter is an
  address, and arrays are reached the same way.
- **Two limits for each frame.** `ent 1 l5` makes room for the
  variables, and `ent 2 l6` reserves the most the stack will need
  above them. Both sizes are labels, given values only after the code
  (`l5=7`): the compiler works in one pass, and knows them only at the
  end. The machine checks both, so a frame can never run into the heap,
  which `new` grows from the other end of the store.
- **Standard procedures.** `csp wri` writes an integer, `csp rdc`
  reads a character, and so on: input and output are not instructions,
  but calls into the machine.
- **case by table.** `xjp` jumps to the table entry for the value on
  the stack, and the entry jumps to its branch.

Two P4 programs written by hand are in [`samples`](samples):
[`hello.p4`](samples/hello.p4), and [`nested.p4`](samples/nested.p4),
the program above, in P4.

## pascal/0

The P4 machine was made for a compiler, and here is one:
[`pascal.py`](pascal.py) compiles pascal/0, a small part of Pascal
described in [`LANG.md`](LANG.md), to P4 code. It has integers,
booleans and characters, arrays, `for`, `case`, `repeat`, and
procedures and functions nested in each other with value and `var`
parameters. It works as Wirth's compilers did, in one pass: where
chapter 10's compiler first reads the whole program into a tree, this
one writes the code for each statement as soon as it has read it. The
function in this program

```pascal
function square(x: integer): integer;
begin
    square := x * x
end;
```

becomes

```
l 2
 ent 1 l 3
 ent 2 l 4
 lodi 0 5
 lodi 0 5
 mpi
 stri 0 0
 reti
l 3=6
l 4=2
```

`x` is at 5, after the mark, and the result goes in word 0 of the frame,
where `reti` leaves it on the stack for the caller. The frame needs 6
words, and the stack at most 2 more.

The [`pascal`](pascal) folder holds thirteen programs, among them
Wirth's eight queens, the sieve of Eratosthenes, and the towers of
Hanoi, each with its P4 code and its output. Those in
[`pascal/traps`](pascal/traps) break a rule that only shows when the
program runs, and the machine stops them: an index out of range, a
division by zero, a `case` value with no label, and a variable used
before it has a value. Those in [`pascal/errors`](pascal/errors) are
refused by the compiler.

Every program in `pascal` is real Pascal. If Free Pascal is installed,
`make test` compiles each one with it too, in its ISO mode, and checks
that it prints exactly what the P4 machine printed.

## Run it

```
make test
python3 pmachine.py samples/nested.p
python3 pmachine.py -t samples/nested.p
python3 p4.py -t samples/nested.p4
python3 pascal.py pascal/queens.pas > queens.p4
python3 p4.py queens.p4
```

## Exercises

1. Write the PL/0 compiler. PL/0 is small enough that Wirth's
   compiler, in Pascal, is a few hundred lines, and chapter 10's enkel/0
   compiler is a good start. Most of the new work is the levels: each
   name must remember where it was declared. Then compare it with
   `pascal.py`.
2. Where are a procedure's parameters on the P-machine, if the caller
   pushes them before `cal`? Compare with P4's `mst`, which is there to
   make room for the mark *before* the arguments.
3. Following `l` static links costs `l` steps on every use. A
   *display* is an array that holds, for each level, the frame in use
   now. What must `cal` and the return do to keep it right? (Many
   Pascal compilers did this.)
4. Write a P4 interpreter in C, and compare its speed with `p4.py` on
   `queens.pas`. What did the p-System gain by interpreting a compact
   code, on computers with 64 KB of memory?
5. Add `forward` to pascal/0, so two procedures can call each other.
   What must the compiler know about a procedure before it can write
   the call?
6. Add records. The machine needs nothing new: a field is an offset,
   added to the record's address with `inc`.
7. Add real numbers. The machine has them already (`adr`, `flt`,
   `csp wrr`); the compiler must decide when an integer becomes a real.
