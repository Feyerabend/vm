# Chapter 2: Jumps

Chapter 1's machine ran each instruction once, top to bottom. To
repeat something, or to choose between two things, the machine has
to be able to put a different number in `pc`.

- `JMP addr` always continues at `addr`.
- `JZ addr` pops a value and continues at `addr` only if it was zero;
  otherwise it carries on with the next instruction.

With these two every loop and every `if` can be built. A `while`
loop is a `JZ` out of the loop at the top and a `JMP` back at the
bottom; that is the shape of the program in [`vm.c`](vm.c).

## Juggling the stack

Values on a stack have no names, so to use one twice, or to reach
one that is not on top, the machine needs instructions that only
rearrange. These come straight from FORTH:

| Name | Before  | After     |
|------|---------|-----------|
| DUP  | a       | a a       |
| DROP | a       |           |
| SWAP | a b     | b a       |
| OVER | a b     | a b a     |
| ROT  | a b c   | b c a     |

`LT` and `EQ` compare and leave `1` (true) or `0` (false), which is
exactly what `JZ` wants to see.

## The instructions so far

| Code | Name  | Operand | Effect                           |
|------|-------|---------|----------------------------------|
| 0    | HALT  |         | stop                             |
| 1    | PUSH  | n       | push n                           |
| 2    | ADD   |         | a b -> a + b                     |
| 3    | SUB   |         | a b -> a - b                     |
| 4    | MUL   |         | a b -> a * b                     |
| 5    | PRINT |         | a -> (print a)                   |
| 6    | JMP   | addr    | pc = addr                        |
| 7    | JZ    | addr    | a -> ; if a == 0 then pc = addr  |
| 8    | DUP   |         | a -> a a                         |
| 9    | DROP  |         | a ->                             |
| 10   | SWAP  |         | a b -> b a                       |
| 11   | OVER  |         | a b -> a b a                     |
| 12   | ROT   |         | a b c -> b c a                   |
| 13   | LT    |         | a b -> (a < b)                   |
| 14   | EQ    |         | a b -> (a == b)                  |

Codes 0 to 5 are the same as in chapter 1. A program written for
chapter 1 still runs here; the machine has grown, not changed.

## Run it

```
make test
```

## What is still missing

The Fibonacci program works, but follow the stack comments and see
how much of it is shuffling. With more than three values in play,
juggling becomes the whole program. Chapter 3 gives values a place
to stay: *frames*.

## Exercises

1. Write a program that prints the numbers from 1 to 10.
2. Compute `7 * 6` using only `ADD` and a loop.
3. `JZ` jumps on false. Add `JNZ`, which jumps on true, and rewrite
   the loop with it. Is the program shorter?
4. Our machine has `LT` but not `GT`. Show that it does not need it.
