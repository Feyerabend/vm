# Virtual Machines

## vm2

Compile with gcc installed; `make` at the command line, then run `./fib`.

*A machine that takes inspiration from the programming language FORTH.
It can be seen that the language here is very close to both the stack operations
and the traditional machine/assembly language. Hence, programs can use and be optimized
in line of being "forthified" (adopted to suit FORTH thinking).*

The sample chosen to illustrate extended from the previous vm1-machine is the Fibonacci series:
1, 1, 2, 3, 5, 8, 13 ... which can be defined as a mathematical recursive function:

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
