# Virtual Machines

The virtual machine consists of essentially two files plus header files. The real
point of the virtual machine is to separate running from the construction of the
runnable.

We have a machine in `enkelvm.c` and `enkelvm.h`, and loading code and directing
the machine is done through `runvm.c`. The only thing to be added is the "binary"
code for the program.


![runvm.c](../assets/images/runvmc.png)

## runvm

The limits of the machine are defined in the runner `runvm.c`. Variables, globals, 
stack, etc. are set from the start. Will it hit a wall concerning memory, and you
have the hardware, the limits might be changed by you.

Before loading, the length of the input file is measured. The point being to allocate
the array for the code correctly. The "binary" file have integers separated by commas,
throughout. It also in a certain format, where the first number points to where the
*vm* should start. The rest of the file is the program itself.

![File format for enkel/0](../assets/images/fileformat.png)

A header of one (1) integer (separated with a comma before the body) signals where to
start. The rest is read in an array to be executed, starting at the position where the
`START` label was pointing before the assembler did its thing.

The runner measures the time from when the program starts until it finishes, and
prints the duration.


### exercise: add version

It is useful sometimes to think about the future when you program. An addition
to the header could be to add some *version* of the current machine. Then when
updating, in the future, you could check for if a certain version can be run
at the present machine or not.

Then one way to amend future problems is to have a conversion script which
converts the previous machine instructions to the (future) current one --
if possible. Or if they can not be translated, have some information of what
has changed and what to do about it.



## vmenkel

### addition, subtraction, division, multiplication

The virtual machine has in main been described earlier, and not much have changed
concerning the familiar arithmetical operations. The implementation should be
recognized as straightforward.

```c
case ADD:
	b = pop(vm);
	a = pop(vm);
	push(vm, a + b);
	break;

case DIV:
	b = pop(vm);
	a = pop(vm);
	if (b == 0) {
		fprintf(stderr, "Runtime error: division by zero.\n");
		exit(EXIT_FAILURE);
	}
	div_t c = div(a, b);
	push(vm, (int) c.quot);
	break;

case MUL:
	b = pop(vm);
	a = pop(vm);
	push(vm, a * b);
	break;

case SUB:
	b = pop(vm);
	a = pop(vm); 
	push(vm, a - b);
	break;

case UMIN:
	a = pop(vm);
	push(vm, -a);
	break;
```

We have added a unary minus which has an easy implementation in C. Also a runtime
error is raised when a division by zero occurs (rather than have C to work this out).


### modulus, and, or, xor

Some convenient or useful operations have been added. You might change the implementation
here to better fit your purpose, such as `|` to `||` or `&` to `&&` etc.

Feel free to add your own operator, or delete existing ones. Remember though that
changes have a cascading effect in that headers have to change, enumerations, and
parsing (even scanning sometimes depending, if a new character is added not presently
in the scanner).

```c
case MOD:
	b = pop(vm);
	a = pop(vm);
	push(vm, a % b);
	break;

case OR:
	b = pop(vm);
	a = pop(vm);
	push(vm, a | b);
	break;

case AND:
	b = pop(vm);
	a = pop(vm);
	push(vm, a & b);
	break;

case XOR:
	b = pop(vm);
	a = pop(vm);
	push(vm, a ^ b);
	break;
```


### call/return

#### activation records

An activation record is a "private" block of memory, here placed on the stack. The activation
record is used when there is an invocation of a procedure. It is also recognized as a runtime
structure to manage procedure calls.

```c
case CALL:
	addr = nextcode(vm);	// CALL <address>
	push(vm, vm->fp);	// push the frame pointer to stack
	push(vm, vm->pc);	// push the program counter to stack
	vm->fp = vm->sp;	// set the frame pointer to what the stack pointer is
	vm->pc = addr;		// set the program counter to the address: addr
	break;
```

An activation record includes a mechanism to return control to the caller and continue
execution at the point immediately after the call. Also the mechanism is responsible
for restoring the previous stack pointer, frame pointer and discard any remains on the
stack.

```c
case RET:
	vm->sp = vm->fp;	// reset the stack pointer from the frame pointer
	vm->pc = pop(vm);	// pop the top element as the new program counter
	vm->fp = pop(vm);	// pop the (new) top and set the frame pointer
	break;
```

Here also the procedure in connection with the language will return one value to the caller
which is stored in the `rval` global variable. Thus it is not the vm that handles this
feature in any special instructions, but rather it is done through the compiler.

#### passing parameters

An activation record is used to map a set of arguments, or parameters, from the caller's
name space to the callee's name space. In this langauge case it is through another set of
instructions `LDARG` and `STARG`. When calling a procedure a bag of arguments gets to the
procedure with `STARG`.

```c
case STARG:
	v = pop(vm);		// pop the value
	addr = nextcode(vm);	// STARG <address>
	vm->args[addr] = v;	// store the value at address
	break;
```

