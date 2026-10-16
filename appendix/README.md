# Appendix: Other machines

The book built one machine, and made one choice at every turn: a
stack, not registers; 32-bit words; addresses fixed by the assembler;
values tagged and checked while running; a written specification,
and tests. Other machines chose differently, and each choice was
right for something.

These six short studies each take a machine that is not ours, run a
small version of it, and look at the one or two decisions that make it
different. Each is a single Python file with no dependencies, a few
sample programs, and `make test`.

| Study | Machine | Year | What it chose differently |
|-------|---------|------|---------------------------|
| [A](a-metcalfe) | Metcalfe's parsing machine | 1964 | A machine for one problem: its only value is a flag, and failing undoes itself. |
| [B](b-pcode) | Wirth's P-machine, and UCSD p-code | 1976 | Static links, for procedures nested in procedures. |
| [C](c-chip8) | CHIP-8 | 1977 | Registers, graphics by XOR, and no specification, with the quirks that followed. |
| [D](d-sweet16) | SWEET16 | 1977 | Small code over speed, and a machine entered and left in the middle of native code. |
| [E](e-postscript) | PostScript | 1984 | Names looked up while running, procedures as data, and pictures as programs. |
| [F](f-jvm) | The Java Virtual Machine | 1995 | A constant pool instead of addresses, and types in the instructions, checked before running. |

They can be read in any order, after the chapters they refer to. Each
says which.

```
make test
```

runs all six. The JVM study also runs the real JVM on its programs
when `java` is installed, and checks that both machines agree.
