# Virtual Machines

## run

Try running a script 'arith.py':

```shell
> python3 arith.py
```

It will parse the arithmetical expression '3 + 2 * (x - 4) / y' and
the result will be:

```shell
Parsed result: ..
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
parser, e.g. recursive decent parser, we have seen before.

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
works as definitions in the grammar.


## enbf

We are already acquainted with some formalizations of
language syntax in "Backus-Naur Form" (BNF) or
"Extended Backus-Naur Form" (EBNF) or some versions
of them. Both forms are used as notations to express
context-free grammars. Below are the EBNF notations
for both the *prefix expression* and the
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

- *Infix EBNF*:
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

- *Prefix EBNF*:
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
Parsed result: ..
Reconstructed expression: 3+2*(x-4)/y
Evaluated result: 4.0  with x = 5 and y = 2"
```

Besides the cryptic first parsed result, a reconstructed expression from this
result is shown below, and also the expression is evaluated, with application
of `x` as 5 and `y` as 2.

What is happening in 'arith2.py' is that the parsing results in a structure
which represents the arithmetic expression in a prefix fashion. Through
some conversions, we end up back with the original infix.


## combinator parsers


..
