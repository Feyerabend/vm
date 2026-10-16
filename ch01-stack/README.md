# Chapter 1: A stack machine

A virtual machine, at its smallest, is a loop:

1. read the instruction at the program counter `pc`,
2. move `pc` past it,
3. do what the instruction says,
4. repeat until told to stop.

The machine in [`vm.c`](vm.c) keeps its working values on a *stack*.
`PUSH 2` puts a 2 on top. `ADD` takes the two top values off, adds
them, and puts the result back. Nothing is named; everything is "the
value on top" or "the one just under it".

```
PUSH 2      stack: 2
PUSH 3      stack: 2 3
ADD         stack: 5
PUSH 7      stack: 5 7
MUL         stack: 35
PUSH 5      stack: 35 5
SUB         stack: 30
PRINT       prints 30, stack is empty
```

This is the same order of operations as *Reverse Polish Notation*
on an HP calculator, and as the language FORTH: operands first, then
the operation. `(2 + 3) * 7 - 5` needs no parentheses once it is
written as `2 3 + 7 * 5 -`.

## The instructions

| Code | Name  | Operand | Effect                      |
|------|-------|---------|-----------------------------|
| 0    | HALT  |         | stop                        |
| 1    | PUSH  | n       | push n                      |
| 2    | ADD   |         | pop b, pop a, push a + b    |
| 3    | SUB   |         | pop b, pop a, push a - b    |
| 4    | MUL   |         | pop b, pop a, push a * b    |
| 5    | PRINT |         | pop a, print it             |

## Run it

```
make test
```

## What is missing, on purpose

- Nothing checks the stack. Pop an empty stack and the machine reads
  garbage; push too much and it writes past the array. Chapter 4
  turns these into proper errors.
- The program lives inside the C source. Chapter 5 gives programs a
  file format of their own.
- There is no way to repeat anything or make a decision. That is the
  next chapter.

## Exercises

1. Add `DIV`. What should happen on division by zero? (Write down
   your answer; chapter 4 gives one.)
2. Rewrite the program to compute `1 + 2 + 3 + 4 + 5` in two
   different instruction orders. Which one needs the deeper stack?
3. What is the largest stack depth the given program ever reaches?
