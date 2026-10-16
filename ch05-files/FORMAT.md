# The .vm file format, version 1

A `.vm` file holds one program. All numbers in it are 32-bit signed
integers, stored *little-endian*: least significant byte first.

| Offset | Size  | Contents |
|--------|-------|----------|
| 0      | 3     | the magic number: the bytes `S`, `V`, `M` |
| 3      | 1     | the format version: `1` |
| 4      | 4     | n, the number of code words, 1 to 65536 |
| 8      | 4 × n | the code words, from address 0 upward |

The file ends right after the last code word.

A file that breaks any of these rules is refused before it runs:
the machine prints `<file>: <reason>` on standard error and exits
with status 2. A program that loads but then fails while running is a
trap, with exit status 1, as in chapter 4.

## Why each part is there

**The magic number** lets the machine tell a program from any other
file at once, rather than running a JPEG and trapping a few
instructions later. Most binary formats start with one: `\x7fELF`
for Linux programs, `CAFEBABE` for Java class files, `%PDF` for PDFs.

**The version** makes it possible to change the format later
without old machines quietly misreading new files.

**The length** lets the machine check that the whole program is
there, and that nothing follows it. A file cut short by a failed copy
is caught on loading, not discovered as a strange trap halfway
through a run.

**Little-endian, always** means a file written on one computer runs
on another, whatever order that computer keeps the bytes of its own
integers in. The loader builds each word from its four bytes, so it
never depends on the byte order of the computer it runs on.

## What is not here

There is nothing but code. Real formats also carry data (strings,
constants), a table of names for debugging, and the address to start
at. This book never needs them: its compilers build strings with
instructions, and traps name addresses, which the assembler's listing
turns back into lines. Designing a version 2 that carries names is a
good exercise; chapter 7 suggests why a debugger would want it.
