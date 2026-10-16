# Chapter 7: Watching the machine run

When a program prints the wrong number, all the machine has told you
is the wrong number. Everything that led to it happened out of
sight. This chapter makes the machine show its work, in three ways:

```
./vm program.vm           run, as before
./vm -t program.vm        trace: one line per step, on stderr
./vm -d program.vm        debug: stop, look, step, continue
```

and a fourth tool, [`replay.py`](replay.py), explores a saved trace
after the run is over, backwards as well as forwards.

## Splitting the loop

Until now `run()` was one loop with the whole machine inside it. Here
the body of the loop becomes a function of its own, `step()`, which
runs exactly one instruction. Then:

- `run()` calls `step()` until it returns 0,
- `trace()` calls `step()` and prints a line after each call,
- `debug()` calls `step()` when you tell it to.

Every debugger, from the 1960s' DDT to gdb, is built on the same
split: a machine that can be told to take *one step* and then be
looked at.

The machine also has to know the names of its own instructions now,
to print them. It has a `names` table, and a `noperands` table telling
how many operands follow each instruction.

## The trace

```
$ ./vm -t samples/gcd.vm
     1     0  PUSH 1071       1071
     2     2  PUSH 462        1071 462
     3     4  CALL 17 2       | 1071 462
     4    17  LOAD 1          | 1071 462 462
   ...
    17    28  CALL 17 2       | 1071 462 | 462 147 | 147 21
```

Each line holds the step number, the address, the instruction, and
the stack *after* the instruction ran. A bar `|` marks where a call's
frame begins, so you can watch the recursion go down, three calls
deep, and come back up again. What the program prints still goes to
standard output; the trace goes to standard error, so the two can be
kept apart: `./vm -t gcd.vm 2> trace.txt`.

## The debugger

```
$ ./vm -d samples/gcd.vm
    0  PUSH 1071
(vm) b 32
(vm) c
   32  LOAD 0
(vm) p
stack: | 1071 462 | 462 147 | 147 21 | 21 0
frame 4: returns to 31, locals start at 6
...
```

| Command  | Does |
|----------|------|
| `s [n]`  | step one instruction, or n |
| `c`      | continue until a breakpoint or the end |
| `b addr` | set a breakpoint |
| `d addr` | delete a breakpoint |
| `p`      | print the stack and the frames |
| `l [n]`  | list the next n instructions; `*` marks breakpoints |
| `q`      | quit |

The addresses are the ones in the assembler's listing (`asm.py -l`)
or the disassembler's output. If a program traps under the debugger,
the machine prints the stack as it was at that moment. The values the
failing instruction took off the stack are gone by then: in
[`tests/divzero.debug.out`](tests/divzero.debug.out) the 100 and the
0 of the division are no longer there.

## Replaying a trace

The debugger only goes forward. But when you find a wrong value,
the question is nearly always *where did it come from?*, which is
a question about the past. A trace is the whole past, written down.

```
$ ./vm -t samples/gcd.vm 2> trace.txt
$ python3 replay.py trace.txt
(replay) v 21          find the first step where 21 is on top
    16    27  MOD             | 1071 462 | 462 147 147 21
(replay) w             show the steps around it
(replay) b 28          back to the previous step at address 28
```

Debuggers that can go backwards are called *reverse* or *time-travel*
debuggers. gdb can do it, slowly; `rr` does it by recording a run,
which is the idea here at its smallest.

## Tests

The tests run a scripted debugger session and a scripted replay
session, and compare what they print, along with a whole trace,
against saved files in [`tests/`](tests). If you change the trace
format on purpose, check the new output by eye, then run
`make expected` to save it as the new expected output.

```
make test
```

## Exercises

1. Add `w addr` to the debugger: a *watchpoint* that stops whenever
   the instruction at `addr` changes the top of the stack.
2. Make `b` accept a label as well as an address. What would the
   machine need to know, and where could that come from? (Look at the
   end of [`FORMAT.md`](../ch05-files/FORMAT.md).)
3. Write a profiler: count how many times each address is executed
   and print the ten busiest. Which part of `primes` is hottest?
4. A trace of a long run is enormous. Instead of writing every step,
   record only what cannot be worked out again: here, nothing at
   all, since the machine is deterministic. What would change once
   the machine could read input?
