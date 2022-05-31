# vm
Virtual machines samples

### vm1 -- compile with gcc installed; `gcc vm1.c` at the command line, then run with `./a.out`.

*A very simple virtual machine implemented as a stack machine.
As an example: Push two numbers on the stack. Each at a time.
Then add the two numbers. Place the result back on stack. Then print sum.*

> int program[] = {
        SET, 33,
        SET, 44,
        ADD,
        PRINT,
        HALT
};

In vm1.c the important functions are:
- **VM* newVM(int* code, int pc)** which allocates vm, struct for the stack, code array, program counter (pc) and stack pointer (sp). 
- **void freeVM(VM* vm)** deallocates vm.
- **int pop(VM* vm)** moves the pointer (sp) at the array for the stack to pop a value, stack impl. here as a fixed array.
- **void push(VM* vm, int v)** push a value on stack.
- **int nextcode(VM* vm)** move the pointer (pc) at the array to the next code in line. Can be value or operation depending on previous code. 
- **run(VM* vm)** the "processor". Picks a code from the array, and finds out what the operation will do, and execute on it.


### vm2 -- compile with gcc installed; `make` at the command line, then run `./fib`.

*A machine that takes inspiration from the programming language FORTH.
It can be seen that the language here is very close to both the stack operations
and the traditional machine/assembly language. Hence, programs can use and be optimized
in line of being "forthified" (adopted to suit FORTH).*
