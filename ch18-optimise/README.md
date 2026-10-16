# Chapter 18: Optimising

Two ways to make the machine do less work for the same program. The
first changes the *program*: an optimiser that rewrites it into fewer,
cheaper instructions before it runs. The second changes the
*machine*: superinstructions, which run two instructions for the cost
of one dispatch. Neither changes what a program does, and the tests
are mostly about proving that.

## A peephole optimiser

[`opt.py`](opt.py) reads assembly language, as the compilers of
Part III write it, and writes it back improved. It looks at the
program through a small window, a few instructions at a time:

| Rule | Before | After |
|------|--------|-------|
| constant folding | `PUSH 2`, `PUSH 4`, `MUL` | `PUSH 8` |
| no effect | `PUSH a`, `DROP` (and `DUP`, `DROP`; `LOAD k`, `DROP`; `SWAP`, `SWAP`) | nothing |
| double negation | `LT`, `PUSH 0`, `EQ`, `PUSH 0`, `EQ` | `LT` |
| jump threading | `JMP L` where L is `JMP M` | `JMP M` |
| jump to next | `JMP L` where L is the next instruction | nothing |
| dead code | instructions no path reaches | nothing |

It repeats until nothing changes, since one rewrite often makes room
for another. Chapter 10 promised that the useless `PUSH 0, RET` after
every enkel/0 `return` would go: it is dead code, and it goes.

### Changing nothing, including the failures

The hard part is not the rewriting but knowing when it is allowed.
`PUSH 0, DROP` looks like it does nothing. On a full stack, though,
the `PUSH` traps with *stack overflow*, and without it, nothing does.
The optimised program would behave differently, in exactly the case
where behaving correctly matters most.

So the window rules are used only where chapter 17's analysis, here in
[`flow.py`](flow.py), says how deep the stack is. Then the optimiser
can see that a `PUSH` has room, and that no instruction in the window
is one that is certain to trap. And it assumes nothing about values:
`x + 0` is *not* simplified to `x`, because if x is a reference, the
`ADD` traps.

For a program the analysis cannot handle, one that uses `CALLI`, only
jump threading and dead code removal are done; they need no depths.
A program that uses numbers for code addresses (`JMP 17`) is left
alone, since moving code would make those numbers wrong. The
compilers always use labels.

Addresses do change, so a trap names a different address. Everything
else must be the same, and [`same.sh`](same.sh) checks it for every
program in the conformance suite, every sample from enkel/0, basal/0,
lambda/0 and assembly, and every benchmark: 91 programs. That is a
strong test of constant folding in particular. The suite's `wrap` and
`division` programs fold down to nothing but constants, so the
optimiser's own arithmetic, wrapping at 32 bits and rounding towards
zero, must agree with the machine's, case by case.

## Superinstructions

Chapter 16 counted which instructions most often follow which. Across
the benchmarks and samples:

| Pair | Share of all pairs run |
|------|-----:|
| `LOAD`, `PUSH` | 9.6 % |
| `LOAD`, `LOAD` | 6.0 % |
| `LT`, `JZ` | 4.1 % |
| `PUSH`, `SUB` | 3.1 % |
| `PUSH`, `LOADM` | 2.9 % |
| `ADD`, `STORE` | 2.9 % |
| `PUSH`, `ADD` | 2.3 % |
| `LOAD`, `ADD` | 2.1 % |

The threaded machine of chapter 16 now has a *superinstruction* for
each of these pairs, in [`super.h`](super.h): one handler that does
both, with one dispatch instead of two. When the threaded code is
built, the first instruction of each such pair gets the
superinstruction's label. The second keeps its own label, so a jump
straight to it still works.

Nothing in the specification changes. A superinstruction is not an
instruction a program can contain, only a way this machine runs two
of them. But the two halves must trap exactly as the two instructions
would. `PUSH, ADD` need not put the constant on the stack at all, but
on a full stack it must still say *stack overflow*, at the `PUSH`. And
a trap in the second half must name the second instruction's address.
[`tests/super`](tests/super) has a program for each such case,
including a jump into the middle of a pair.

## Measured

Instructions dispatched, without and with each technique:

|             | plain | optimised | super | both |
|-------------|------:|----------:|------:|-----:|
| fib         | 26,925,370 | 26,925,370 | 18,847,760 | 18,847,760 |
| loop        | 260,000,007 | 260,000,007 | 200,000,007 | 200,000,007 |
| sieve       | 23,636,044 | 23,636,044 | 14,743,494 | 14,743,494 |
| closures    | 26,477,794 | 26,477,794 | 24,380,514 | 24,380,514 |
| enkel-sieve | 56,905,612 | 56,905,612 | 41,765,809 | 41,765,809 |
| basal-loop  | 14,399,563 | 13,199,563 | 11,999,631 | 10,199,631 |

Superinstructions cut dispatches by 8 to 38 percent. The optimiser
does nothing for the hand-written benchmarks or for enkel/0's output,
and folds away 8 percent of `basal-loop`, where the program said
`2 * 4` and `10 / 5`.

Time, milliseconds, best of five, Clang 18 `-O2`:

|             | plain | optimised | super | both |
|-------------|------:|----------:|------:|-----:|
| fib         |  62 |  62 |  53 |  56 |
| loop        | 597 | 567 | 560 | 560 |
| sieve       |  48 |  57 |  60 |  72 |
| closures    |  72 |  54 |  65 |  66 |
| enkel-sieve | 101 |  99 |  92 |  99 |
| basal-loop  |  30 |  26 |  26 |  19 |

These numbers do not tell a clean story, and that is the honest
result. The "plain" and "optimised" columns for `fib` run the *same*
program, so differences of 10 or 20 percent are noise on this machine.
Beyond the noise, superinstructions help a little, sometimes. With
GCC 13, `loop` even got slower with them: a bigger interpreter
function can make the compiler's job harder, and that can cost more
than the dispatches saved.

This agrees with chapter 16: on today's processors, dispatch is no
longer the main cost of this machine. Fewer dispatches is only worth
it when each one is expensive. What *is* expensive here is checking:
every `ADD` checks two tags, every `pop` checks for underflow. The
register machine of chapter 17 was twice as fast partly because it
had proved, before running, that most of those checks were
unnecessary. Chapter 19 does the same for the stack machine.

## Run it

```
make test
make measure
```

## Exercises

1. Add a rule for `STORE k`, `LOAD k`, which is common in enkel/0's
   output. Is `DUP`, `STORE k` really better? Measure it.
2. Choose superinstructions automatically: profile a set of programs,
   pick the 8 most common pairs, and generate `super.h` from them.
3. Add superinstructions of *three* instructions, such as `LOAD`,
   `PUSH`, `ADD`. How many dispatches do they save on `loop`?
4. The optimiser cannot fold `x * 2 * 3`, because the multiplication
   by 2 comes first. What would it need to know to rewrite it as
   `x * 6`? Is that rewrite even correct, with wrapping arithmetic?
