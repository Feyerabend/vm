# Virtual Machines

A machine that takes inspiration from the programming language FORTH[^1].
It can be seen that the language here is very close to both the stack
operations and the traditional machine/assembly language. Hence, programs
can use and be optimized in line of being "forthified" (adopted to suit
FORTH thinking).

[^1]: See https://en.wikipedia.org/wiki/Forth_(programming_language).

## vm2

Compile with gcc installed; `make` at the command line, then run `./fib`.

The sample chosen to illustrate extended from the previous vm1-machine is
the Fibonacci series: 1, 1, 2, 3, 5, 8, 13 ... which can be defined as a
mathematical recursive function:

```math
F(0) = 0,
F(1) = 1,
F(n) = F(n − 1) + F(n − 2) where n > 1,
n ∈ ℕ
```

Applied from the FORTH-thinking we have the following operations at the core:

```forth
TWODUP
ADD
ROT
DROP
```

First duplicate what is already on stack, the two top items `TWODUP` (or `2DUP`),
such that if we have "1 2" after would be left with "1 2 1 2".
Next add the two numbers on the stack "1 2" becomes "3", and the first two still
are there such that "1 2 3". Then rotation `ROT` would get "2 3 1", and we then
`DROP` the top, "2 3". That is, the numbers that remain will be added next time.
And so on.

## CISC vs. RISC

The experimental enlargement of the machine capacities through new instructions
maybe also be compared with the RISC vs. CISC debate[^2] (even if it is on a
virtual machine which introduces new aspects that doesn't make it fully comparable).
Here RISC (reduced instruction set) indicate microprocessors which have a few (simple,
powerful), compared to the CISC (complex instruction set) which have many (complex,
"slow") instructions. (A machine with even less instructions, in fact only one, use
only the SUBLEQ[^3] instruction.)

[^2]: See RISC https://en.wikipedia.org/wiki/Reduced_instruction_set_computer,
and CISC https://en.wikipedia.org/wiki/Complex_instruction_set_computer.

[^3]: See https://en.wikipedia.org/wiki/One-instruction_set_computer.

## hardware

Another observation is that there exist hardware, processors with instruction sets
that implements the virtual machine of Java: *JVM* (at least in its early iterations
for embeded use).[^4]

[^4]: See https://en.wikipedia.org/wiki/PicoJava.


Building from the "bottom up" was also something that could be claimed happened to
Lisp Machines, that had *Lisp Machine Lisp* at the hardware level.[^5]
Microcode could be used for directly implementing a "high level" language such
as PL/I in hardware.[^6] Or indeed in Forth.[^7]

[^5]: See https://en.wikipedia.org/wiki/Lisp_Machine_Lisp,
and https://en.wikipedia.org/wiki/Lisp_machine.

[^6]: See https://en.wikipedia.org/wiki/Microcode

[^7]: See http://users.ece.cmu.edu/~koopman/stack_computers/sec4_4.html
