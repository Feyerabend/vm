# Chapter 12: Three ways to parse

Chapters 9, 10 and 11 all parsed by *recursive descent*: one function
per grammar rule. It is the most common way to write a parser by
hand, and not the only one. This chapter parses one language three
ways, and makes them prove they agree.

The language is chapter 9's, with two comparisons added at the
loosest precedence:

```
2 + 3 * 7 < 30;         # 1, since 23 < 30
(1 < 2) + (3 = 3);      # 2
```

## The three parsers

**[`descent.py`](descent.py): recursive descent.** One function per
precedence level, each calling the next tighter one. The comparisons
cost a new grammar rule and a new function on top of the ladder.

**[`pratt.py`](pratt.py): Pratt parsing.** Vaughan Pratt's 1973 idea,
*top down operator precedence*. There is no ladder of functions, only
a table of *binding powers* and one loop:

```python
INFIX = {
    "<": 10, "=": 10,
    "+": 20, "-": 20,
    "*": 30, "/": 30, "%": 30,
}
```

To parse an expression, take an operand, then keep taking operators,
but only those that bind more tightly than whatever asked for the
expression. The comparisons cost two lines in the table. Pratt
parsers are what many modern compilers use for expressions, because
languages with fifteen precedence levels, like C, would otherwise
need fifteen functions.

**[`combinators.py`](combinators.py): parser combinators.** A parser
is a value: a function from a position in the tokens to what it found
there. Bigger parsers are built from smaller ones by ordinary
functions: `seq`, `alt`, `many`. The grammar is then written down
almost as it reads:

```python
product    = chain_left(unary, "*/%")
total      = chain_left(product, "+-")
comparison = chain_left(total, "<=")
statement  = apply(seq(comparison, token(";")), lambda v: v[0])
```

This is the idea of the earlier `archive/parse`, here working on
tokens and building the same trees as the other two.

All three share the scanner, the tree and the code generator, in
[`common.py`](common.py). Only parsing differs.

## Proving they agree

Each tree can be written as an *s-expression*, a line of text that
shows its shape: `2 + 3 * 7 < 30` is `(< (+ 2 (* 3 7)) 30)`.

```
$ python3 compile.py -pratt -tree samples/compare.expr
(< 1 2)
(< (+ 2 (* 3 7)) 30)
...
```

The test takes 500 random expressions from the fuzzer of chapter 9,
now with comparisons, and checks with [`same.py`](same.py) that all
three parsers build exactly the same 500 trees. It then checks that
the three produce byte-for-byte the same assembly, and that the
program prints the right values.

A Pratt parser with one mistake in it, making `-` group from the
right, fails at the second statement:

```
statement 2: descent and pratt differ
  (/ (- (% (neg ...
  (/ (- (% (neg ...
```

## Where they differ: error messages

Given the same mistakes, the parsers say different things:

```
-descent:     tests/two.expr:1:3: expected ';', found '2'
-pratt:       tests/two.expr:1:3: expected ';', found '2'
-combinators: tests/two.expr:1:3: expected '%' or '*' or '+' or '-' or '/' or ';' or '<' or '=', found '2'
```

The combinator parser is *right*: any of those tokens could have come
next. But it is less helpful. A hand-written parser knows what the
writer of a program most likely meant; a parser built mechanically
from a grammar knows only what the grammar allows. The usual fix,
used here, is to report the failure that got *furthest* into the
input, which finds the place of the mistake reliably. Saying what the
mistake was, well, takes knowledge that is not in the grammar.

## Speed

On one computer, parsing about 82,000 tokens: recursive descent
60 ms, Pratt 54 ms, combinators 142 ms. Combinators pay for their
flexibility in function calls. For a compiler this rarely matters;
for a parser that runs on every keystroke in an editor, it can.

## Which to use?

- **Recursive descent** for whole languages, when you want the best
  error messages and full control. Most production compilers,
  including GCC's and Clang's C front ends, are hand-written recursive
  descent.
- **Pratt** for expressions, inside a recursive descent parser for
  everything else. This is a very common combination.
- **Combinators** when the grammar changes often, or must be built
  while the program runs, or in functional languages where they are
  natural: Haskell's Parsec is the classic.

A fourth family is missing here: *generated* parsers, from tools like
yacc, Bison or ANTLR, which read a grammar and write the parser for
you. They are the descendants of the table-driven ideas behind the
Metcalfe machine in `archive/metcalfe`, and they deserve a chapter
of their own in the appendix.

## Run it

```
make test
```

## Exercises

1. Add `^` for powers, right-associative, to all three parsers. Which
   took the fewest changes?
2. Add a conditional expression `a ? b : c` at the loosest precedence.
   In the Pratt parser, `?` is an infix operator that parses two more
   expressions. Where does the `:` get checked?
3. Make the combinator parser's error messages better without
   writing any special cases, using only information in the grammar.
   (Hint: label the parsers: `comparison` could be called "an
   expression".)
4. Write a fourth parser: the *shunting-yard* algorithm of Edsger
   Dijkstra, which uses two stacks instead of recursion. Add it to
   `same.py`.