Loading the arguments from the caller, to local variables storage is done through `LDARG`.

```c
case LDARG:
	addr = nextcode(vm);	// LDARG <address>
	v = vm->args[addr];	// load value from where the address points
	push(vm, v);		// push the value
	break;
```


### local variables

Local storage ..

```c
case ST:
	v = pop(vm);
	offset = nextcode(vm);
	vm->vars[vm->fp + offset] = v;
	break;
```

```c
case LD:
	offset = nextcode(vm);
	v = vm->vars[vm->fp + offset];
	push(vm, v);
	break;
```



### global variables

Global storage ..

```c
case LOAD:
	addr = nextcode(vm);
	v = vm->vars[addr];
	push(vm, v);
	break;
```

```c
case STORE:
	v = pop(vm);
	addr = nextcode(vm);
	vm->vars[addr] = v;
	break;
```




### arrays

The arrays might seem to have an odd implementation. As the others it does not use
an argument for address. Instead it uses the stack. A base address is stored in an
array at runtime, which resembles how globals work, and is actually a global. When
the arrays is used and an index will point to the offset given the base. So a global
variable is used for the base, and an index given at runtime is *added to the base*,
which give the address from which to get a value or to store a given value.

A general scheme is used for accessing values in arrays.

```text
LOAD <address>	// get the value from a global variable
ADD		// add what comes from stack (index) and global var
...
```

This will put an absolute address for the array on the stack. Thereafter either a
`RLOAD` or `RSTORE` can be used. The arrays uses parts in their own long single
array `arrs[]` at runtime.

```c
case RLOAD:
	a = pop(vm);		// get an address from the stack
	v = vm->arrs[a];	// get the value at the address
	push(vm, v);		// push the value to stack
	break;
```


```c
case RSTORE:
	a = pop(vm);		// pop for (calculated) address
	b = pop(vm);		// pop for value to be stored
	vm->arrs[a] = b;	// store in array
	break;
```






### jump

Jumping or branching is done through altering the address of the program counter
(pointing to the next instruction to be executed). A simple check before branching
if true, can decide if to jump. Here are two alternatives for the check, if what
is on stack equal to zero, or if it is not equal to zero.

There is also a jump without a condition.

```c
case JP:
	vm->pc = nextcode(vm);	// unconditional jump
	break;

case JPNZ:
	addr = nextcode(vm);	// JPNZ <address>
	v = pop(vm);		// pop value
	if (v != 0) {		// if the value not zero, ..
		vm->pc = addr;	// .. then go to address
	}
	break;

case JPZ:
	addr = nextcode(vm);	// JPZ <address>
	v = pop(vm);		// pop value
	if (v == 0) {		// if the value is zero, ..
		vm->pc = addr;	// .. then go to address
	}
	break;
```


### condition


```c
case EQ:
	b = pop(vm);
	a = pop(vm);
	push(vm, (a == b) ? TRUE : FALSE);
	break;

case GT:
	b = pop(vm);
	a = pop(vm);
	push(vm, (a > b) ? TRUE : FALSE);
	break;

case GQ:
	b = pop(vm);
	a = pop(vm);
	push(vm, (a >= b) ? TRUE : FALSE);
	break;

case LT:
	b = pop(vm);
	a = pop(vm);
	push(vm, (a < b) ? TRUE : FALSE);
	break;

case LQ:
	b = pop(vm);
	a = pop(vm);
	push(vm, (a <= b) ? TRUE : FALSE);
	break;

case NEQ:
	b = pop(vm);
	a = pop(vm);
	push(vm, (a != b) ? TRUE : FALSE);
	break;
```


### print

There are three ways to show results from the programs: *emit*, *print with a newline* and
*print without a newline*.

To print the characters that correspond to ASCII codes, you can "EMIT" the code.
For instance a uppercase "A" use number 65 as its ASCII code. Thus, a "string" of
characters can consist of putting out series of codes.

```c
case EMIT:
	v = pop(vm);
	printf("%c", (char)v);
	break;
```

Another way to show results can be print with a new line at the end. As *enkel/0*
really only can represent positive integers, a number from the top of the stack
is printed with "PRINT".

```c
case PRINT:
	v = pop(vm);
	printf("%d\n", v);
	break;
```

The same goes for "PRNT", but without a new line at the end.

```c
case PRNT:
	v = pop(vm);
	printf("%d", v);
	break;
```
But "PRNT" has not been used in the compiler, so it stands left
as a possible extension for you to implement.


### misc

```c
case NOP:
	break;				
```
This "NOP" operation does nothing. It just been left here.

```c
case HALT:
	return;
```
The "HALT" is actually essential to stop the program and to return
to a higer level from which the program started.

```c
case SET:
	v = nextcode(vm);
	push(vm, v);
	break;
```

This operator "SET" pushes a value directly after the operation,
to the stack. Quite essential in out vm as it is stack based.
