# Virtual Machines

*Two virtual machines that (almost) implements the same vm.*
One in C, and the other in Python3.


## vm4

There is a `sample.p` that has been compiled to `sample.b` previously.
You can run this on either of the virtual machines. First running
the C variant:

```shell
> ./c.sh
```

And then the Python3 variant:

```shell
> ./py.sh
```

As can be observed, Python is roughly 50 times slower than C.


#### Sample

The sample is the factorial:

```pascal
procedure factorial[n];
	var m, o;
	begin
		if n = 1 then return 1;
		o is n - 1;
		call factorial[o];
		return (n * rval)
	end;

begin
	call factorial[10];
	print rval
end.
```

Which translates into assembly:

```assembly
C0002:
	LDARG 0
	ST 0
	LD 0
	SET 1
	EQ
	JPZ :L0003
	SET 1
	STORE 0
	RET
L0003:
	LD 0
	SET 1
	SUB
	ST 3
	LD 3
	STARG 0
	CALL :C0002
	LD 0
	LOAD 0
	MUL
	STORE 0
	RET
	RET
START:
	SET 10
	STARG 0
	CALL :C0002
	LOAD 0
	PRINT
	HALT
```

And then the assembler spits out the "binary" file:

```shell
38,13,0,28,0,12,0,27,1,5,11,16,27,1,30,
0,24,12,0,27,1,31,28,3,12,3,29,0,2,0,12,
0,14,0,18,30,0,24,24,27,10,29,0,2,0,14,
0,22,8
```

Which both machines can handle.

## problems with different machines

Besides this sample above, it is easy to find samples that simply do not work
on *both* machines. It depends upon implementations rather than some abstractions.
But instead of defining our own specification, we will look at a well known
programming language and the fact it already has a virtual machine: the
Java Virtual Machine Specification.
