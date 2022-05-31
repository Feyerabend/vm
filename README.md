# vm
Virtual machines samples

vm1 -- compile with gcc installed; `gcc vm1.c` at the command line, then run with `./a.out`.

*A very simple virtual machine implemented as a stack machine.
As an example: Push two numbers on the stack. Each at a time.
Then add the two numbers. Place the result back on stack. Then print sum.*

vm2 -- compile with gcc installed; `make` at the command line, then run `./fib`.

*A machine that takes inspiration from the programming language FORTH.
It can be seen that the language here is very close to both the stack operations
and the traditional machine/assembly language. Hence, programs can use and be optimized
in line of being "forthified" (adopted to suit FORTH).*
