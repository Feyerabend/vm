# The instruction set

Every instruction is one integer, followed by its operands, if any,
as further integers. Values are 32-bit signed integers; from chapter
13 on, a value can also be a reference to a block on the heap. From
chapter 5 on, programs are stored in files as described in
[`ch05-files/FORMAT.md`](ch05-files/FORMAT.md).

An instruction never changes number or meaning once added. The
*since* column gives the chapter where it first appears.

Stack effects are written `before -> after`, with the top of the
stack on the right.

| Code | Name  | Operands | Stack effect      | Since | Meaning |
|------|-------|----------|-------------------|-------|---------|
| 0    | HALT  |          |                   | 1     | Stop the machine. |
| 1    | PUSH  | n        | `-> n`            | 1     | Push the number n. |
| 2    | ADD   |          | `a b -> a+b`      | 1     | |
| 3    | SUB   |          | `a b -> a-b`      | 1     | |
| 4    | MUL   |          | `a b -> a*b`      | 1     | |
| 5    | PRINT |          | `a ->`            | 1     | Print a in decimal, then a newline. |
| 6    | JMP   | addr     |                   | 2     | Continue at addr. |
| 7    | JZ    | addr     | `a ->`            | 2     | Continue at addr if a is 0. |
| 8    | DUP   |          | `a -> a a`        | 2     | |
| 9    | DROP  |          | `a ->`            | 2     | |
| 10   | SWAP  |          | `a b -> b a`      | 2     | |
| 11   | OVER  |          | `a b -> a b a`    | 2     | |
| 12   | ROT   |          | `a b c -> b c a`  | 2     | |
| 13   | LT    |          | `a b -> a<b`      | 2     | 1 if true, 0 if false. |
| 14   | EQ    |          | `a b -> a==b`     | 2     | 1 if true, 0 if false. |
| 15   | LOAD  | k        | `-> local[k]`     | 3     | Push local k of the current frame. |
| 16   | STORE | k        | `a ->`            | 3     | local[k] = a. |
| 17   | CALL  | addr n   | (see chapter 3)   | 3     | Call addr; the top n values become locals 0 to n-1. |
| 18   | RET   |          | (see chapter 3)   | 3     | Return the top value to the caller. |
| 19   | DIV   |          | `a b -> a/b`      | 4     | Rounded toward zero. Traps if b is 0. |
| 20   | MOD   |          | `a b -> a%b`      | 4     | Sign follows a. Traps if b is 0. |
| 21   | AND   |          | `a b -> a&b`      | 10    | Bitwise. |
| 22   | OR    |          | `a b -> a\|b`     | 10    | Bitwise. |
| 23   | XOR   |          | `a b -> a^b`      | 10    | Bitwise. |
| 24   | LOADM |          | `a -> mem[a]`     | 10    | Read memory. Traps outside 0 to 4095. |
| 25   | STOREM |         | `a v ->`          | 10    | mem[a] = v. Traps outside 0 to 4095. |
| 26   | EMIT  |          | `c ->`            | 10    | Write the byte c, 0 to 255. |
| 27   | NEW   |          | `n -> r`          | 13    | A new block of n fields, all 0. |
| 28   | GETF  |          | `r i -> v`        | 13    | Field i of block r. Traps out of bounds. |
| 29   | SETF  |          | `r i v ->`        | 13    | Field i of block r = v. Traps out of bounds. |
| 30   | LEN   |          | `r -> n`          | 13    | The number of fields of block r. |
| 31   | CALLI | n        | `t -> ...`        | 15    | As CALL, to the address t taken from the stack. |

## Traps

From chapter 4 on, the machine checks every step. When a step would
fail, the machine stops with exit status 1 and prints
`trap: <reason> at <address>` on standard error, where the address is
that of the failing instruction. Output printed before the trap is
kept. The reasons are listed in [chapter 4](ch04-traps/README.md).

In chapters 1 to 3 the same situations are undefined.

Until chapter 8, overflow of `ADD`, `SUB`, `MUL` and `DIV` is
undefined.

## The specification

From chapter 8 on, the machine is defined by a specification:
version 1 in [`ch08-spec/SPEC.md`](ch08-spec/SPEC.md), and version 2,
which adds memory and codes 21 to 26, in
[`ch10-enkel/SPEC.md`](ch10-enkel/SPEC.md), and version 3, which adds
the heap, references and codes 27 to 30, in
[`ch13-heap/SPEC.md`](ch13-heap/SPEC.md), and version 4, which adds
code 31, in [`ch15-closures/SPEC.md`](ch15-closures/SPEC.md). This
table is a summary. Where they differ, the specification is right. It settles what
the table leaves open: arithmetic wraps at 32 bits, every instruction
carries out its steps in a fixed order, and `STORE` pops its value
before it checks the local.
