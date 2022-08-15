# Virtual Machines

A very simple virtual machine implemented as a stack machine.
As an example: Push two numbers on the stack. Each at a time.
Then add the two numbers. Place the result back on stack. Then
print sum. Halt.

## vm1

A representation of a sample program is hard coded into `vm1.c`:

~~~~
int program[] = {
     SET, 33,
     SET, 44,
     ADD,
     PRINT,
     HALT
};
~~~~

```
   SET, 33,        <- store 33 on the stack, 33 on the top
   SET, 44,        <- next, store 44 on the stack, top now 44
   ADD,            <- add the two numbers on the stack, 33 + 44 = 77, and put the result on stack
   PRINT,          <- take what is on the stack and print (77)
   HALT            <- halt the program
```

Everything in the program is represented as integers (positive integers).
For instance `SET` is internally represented by a number (5), `ADD` is
represented by another number (2), and so on. A switch statement selects
each "instruction" and executes the corresponding routine.

```
...
     case SET:
     v = nextcode(vm);
     push(vm, v);
     break;
...
```

The instruction for storing numbers on the stack is `SET`. When executed,
the next instruction in line (a number), will be put on stack `push(vm, v)`
where *vm* represents the main structure for the virtual machine (program
counter, stack pointer ...) and *v* is the value to be put on the stack.

In `vm1.c` the important functions are:
- `VM* newVM(int* code, int pc)` which allocates vm, struct for the stack, code array, program counter (pc) and stack pointer (sp). 
- `void freeVM(VM* vm)` deallocates vm.
- `int pop(VM* vm)` moves the pointer (sp) at the array for the stack to pop a value, stack impl. here as a fixed array.
- `void push(VM* vm, int v)` push a value on stack.
- `int nextcode(VM* vm)` move the pointer (pc) at the array to the next code in line. Can be value or operation depending on previous code. 
- `run(VM* vm)` the "processor". Picks a code from the array, and finds out what the operation will do, and execute on it.

## run

Compile with gcc installed, and then run:

```
> gcc vm1.c
> ./a.out
```

Or, if not gcc installed:

```
> cc vm1.c -o vm1
> ./vm1
```

You should be able to see what 33 + 44 is ... (hint 77)


## portability

One of the many praised features of virtual machines is enabling *portability of code*.
You can try another version of the virtual machine in "alternate-vm.html", which you
can run in your browser. (Copy to the desktop and double-click.)
You will notice the program is the same in *principle* (as the opcodes can also be) so we only
implement a new virtual machine each time we would like to run the program on another
system, operating system, hardware, etc. Sun Microsystems Inc., the company originally
behind the programming language Java, once had a slogan: "Write Once, Run Anywhere"[^1],
that kind of illustrated that idea.

[^1] https://en.wikipedia.org/wiki/Write_once,_run_anywhere
