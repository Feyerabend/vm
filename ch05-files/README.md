# Chapter 5: Programs in files

The machine of chapter 4 had its programs compiled into it. To run a
different program, you changed the C source and recompiled the
machine. That is fine for a demonstration and useless for anything
else.

This chapter separates the two. The machine is built once; programs
are files it reads.

```
$ python3 tobin.py samples/fib.txt samples/fib.vm
$ ./vm samples/fib.vm
0
1
1
...
```

No instructions are new. Only `main` changed, and a loader was added
in front of `run`: compare with chapter 4.

## The pieces

- [`FORMAT.md`](FORMAT.md) describes the file format: a magic number,
  a version, a length, then the code.
- [`vm.c`](vm.c) loads a file, checks it, and runs it.
- [`tobin.py`](tobin.py) turns a text listing such as
  `PUSH 2 PUSH 3 ADD PRINT HALT` into a `.vm` file.
- [`samples/`](samples) holds the programs of earlier chapters as
  text, and one new one, `primes.txt`.
- [`badfiles.py`](badfiles.py) writes files broken in every way the
  loader checks for, so the test can make sure each is refused.

## Two kinds of failure

A file can be wrong *as a file*: not a program at all, from a newer
version, cut short. Those are caught before any instruction runs, and
the machine exits with status 2. A file can also be a perfectly good
file holding a wrong program, which divides by zero or jumps off the
end. Those are traps, as in chapter 4, with status 1.

Keeping the two apart matters for whoever reads the message: one says
*this file is damaged*, the other says *this program has a bug*.

## Not yet an assembler

`tobin.py` translates names to numbers and nothing else. Look at
[`samples/primes.txt`](samples/primes.txt): every jump target is an
address counted by hand and written into a comment, and adding one
instruction near the top means recounting everything below it. That
is the problem chapter 6 solves with *labels*.

## Run it

```
make test
```

## Exercises

1. Write a program in a text file that prints the squares of 1 to 10,
   turn it into a `.vm` file, and run it.
2. Use a hex viewer (`xxd samples/gcd.vm`) and find the magic number,
   the length, and the first instruction.
3. Add one instruction near the top of `primes.txt`. How many numbers
   must you change? Which ones?
4. Make `tobin.py` check that an instruction which needs an operand
   actually gets a number after it, and not another instruction name.
