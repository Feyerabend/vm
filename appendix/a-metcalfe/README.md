# A: The Metcalfe parsing machine

In 1964 Howard Metcalfe described a machine for one job: reading a
sentence and deciding whether it follows a grammar.[^1] It is a
virtual machine in the full sense: a small, fixed set of instructions,
and programs written for it, one per language. It is also older than
almost every machine in this book's background.

## The machine

The machine has an input tape of tokens, an output tape, one flag, and
a stack of calls. There are no numbers to add and no values on a
stack. Everything it does is a test, and the answer goes to the flag:

| Instruction | Does |
|-------------|------|
| `call L` | call the rule at `L` |
| `return` | return; if the flag is false, undo the rule |
| `match x` | if the next token is `x`, take it and set the flag, else clear it |
| `print x` | write `x` on the output tape |
| `true L`, `false L` | jump if the flag is set, or clear |
| `flag true`, `flag false` | set or clear the flag |
| `stop` | stop |

A grammar becomes a program almost word for word: each rule is a
subroutine, each alternative a test with a jump. Here is a factor,
`F = name | number | "(" E ")"`, from
[`samples/postfix.mc`](samples/postfix.mc):

```
F:      match ?
        false F1
        print ?
        true F9
F1:     match (
        false F9
        call E
        false F9
        match )
F9:     return
```

The one subtle instruction is `return`. Each `call` remembers where
on both tapes it began. If the rule ends with the flag clear, `return`
moves the input back to that point and takes away whatever the rule
wrote. So a rule that fails half way leaves no trace, and the caller
can try something else.

[`metcalfe.py`](metcalfe.py) is the whole machine and its assembler:
under 200 lines of Python. The details of `match ?` and `print ?`,
which take and copy any name or number, are ours, added so that the
examples can carry real names instead of a placeholder.

## Compared with ours

Our machine computes, and a parser for it, in chapter 12, was a
program in Python. Metcalfe's machine *only* parses, and the parser
is the program. The instruction set is chosen for the problem: the
flag is the only value, because a recognizer only ever needs to know
whether the last thing worked.

The postfix sample shows the two meeting. It turns infix into
postfix, which is exactly the order of operations a stack machine
needs:

```
a + b * c        =>  a b c * +
2 * (x + 1) / y  =>  2 x 1 + * y /
```

Prefix "PUSH" to every name and number, and the operators become
`ADD` and `MUL`: that is chapter 9's compiler, as a program for a
different machine.

## The limits of undoing

[`samples/choice.mc`](samples/choice.mc) shows how far `return` can
undo. Its grammar is `S = A B`, with `A = "a" "c" | "a"` and
`B = "c" "b" | "d"`. Each alternative of `A` is a rule of its own, so
when the first fails half way, its `return` puts the input back for
the second. But once `A` has returned successfully, nothing makes it
try again:

```
a c c b  =>  ac cb
a c b    =>  not accepted
```

`a c b` is in the language: `A` as `a`, then `B` as `c b`. The machine
never finds it, since `A` takes `a c` first and `B` is left with `b`.
This is *ordered choice*: the first alternative that matches wins.
Parsing expression grammars, forty years later, made the same choice
on purpose, and the combinators of chapter 12 behave the same way.

Schorre's META II, from the same year, is a close relative: a machine
with a flag, tests, calls and output, and a compiler written for it
that could compile itself.

## Run it

```
make test
echo "a + b * c" | python3 metcalfe.py samples/postfix.mc
echo "a + b" | python3 metcalfe.py -t samples/postfix.mc
```

With `-t`, the machine shows every step: the address, the
instruction, what is left of the input, and what it has written.

## Exercises

1. Change [`samples/postfix.mc`](samples/postfix.mc) so its output is
   assembly language for our machine: `PUSH 2`, `ADD`, and so on.
   Names are a problem; what could they become?
2. Add a unary minus to the grammar. Where must it go, and what does
   it print?
3. Change `samples/choice.mc` so that it accepts `a c b`. Can it be
   done by reordering alone? What does that cost for other inputs?
4. The machine's undoing is only as deep as one rule. Add an
   instruction that lets a rule try its alternatives again after it
   has returned. (This is *backtracking*, and it can take time
   exponential in the length of the input.)

[^1]: Howard H. Metcalfe, "A parameterized compiler based on
mechanical linguistics", *Annual Review in Automatic Programming*,
vol. 4, ed. Richard Goodman, Pergamon Press, 1964. Also see Mick
Farmer, *Compiler physiology for beginners*, Chartwell-Bratt, 1985.
