# Virtual Machines

*Combinator parsers*[^combpar] are a way to parse e.g. programming languages.
It could be argued that traditional recursive decent parsers are close to
combinator parsers. But there are some differences, such as the latter
have very tight relationship with mathematics, and with functional languages.
Traditional parsers rather have a more imperative and closeer relationship
to the machine.

First we take a look at simple combinator parsers that includes familiar
parsing of expressions with an infix order of the operators.

[^combpar]: More on combinator parsers:
https://gdevanla.github.io/posts/write-a-parser-combinator-in-python.html,
and https://en.wikipedia.org/wiki/Parser_combinator.


## run

Try running a script 'arith.py':

```shell
> python3 arith.py
```

It will parse the arithmetical expression '3 + 2 * (x - 4) / y' and
the result will be:

```shell
Parsed result: [[[[], 3, [' ']]], ([[], '+'], [[[' '], 2, [' ..
```

We will ignore this result for the moment, but focus on that it
(should have) parsed the expression sucessfully.

Looking at the code we can e.g. see how parsing a character is done:

```python
def char(c):
    def parser(text, pos):
        if pos < len(text) and text[pos] == c:
            return c, pos + 1
        return None, pos
    return parser
```

First to notice is that the 'def' returns another 'def'. That is, the
assumed parser really returns another parser. The inner parser returned
here test from the text, the first character. If it finds one, it
returns the character and also advances the parser one step in the text.

This is not so much different from what happends in a traditional 
parser, e.g. recursive decent parser, we have seen before. What is 
different is the *use* of functions, and later (re)use of functions
(lazily).

If we take another parser for 'whitespace':

```python
def whitespace():
    return many(choice(char(' '), char('\t'), char('\n')))
```

we can see that the most inner parser have a 'choice' between
characters, a space, a tabulator mark, and a newline.

Looking at 'choice':

```python
def choice(*parsers):
    def parser(text, pos):
        for p in parsers:
            res, pos = p(text, pos)
            if res is not None:
                return res, pos
        return None, pos
    return parser
```

it looks for parsers inside, and with the first
success for the returning parser, it accepts it
as the choice and returns the resulting returned
text, but also the position where the match was made.

In a way this reflects how grammars work with
choises, as we have seen before with '|'. The 'defs'
works as or corresponds to the definitions in the grammar.


## enbf

We are already acquainted with some formalizations of
language syntax in "Backus-Naur Form" (BNF) or
"Extended Backus-Naur Form" (EBNF) or some versions
of them. Both forms are used as notations to express
context-free grammars. Below are the EBNF notations
for both the *prefix* and the
*infix expression* as described in the examples.


### infix

Infix notation is the more conventional form where
operators are placed between operands. The EBNF for
infix notation that corresponds to the previous
prefix examples would look like this:

```ebnf
expression  ::= term {("+" | "-") term}
term        ::= factor {("*" | "/") factor}
factor      ::= "(" expression ")" | operand
operand     ::= variable | number
variable    ::= "x" | "y"  // extend this to include other variable names if needed
number      ::= digit {digit}
digit       ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

  - `expression` consists of `term` optionally followed by a
     sequence of `term`s separated by `+` or `-`.
  - `term` consists of `factor` optionally followed by a
    sequence of `factor`s separated by `*` or `/`.
  - `factor` can be an `expression` enclosed in parentheses
    or an `operand`.
  - `operand` can be either a variable or a number.
  - `variable` is restricted to `x` and `y` for simplicity
    (can be extended with more variables).
  - `number` consists of one or more digits.

This corresponds to what the parsing in 'arith.py'
do to arithmetical expressions,
e.g. '3 + 2 * (x - 4) / y'.


### prefix

Prefix notation (Polish notation) is where operators
precede their operands. The EBNF for the given prefix
notation would look like this:

```ebnf
expression  ::= "(" operator expression expression ")" | operand
operator    ::= "+" | "-" | "*" | "/"
operand     ::= variable | number
variable    ::= "x" | "y"  // extend this to include other variable names if needed
number      ::= digit {digit}
digit       ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

  - `expression` can be either an operator followed by two
     expressions enclosed in parentheses, or it can  be an operand.
  - `operator` includes the basic arithmetic operators:
    `+`, `-`, `*`, and `/`.
  - `operand` can be either a variable or a number.
  - `variable` is restricted to `x` and `y` for simplicity
     (can be extended with more variables).
  - `number` consists of one or more digits.

