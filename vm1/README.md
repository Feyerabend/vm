# Virtual Machines

A very simple virtual machine implemented as a stack machine.
As an example: Push two numbers on the stack. Each at a time.
Then add the two numbers. Place the result back on stack. Then
print sum. Halt.

## vm1

A representation of a sample program is hard coded into `vm1.c`:

> int program[] = {
        SET, 33,
        SET, 44,
        ADD,
        PRINT,
        HALT
};

In `vm1.c` the important functions are:
- `VM* newVM(int* code, int pc)` which allocates vm, struct for the stack, code array, program counter (pc) and stack pointer (sp). 
- `void freeVM(VM* vm)` deallocates vm.
- `int pop(VM* vm)` moves the pointer (sp) at the array for the stack to pop a value, stack impl. here as a fixed array.
- `void push(VM* vm, int v)` push a value on stack.
- `int nextcode(VM* vm)` move the pointer (pc) at the array to the next code in line. Can be value or operation depending on previous code. 
- `run(VM* vm)` the "processor". Picks a code from the array, and finds out what the operation will do, and execute on it.

## run

Compile with gcc installed, e.g.:

```
> gcc vm1.c
> ./a.out
```

Or if not gcc installed:

```
cc vm1.c -o vm1
./vm1
```

You should be able to see what 33 + 44 is ...
