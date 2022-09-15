# Virtual Machines

The virtual machine consists of essentially two files plus header files. The real
point of the virtual machine is to seperate running from the construction of the
runnable.

We have a machine in `enkelvm.c` and `enkelvm.h`, and loading code and directing
the machine is done through `runvm.c`. The only thing to be added is the "binary"
code for the program.


## runvm

The limits of the machine are defined in the runner `runvm.c`. Variables, globals, 
stack, etc. are set from the start. Will it hit a wall concerning memory, and you
have the hardware, the limits might be changed by you.

Before loading, the length of the input file is measured. The "binary" have integers
seperated by commas, throughout. It also in a certain format, where the first number
points to where the *vm* should start. The rest of the file is the program itself.

![File format for enkel/0](../assets/images/fileformat.png)

A header of one (1) integer (separated with a comma before the body) signals
where to start. The rest is read in an array to be executed, starting at the
postition where the `START` label was poiting before the assembler did its thing.

The runner measures the time from when the program starts until it finishes, and
prints the duration.

...


## vmenkel


### addition, subtraction, division, multiplication

The virtual machine has in main been described earlier, and not much have changed
concerning the familiar arithmetical operations. The implemetation should be
recognized as strait forward.

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
		push(vm, a / b);
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

We have added a unary minus which have an easy implemetation in C. Also a runtime
error is raised when a division by zero occurs (rather than have C to work this out).


### modulus, and, or, xor


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

Activation records ..

```c
case CALL:
	addr = nextcode(vm);	// CALL <address>
	push(vm, vm->fp);	// push the frame pointer to stack
	push(vm, vm->pc);	// push the program counter to stack
	vm->fp = vm->sp;	// set the fram pointer to what the stack pointer is
	vm->pc = addr;		// set the program counter to the what the argument is: addr
	break;
```


```c
case RET:
	vm->sp = vm->fp;	// reset the stackpointer from the frame pointer
	vm->pc = pop(vm);	// pop the top element as the new program counter
	vm->fp = pop(vm);	// pop the (new) top and set the frame pointer
	break;
```



### passing parameters

Passing arguments ..

```c
case STARG:
	v = pop(vm);		// pop the value
	addr = nextcode(vm);	// STARG <address>
	vm->args[addr] = v;	// store the value at address
	break;
```

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
the arrays is used an index will point to the offset given the base. So a global
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

Jumping or branching is done through altering the address of the programcounter
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
	if (v != 0) {		// if value not zero, ..
		vm->pc = addr;	// .. then go to address
	}
	break;

case JPZ:
	addr = nextcode(vm);	// JPZ <address>
	v = pop(vm);		// pop value
	if (v == 0) {		// if value is zero, ..
		vm->pc = addr;	// .. then go to address
	}
	break;
```

