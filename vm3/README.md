# Virtual Machines

The VM has been extended with some new features, which makes it a little bit more powerful.
There are added some extra jump instructions to the vm, also comparatives and a storage facility to
accommodate for iterations (vs. vm1). Moreover there is also a small framework for call/return.
You can store arguments which can be retrieved, use local variables in the function / procedure,
and return value. The "activation records", usually associated with call/return and stack machines,
are stored on the stack, with the exception for arguments used with the call (parameters).[^2] These
"records" are alternatives to the heap solution for memory allocation. The most obvious problem
with activation records (vs. heap) are that memory allocations have to be known at compile time.
Further, there are also both global variables and local variables.

[^2]: More on "activation records" can be found e.g.: https://ruslanspivak.com/lsbasi-part17/.
See also: https://en.wikipedia.org/wiki/Call_stack#Structure.
One exception in the implementation of vm3 is that the parameters passed together with the procedure call
are only *transferred* to the procedure, and can not be relied upon inside the procedure. They
will be invalid in case of nested procedure calls, e.g. The parameters used should therefore only
be regarded as stored as "scratch registers". The parameters should therefore be copied to local variables,
if they have any permanency inside the procedure.

Besides the VM there is also an assembler to simplify programming. It is written in *Python3* which
ease the handling of strings, and have some nice features for list processing.[^3] Using C would be
a bit longer and perhaps harder to read code.

[^3]: Here I borrowed some useful code from
https://github.com/vladris/pixie/wiki/Dust-Assembler,
and looked at some confusing code from
https://github.com/amsanei/Assembler-with-python.

## vm3

Compile with gcc installed.

```
> make bin
> ./bin
```

#### Sample

To test this VM, try a program named `bin` for translating decimal numbers to binary.
The sample starts with the arbitrary number 51966, and we chose 16 bits representation.

```
START:
	SET 16		# number of bits
	STORE R0

LOOP:
	SET 51966	# decimal input
	LOAD R0
	DEC
	RSH
	SET 1
	AND
	PRNT

	LOAD R0
	DEC
	DUP
	STORE R0

	JPNZ :LOOP
	HALT
```

First start with the assembly text in `bin.a` and convert it to the appropriate machine code.

```
> python3 ./asm.py bin.a bin.b
```

The resulting file `bin.b` will be:

```
27,16,31,0,27,51966,15,0,3,26,27,1,1,24,15,0,3,5,31,0,11,4,8
```

Which converts the assembly code in `bin.a` to the machine code for *vm3*. Copy the code produced
either from screen (if available) or from the generated file `bin.b`. Open the c-file `bin.c` with
an editor, and paste the code (replace) in the array named "program". Save the c-file `bin.c` with
your changes. Now:

```
> make clean
> make bin
```

Then, if everything worked, no errors were produced, then run it by:

```
> ./bin
```

A binary number should appear on the screen `1100101011111110`.

The same procedure on compiling and assembling goes for the other samples `factorial` and `prime` (numbers).
