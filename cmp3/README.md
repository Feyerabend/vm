# Virtual Machines

Simple compiler from parsed text to assembly for the virtual machine.
This is a restricted version which only does some compilation of
artithmetical expressions. (No assignments or variables.)


## cmp3

In the file `cmp3.c` you will find a merge between the previous
compiler which starts from the outset of an abstract tree
representation of a program, to the previous parsing of programs as text.

The scanner `scan.c` and `scan.h` are copied from the PL/0 parser with
all tokens recognized. (However they are not all used or recognized by
the parser in `cmp3.c`.)

The file `par2.c` is included here to illustrate, but not to compile,
how arithmetic expressions are parsed. All essential code have already
been moved to `cmp3.c`.


## run

Test the sample with:

```shell
> make clean
> make cmp3
```

Then, if everything worked, no errors were produced, then run it by
letting the text from `sample.p` be parsed:

```shell
> ./cmp3 < sample.p
```

The result should be a file `sample.a`, the assembled version of the program:

```assembly
START:
   SET 12
   SET 1000
   SET 3
   SET 5
   MUL
   ADD
   MUL
   HALT
```

The program as text in `sample.p` is:

```shell
12 * (1000 + (3 * 5))
.
```

The period at the end marks the end of the program (originally from PL/0).


## ambiguities in parsing

We have avoided going into the theory of parsing and grammars here. Instead
we already start with a finished parser, just to add some root at which we
build a tree with parsed leafs. Also some not too conflicting concepts with the
existing solution in e.g. arrays will be added in the future. Hopefully the
grammar was not to disturbed by these moves. However this is *not really* the
solution if you want to build a compiler/parser. This has been done only
for the *learning experience* of what a compiler does and is. There are many
pitfalls with the construction of grammars, which can end up with an endless
recursion in worst case. There are tons of literature on this, but just a short
notice on the problem you can start with, can e.g. be read here:
https://ycpcs.github.io/cs340-fall2016/lectures/lecture05.html.



## division by zero

The case of *DIVIDE* is not implemented in the compiler as it does not exist
in the virtual machine so far, and hence could not run. Division is though here
included in *parsing* as it gives the more complete illustration of expressions.
The problem is that division by zero is undefined in ordinary arithmetic, and
hence have to have some special handling at runtime. A calculator often gives "ERROR"
as the answer.
