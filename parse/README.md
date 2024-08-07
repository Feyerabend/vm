# Virtual Machines

## run

```shell
> python3 arith.py
```



```shell
> python3 arith2.py
```



## enbf

We are already acquainted with some formalizations of
language syntax in "Backus-Naur Form" (BNF) or
"Extended Backus-Naur Form" (EBNF). Both are used as
notations to express context-free grammars. Below are
the EBNF notations for both the *prefix expression* and
the *infix expression* as described in the examples.


### prefix

Prefix notation (Polish notation) is where operators precede their
operands. The EBNF for the given prefix notation would look like this:

```ebnf
expression  ::= "(" operator expression expression ")" | operand
operator    ::= "+" | "-" | "*" | "/"
operand     ::= variable | number
variable    ::= "x" | "y"  // extend this to include other variable names if needed
number      ::= digit {digit}
digit       ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

### infix

Infix notation is the more conventional form where operators are
placed between operands. The EBNF for infix notation that corresponds
to the previous prefix examples would look like this:

```ebnf
expression  ::= term {("+" | "-") term}
term        ::= factor {("*" | "/") factor}
factor      ::= "(" expression ")" | operand
operand     ::= variable | number
variable    ::= "x" | "y"  // extend this to include other variable names if needed
number      ::= digit {digit}
digit       ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

### description

- *Prefix EBNF*:
  - `expression` can be either an operator followed by two expressions enclosed in parentheses, or it can be an operand.
  - `operator` includes the basic arithmetic operators: `+`, `-`, `*`, and `/`.
  - `operand` can be either a variable or a number.
  - `variable` is restricted to `x` and `y` for simplicity, but this can be extended.
  - `number` consists of one or more digits.

- *Infix EBNF*:
  - `expression` consists of `term` optionally followed by a sequence of `term`s separated by `+` or `-`.
  - `term` consists of `factor` optionally followed by a sequence of `factor`s separated by `*` or `/`.
  - `factor` can be an `expression` enclosed in parentheses or an `operand`.
  - `operand` can be either a variable or a number.
  - `variable` is restricted to `x` and `y` for simplicity, but this can be extended.
  - `number` consists of one or more digits.

These EBNF rules define the syntax of the prefix and infix expressions
as used in the examples, ensuring the correct structure and order of operations.


## combinator parsers

..
