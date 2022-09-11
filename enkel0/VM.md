# Virtual Machines

The virtual machine consists of essentially two files plus header files. The real
point of the virtual machine is to seperate running from the construction of the
runnable.

We have a machine in `enkelvm.c` and `enkelvm.h`, and loading code and directing
the machine is done through `runvm.c`. The only thing to be added is the "binary"
code for the program.


## runvm

The limits of the machine are defined in the runner `runvm.c`. Variables, globals, 
stack, etc. are set from the start. Will it hit a wall, and you have the hardware,
the limits might be changed by you.

Before loading, the length of the input file is measured. The "binary" have integers
seperated by commas, throughout. It also in a certain format, where the first number
points to where the *vm* should start. The rest of the file is the program itself.

![File format for enkel/0](../assets/images/fileformat.png)

A header of one (1) integer (separeted with a comma before the body) signals
where to start. The rest is read in an array to be executed, starting at the
postition where the `START` label was poiting before the assembler did its thing.

The runner measures the time from when the program starts until it finishes, and
prints the duration.

...


## vmenkel

The virtual machine has in main been described earlier, and not much have changed.






### call/return

Activation records ..

```
case CALL:
	addr = nextcode(vm);	// CALL <address>
	push(vm, vm->fp);	// push the frame pointer to stack
	push(vm, vm->pc);	// push the program counter to stack
	vm->fp = vm->sp;	// set the fram pointer to what the stack pointer is
	vm->pc = addr;		// set the program counter to the what the argument is: addr
	break;
```


```
case RET:
	vm->sp = vm->fp;	// reset the stackpointer from the frame pointer
	vm->pc = pop(vm);	// pop the top element as the new program counter
	vm->fp = pop(vm);	// pop the (new) top and set the frame pointer
	break;
```


### passing parameters

Passing arguments ..

```
case STARG:
	v = pop(vm);		// pop the value
	addr = nextcode(vm);	// STARG <address>
	vm->args[addr] = v;	// store the value at address
	break;
```

```
case LDARG:
	addr = nextcode(vm);	// LDARG <address>
	v = vm->args[addr];	// load value from where the address points
	push(vm, v);		// push the value
	break;
```

### local variables

Local storage ..

```
case ST:
	v = pop(vm);
	offset = nextcode(vm);
	vm->vars[vm->fp + offset] = v;
	break;
```

```
case LD:
	offset = nextcode(vm);
	v = vm->vars[vm->fp + offset];
	push(vm, v);
	break;
```

### global variables

Global storage ..

```
case LOAD:
	addr = nextcode(vm);
	v = vm->vars[addr];
	push(vm, v);
	break;
```

```
case STORE:
	v = pop(vm);
	addr = nextcode(vm);
	vm->vars[addr] = v;
	break;
```


### arrays


```
case RLOAD:
	a = pop(vm);
	v = vm->arrs[a];
	push(vm, v);
	break;
```
```
case RSTORE:
	a = pop(vm);
	b = pop(vm);
	vm->arrs[a] = b;
	break;

```






### jump

Jumping

```
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

