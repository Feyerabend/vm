# Virtual Machines

The compilation here takes place in a series of steps.
Often these kinds of steps are referred to as a "toolchain".
Such a link in the "chain" can be a program that takes in
someting from a file and leaves someting (else) as output,
which has thus been processed. There can be other tools
(not present here) such as for profiling, linking or debugging
in a *toolchain*.


## strip

First we *strip* off any comments that may have been added.
These are assumed to be the same as can be found in C/C++.
(You might change this to someting else you find better,
if you alter the regular expression to handle it.)


## enkel/0

Now from text, as we see the program, the compiler *enkel/0*
converts the prorgamming ideas to code in the form of assembly.

...
...

## scan

When compiling we need something to select the "words" in
the program (programming language). Here is where the "scanner" or
"tokenizer" comes in.


## symbol

As we are more used to remembering names or at least it is
easier to connect parts in the program.

...

## error

A separate handling of errors does not too much clutter the compiler.


## asm

The assembler/assembly follows previous examples as an abstraction layer
from the machine code. We can handle several optimizations here or
immediately before by adding a filtering program in the chain.
Another place is in the compiler, through the AST.

The assembler follows the usual way of handling compiling, where
it is sliced from programming language, to assembly, to machine
language.

