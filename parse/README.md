# Virtual Machines

*Combinator parsers*[^combpar] are a way to parse e.g. programming languages.
It could be argued that traditional recursive decent parsers are close to
combinator parsers, and that would not be wrong. But there are some differences,
such as the latter have very tight relationship with mathematics, and with
functional languages. Traditional parsers rather have a more imperative and
closer relationship to the (von Neumann) machine.

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
*text*, but also the *position* where the match
was made, if successful. Otherwise no text, but
only the position.

In a way this reflects how grammars work with
choises, as we have seen before with '|'. The 'defs'
works as or corresponds to the definitions in the grammar.

### base

Usually combinator parsers come with a group of parsers that
can be the orgin for, or the base of, other more specialized
parsers. They are 'sequence', 'choice', 'many' and 'many1'.

```python
def sequence(*parsers):
    def parser(text, pos):
       ..
def choice(*parsers):
    def parser(text, pos):
       ..
def many(parser):
    def parse(text, pos):
       ..
def many1(parser):
    def parse(text, pos):
       ..
```

These fundamental parsers reminds us of how grammars
can be described. Take an aritmetical expression in
the "Extended Backus-Naur Form" (EBNF):

```ebnf
expression  ::= term {("+" | "-") term}
```

The definition of 'expression' is a *sequence* of
'term' but also followed by an *optional* sequence
of a *choice* of either '+' or '-' and then a 'term'.

A short summary of what the base parsers do:
- `sequence`:
Takes multiple parsers and applies
them in sequence to the input text. It returns the
combined result of all parsers if they all succeed,
along with the position in the text after the last
parser has been applied.
- `choice`:
Tries multiple parsers in order,
returning the result of the first parser that
succeeds. If none of the parsers succeed, it
returns a failure.
- `many`:
Applies a single parser repeatedly,
as many times as possible (including *zero times*).
It collects all the successful results into a
list and returns it along with the final position
in the text.
- `many1`:
Similar to many, but ensures that the parser is
applied at least once. It collects and returns
a list of results from each successful application
of the parser, along with the updated position
in the input text.

### a sample: factor

If look at the main custom parser functions, we
can see quite clearly how they relate to the 
grammar. Take the example of 'factor':

```python
def factor():
    return sequence(
        whitespace(),
        choice(between(char('('), char(')'), expression()),
               variable,
               constant),
               whitespace())
```

This function reminds of:

```ebnf
factor      ::= "(" expression ")" | operand
operand     ::= variable | number
```

We start off with a sequence, and
in case there are some whitespace then consume them, move
to a *choice*. Then either an expression that sits in between
parenthesis, or a variable or a constant, are assumed as
input. In this case the function has not been split up in
two functions, but as can be seen the 'operand' is included
in arguments to the choice function.


## ebnf

We are already acquainted with some formalizations of
language syntax in "Backus-Naur Form" (BNF) or
"Extended Backus-Naur Form" (EBNF) (or rather some
homebrew versions of them). Both forms are used as
notations to express context-free grammars. Below
are the EBNF notations for both the *prefix* and the
*infix expression*.


### infix

Infix notation is the more conventional form where
operators are placed between operands.

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

Let us take a look at another grammar that places the operators
and the operands in a different place: a prefix notation. We
are already familiar with the reverse Polish order or
postfix order from working with numbers and operators in a stack. 
A prefix notation or a Polish notation[^polish] is where operators
precede their operands.

[^polish]: For those who have studied formal logic and its history,
the Polish logican Jan Łukasiewicz should be familiar and
probably associated with this notation. See more at:
https://en.wikipedia.org/wiki/Polish_notation, and
https://en.wikipedia.org/wiki/Jan_%C5%81ukasiewicz.

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

An example of this could be '+ 3 / * 2 - x 4 y' which
corresponds to the above infix '3 + 2 * (x - 4) / y'.
As can be seen parenthesis is no longer needed in the
prefix version (as with postfix), and can therefore
be elimiated. The precendence of operators become implicit.

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
some conversions, we end up back with the original infix.[^note]

[^note]: We can do better,
carefully considering the operators precendence, we can eliminate some of
the parentheses in this sample.

### traditional parsing

When converting from the output of the combinator parsers, we use 
an ordinary way (among others) of converting from prefix to infix:

```python
# parse from prefix to infix
def prefix_infix(expr):
    stack = []
    i = len(expr) - 1
    while i >= 0:
        s = expr[i]
        if not s in ['+', '-', '*', '/', '(', ')']:
            stack.append(s)
        else:
            stack.append('(' + stack.pop() + s + stack.pop() + ')')
        i -= 1
    return stack.pop()
```

This uncomplicated parsing takes an item at a time from 'expr',
appending to the output 'stack' of operators and operands. There
is no need for overcomplicated maneuvers.


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

