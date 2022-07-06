# Virtual Machines
Virtual machines samples[^1]. A collection of virual machines to teach or understand some
ideas and inner workings of virtual machines. They are solely intended for show of principles,
and not for uses in any other way.

[^1]: My best inspiration for the simple machines here comes from Bartosz Sypytowski:
https://bartoszsypytkowski.com/simple-virtual-machine/ from whom I derived most of the code,
even though some bugs were corrected.

## vm1
### compile with gcc installed; `gcc vm1.c` at the command line, then run with `./a.out`.

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

In `vm1.c` the important functions are:
- `VM* newVM(int* code, int pc)` which allocates vm, struct for the stack, code array, program counter (pc) and stack pointer (sp). 
- `void freeVM(VM* vm)` deallocates vm.
- `int pop(VM* vm)` moves the pointer (sp) at the array for the stack to pop a value, stack impl. here as a fixed array.
- `void push(VM* vm, int v)` push a value on stack.
- `int nextcode(VM* vm)` move the pointer (pc) at the array to the next code in line. Can be value or operation depending on previous code. 
- `run(VM* vm)` the "processor". Picks a code from the array, and finds out what the operation will do, and execute on it.


## vm2
### compile with gcc installed; `make` at the command line, then run `./fib`.

*A machine that takes inspiration from the programming language FORTH.
It can be seen that the language here is very close to both the stack operations
and the traditional machine/assembly language. Hence, programs can use and be optimized
in line of being "forthified" (adopted to suit FORTH thinking).*

The sample choosen to illustrate extended from the previous vm1-machine is the Fibonacci series:
1, 1, 2, 3, 5, 8, 13 ... which can be defnied as a mathematical recursive function:

```
F(0) = 0
F(1) = 1
F(n) = F(n − 1) + F(n − 2), n > 1
n ∈ ℕ
```

Applied from the FORTH-thinking we have the following operations at the core:

```
TWODUP
ADD
ROT
DROP
```

First duplicate what is already on stack, the two top items `TWODUP` (or `2DUP`),
such that if we have "1 2" after would be left with "1 2 1 2".
Next add the two numbers on the stack "1 2" becomes "3", and the first two still
are there such that "1 2 3". Then rotation `ROT` would get "2 3 1", and we then `DROP` the top,
"2 3". That is, the numbers that remain will be added next time. And so on. 

## vm3
### compile with gcc installed; sample `make bin` at the command line, then run by `./bin`.

The VM has been extended with some new features, which makes it a little bit more powerful.
There are added some extra jump instructions to the vm, also comparations and a storage facility to
accomodate for iterations (vs. vm1). Moreover there is also a small framework for call/return.
You can store arguments which can be retrieved, use local variables in the function / procedure,
and return value. The "activation records", usually associated with call/return and stack machines,
are stored on the stack, with the exception for arguments used with the call (parameters). These
"records" are alternatives to the heap solution for memory allocation. The most obvious problem
with activation records (vs. heap) are that memory allocations have to be known at compile time.
Futher, there are also both global variables and local variables.

Besides the VM there is also an assembler to simplify programming. It is written in *Python3* which
ease the handling of strings, and have some nice features for list processing.[^2] Using C would be
a bit longer and perhaps harder to read code.

Still we have no debugging support, error messaging, file handling, etc. you can find in any
corresponing system. The purpose here is to be as clear as possible to what goes on with regard
to the machine rather than other stuff. It is thus NOT for use with any other purpose than to teach
and understand som simple principles of what a VM could be.

[^2]: Here I borrowed some useful but confusing code from
https://github.com/amsanei/Assembler-with-python.

#### Sample

To test this VM, try a program named `bin` for translating decimal numbers to binary.
First start with the assembly text in `bin.a` and convert it to the appropiate machine code:

```
> python3 ./asm.py bin.a bin.b
```

Which convert the assembly code in `bin.a` to the machine code for VM3. There is also a file named
`bin.b` which contains the machine code. Then copy the code produced either from screen (if available)
or from the generated file `bin.b`. Open the c-file `bin.c` with an editor, and paste the code (replace)
in the array named "program". Save the c-file `bin.c` with your changes. Now:

```
> make clean
> make bin
```

Then, if everything worked, no errors were produced, then run it by:

```
> ./bin
```

A binary number should appear on the screen.



The same procedure goes for the other samples `factorial` and `prime` (numbers).



