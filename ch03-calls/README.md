# Chapter 3: Calls and frames

In chapter 2 every value lived on one shared stack, and keeping track
of them was the program's whole job. A *function* changes that. When
`fact` is called it needs:

1. **a way back**: the address just after the `CALL`,
2. **its own values**: an `n` that the caller's values, and the
   values of other calls to `fact`, cannot disturb,
3. **a way to hand back a result**.

The machine in [`vm.c`](vm.c) keeps a second stack, of *frames*.
A frame records two numbers: where to return to (`ret`), and where
this call's values begin on the data stack (`fp`, the *frame
pointer*).

## What CALL and RET do

`CALL addr n` is used after the caller has pushed `n` arguments:

```
data stack before:   ... x  y  | 5          (5 is the argument)
                                 ^ fp of the new call
```

1. push a frame holding the current `pc` and `fp`,
2. set `fp` to point at the first argument,
3. jump to `addr`.

Inside the function, `LOAD 0` reads the first argument, `LOAD 1` the
second, and so on: the arguments *are* the function's first locals.
`STORE k` writes one.

`RET` takes the value on top as the result, throws away everything
the call left above `fp`, pops the frame to restore the caller's
`pc` and `fp`, and pushes the result. To the caller, `CALL fact 1`
behaves like one instruction that turned `n` into `fact(n)`.

## Recursion for free

Because frames are on a stack, `fact(5)` calling `fact(4)` calling
`fact(3)` ... each has its own frame and its own `n`. Nothing in the
machine knows or cares that it is the same function. This is the
idea Pascal's and C's run-time stacks are built on, and it is the
*activation record* of the old `vm3`.

## New instructions

| Code | Name  | Operand  | Effect                                   |
|------|-------|----------|------------------------------------------|
| 15   | LOAD  | k        | push local k                             |
| 16   | STORE | k        | pop into local k                         |
| 17   | CALL  | addr n   | new frame; first n stack values = locals |
| 18   | RET   |          | pop result, drop frame, push result      |

Codes 0 to 14 are unchanged from chapter 2.

## Run it

```
make test
```

## Exercises

1. Write `square(x)` and use it to print `square(3) + square(4)`.
2. Write `gcd(a, b)` with two arguments, recursively:
   `gcd(a, 0) = a`, `gcd(a, b) = gcd(b, a mod b)`. You will need a
   `MOD` instruction first.
3. A function with a local variable that is not an argument: the
   function can `PUSH 0` on entry to make room for it, and use it as
   local `n`. Rewrite factorial as a loop this way.
4. What happens with `fact(100000)`? Why? (Chapter 4.)
