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

## Exercises

1. Write the compiler. PL/0 is small enough that Wirth's compiler, in
   Pascal, is a few hundred lines, and chapter 10's enkel/0 compiler is a
   good start. Most of the new work is the levels: each name must
   remember where it was declared.
2. Add parameters. The caller pushes the arguments before `cal`; where
   are they, then, as seen from the new frame?
3. Following `l` static links costs `l` steps on every use. A
   *display* is an array that holds, for each level, the frame in use
   now. What must `cal` and the return do to keep it right? (Many
   Pascal compilers did this.)
4. Write a p-code interpreter in C, and compare its speed with
   `pmachine.py` on a long loop. What did the p-System gain by
   interpreting a compact code, on computers with 64 KB of memory?
