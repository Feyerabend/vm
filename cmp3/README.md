# Virtual Machines

Simple compiler from parsed text to assembly for the virtual machine.
This is a restricted version which only does some compilation of artithmetical expressions.


## cmp3

In the file `cmp3.c` you will find a "marriage" between the previous compiler which starts from the outset of an abstract tree
representation of a program, to the previous parsing of programs as text.

The scanner `scan.c` and `scan.h` are copied from the PL/0 parser with all tokens recognized. (However they are not all used or
recognized by the parser in `cmp3.c`.)

The file `par2.c` is included here to illustrate, but not to compile, how arithmetic expressions are parsed.

## run

Test the sample with:

```
> make clean
> make cmp3
```

Then, if everything worked, no errors were produced, then run it by letting the text from `sample.p` be parsed:

```
> ./cmp3 < sample.p
```

The result should be a file `sample.a`, the assembled version of the program:

```
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

```
12 * (1000 + (3 * 5))
.
```

## note

The case of *DIVIDE* is not implemented in the compiler as it does not exist in the virtual machine so far, and hence could not run.
Division is though here included in *parsing* as it gives the more complete illustration of expressions.