A sample of this could be '+ 3 / * 2 - x 4 y' which
corresponds to the above infix '3 + 2 * (x - 4) / y'.

This is how to do this infix to prefix conversion manually:
1. First convert x - 4 to prefix: - x 4
2. Substitute - x 4 back into the expression: 2 * (- x 4)
3. Convert to prefix: * 2 (- x 4), swap operator and first operand
4. Substitute * 2 (- x 4) back into the expression: (* 2 (- x 4)) / y,
   add parentheses
5. Convert to prefix: / (* 2 (- x 4)) y, swap
6. Substitute / (* 2 (- x 4)) y back into the expression: 3 + (/ (* 2 (- x 4)) y)
7. Convert to prefix: + 3 (/ (* 2 (- x 4)) y)


## run

Now, test the following program 'arith2.py':

```shell
> python3 arith2.py
```

A result from running should be:

```shell
Parsed result: ([[], '+'], [[], 3, [' ']], ([[], '/'], ([[], ..
Reconstructed expression: (3+((2*(x-4))/y))
Evaluated result: 4.0   with x = 5 and y = 2
```

Besides the cryptic first parsed result, a reconstructed expression from this
result is shown below, and also the expression is evaluated, with application
of x as 5 and y as 2.

What is happening in 'arith2.py' is that the parsing results in a structure
which represents the arithmetic expression in a prefix fashion. Through
some conversions, we end up back with the original infix. (We can do better,
carefully considering the operators precendence, we can eliminate some of
the parentheses.)


## traditional vs. combinator parsers

Traditional parsers, such as the hand crafted recursive descent parsers which
we already are familiar with, have a simple and straightforward way to parse
using very explicit functions or methods, recursively calling input reflecting
the grammar. 

It have often used the imperative approach in explicit control flow. Typically
a function corresponds to a non-terminal from the grammar. These parsers uses
helpers in form of tokenizers or scanners, to pick token by token from input.
A (token) look-ahead read can see what comes next, for easier parsing.

Errors in parsing can be a bit difficult to handle, when the parser is suppose
to report *several* consecutive problems in a parsed program. Example of a
parser that automates parsing through traditional means is ANTLR[^antlr].

[^antlr]: https://en.wikipedia.org/wiki/ANTLR, and https://www.antlr.org/


Combinator parsers are, in contrast, a type of parser built using higher-order
functions, known as *combinators*, that combine simpler parsers to build more
complex parsers. The combinator parsers have a very natural connection to
mathematics: [Combinator Parsers](combpar.pdf).

The combinator parsers has a functional approach and works very well with
functional programming languages (e.g. Haskell), or a functional style.
They use functions to define how different parts of the language are
parsed, combining these functions to handle more complex structures.
They promote code reuse and modularity. You can build small,
simple parsers and then combine them to create more complex parsers.
This modularity makes it easy to understand, extend, change, and maintain
the parser.

The composability implies that in various ways you create new parsers.
For example, you can sequence parsers to match patterns in a specific order
or choose between parsers to handle alternatives. Combinator parsers can
handle backtracking naturally, trying multiple parsing strategies and choosing
the one that works, that applies. Example of a parser of this type is
Parsec[^parsec] originally in Haskell, but also 'ported' to other languages.

[^parsec]: https://wiki.haskell.org/Parsec,
or in general: https://en.wikipedia.org/wiki/Parsec_(parser)

