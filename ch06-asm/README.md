# Chapter 6: An assembler

Part II begins. The machine itself is finished for now: [`vm.c`](vm.c)
is chapter 5's, unchanged. This part is about the tools that make the
machine usable.

Look again at chapter 5's [`primes.txt`](../ch05-files/samples/primes.txt).
Every jump target is a number counted by hand, and every comment
carries an address so the counting can be checked. Insert one
instruction near the top and every number below it is wrong.

Here is the same program in [`samples/primes.asm`](samples/primes.asm):

```
main:   PUSH 2
next:   LOAD 0
        PUSH 50
        LT
        JZ end
        ...
        JMP next
end:    HALT
```

`next:` is a *label*. It names the address of the instruction that
follows it, and `JMP next` jumps there. Nobody counts; the assembler
does. Both files produce exactly the same bytes, and the test checks
this for the samples.

## Two passes

How can `JZ end` be translated before the assembler has seen where
`end` is? It cannot, in one reading. So [`asm.py`](asm.py) reads the
source twice:

1. **Counting.** Go through every line, work out how many words its
   instruction needs, and so the address of every line. Whenever a
   label appears, write down the current address.
2. **Writing.** Go through again and produce the code. Every label
   now has a known address, including the ones defined further down.

That is the *two-pass assembler*, and it has looked like this since
the 1950s.

## Checks

A good tool catches mistakes before they become traps. The assembler
checks that:

- every instruction exists,
- it has exactly the number of operands it needs,
- each operand is the right kind: a number, a local, or an address,
- every label used is defined, and none is defined twice,
- every number fits in 32 bits.

It reports *all* the mistakes it finds, not just the first, each with
its line number. See [`tests/errors.asm`](tests/errors.asm) and the
messages it must produce in [`tests/errors.txt`](tests/errors.txt).

## One table, two tools

[`isa.py`](isa.py) describes the instruction set as data: name, code,
and the kinds of operand each instruction takes. Both the assembler
and the disassembler read that one table. Before, the instruction set
was written down in `vm.c`, in `tobin.py` and in `ISA.md`, three
copies that could drift apart. Now the Python tools share one. The C
machine still has its own copy; chapter 8 makes sure they agree.

## The disassembler

[`disasm.py`](disasm.py) goes the other way: from a `.vm` file to
assembly language.

```
$ python3 disasm.py samples/gcd.vm
        PUSH 1071           ; 0
        PUSH 462            ; 2
        CALL L17 2          ; 4
        ...
L17:    LOAD 1              ; 17
        JZ L32              ; 19
```

Label names are not stored in the file, only addresses, so the
disassembler invents `L17` for address 17. A word it cannot read as
an instruction becomes `.word`. Either way, what it writes assembles
back into the identical file, and the test checks that for every
sample.

## The listing

`asm.py -l` prints, beside each source line, its address and the
words it became:

```
    4  17 17 2                  CALL gcd 2
```

When a program misbehaves at "address 28", the listing tells you
which line that was. Chapter 7 makes much more of this.

## Run it

```
make test
```

## Exercises

1. Write a program that prints the multiplication table for 7, using
   labels throughout.
2. Add `EQU`, so that `size EQU 50` lets `PUSH size` mean `PUSH 50`.
   Which pass has to handle it?
3. The disassembler cannot tell code from data. Write a program where
   it gets confused, and explain why no disassembler can avoid this
   in general.
4. Make the assembler warn about code that can never be reached,
   such as an instruction directly after a `JMP` with no label.
