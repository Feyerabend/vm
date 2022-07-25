# Virtual Machines

Simple compiler from parsed text to assembly for the virtual machine.

## cmp3

In the file `cmp3.c` you will find a "marriage" between the previous compiler which starts from the oputset of an abstract tree
representation of a program, to the previous parsing of programs as text.

This is a restricted version which only does some compilation of artithmetical expressions.

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
   PRINT
```

The program as text in `sample.p` is:

```
12 * (1000 + (3 * 5))
.
```
