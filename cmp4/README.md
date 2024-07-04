# Virtual Machines

A compiler, assembler and a virtual machine working to get out
the result (2) from an expression written in plain text, like
'2 * (3 + 4) / 5'.

## cmp4

In the compiler `cmp4.c` (and `cmp4.h`) you can find steps to a small
calculator that take as input expressions with multiplication, addition
etc. and delivers an 'assembly code' as 'MUL' and 'ADD' etc. preparing
for the stack oriented vitual machine. The compiler uses a scanner
`scan.c` (`scan.h`) to recognize what is an operator like '*' or '+',
and what is a number (integer) like '982' (also called a 'toknizer').
It will take as input 'sample.p' (program) and output 'sample.a' (assembly).

After compiling expressions to assembly, an assembler `asm.py` puts together
relevant virtual machine code to an output as 'sample.b' (binary).

At last the virtual machine `vm4.c` (and `vm4.h`) can run the code with
`runvmc.c`, and the desired output will print.

## run

Compile the compiler:

```shell
> make clean
> make cmp4
```

Then test the sample by running or follow the steps in `compile.sh`:

```shell
#!/bin/sh
rm -f sample.a
rm -f sample.b
./cmp4 sample.p
python3 ./asm.py -v -i sample.a -o sample.b
./runvm sample.b
```

This will first remove any previous compiled pieces from 'sample.p',
compile it, and assemble the output 'sample.a' from compilation to
a 'sample.b'. And then run the 'sample.b' in the virtual machine.

There are thus 3 steps:
1. compile program (sample.p)
2. assemble output from compilation (sample.a) to code (sample.b)
3. run the code (sample.b)


## syntax of expressions, enbf

How then do we go about parsing a simple arithmetical expression?
We will first describe the parsing through a notation.
The formulation of the syntax (the text of in this case: expressions)
parsed by the program, will be worked through what is called the
Extended Backus-Naur Form (EBNF) below. ENBF is a notation used
to formally describe the syntax of languages, particularly
programming languages and data formats.
(It extends the basic BNF syntax to provide more expressive and
concise grammar definitions.)

Key Components of *EBNF*:

1. Rules/Productions:
   - EBNF grammars are made up of rules (also called productions).
   Each rule defines how a particular syntax element can be constructed.
   - The left side of a rule is the name of the element being defined.
   The right side specifies how this element can be composed using other
   elements.

2. Terminals and Non-terminals:
  - Terminals: The basic symbols from which strings are formed.
  These are usually the actual characters or tokens of the language
  (like numbers, operators, keywords).
  - Non-terminals: Abstract symbols representing a set of strings.
  They are defined by other rules in the grammar.

3. Operators and Constructs:
  - Concatenation: A sequence of elements written one after the other,
  implying they occur in that order.
  - Alternation `|`: Indicates a choice between alternatives.
  For example, `A | B` means either `A` or `B`.
  - Repetition `{ }`: Indicates zero or more repetitions of an element.
  For example, `{ A }` means zero or more instances of `A`.
  - Optional `[ ]`: Indicates that an element may or may not be present.
  For example, `[ A ]` means `A` is optional.
  - Grouping `( )`: Groups elements together to control the application
  of operators. For example, `(A | B) C` means either `A` or `B`,
  followed by `C`.

In this case we can express the parsing as follows:

```ebnf
expression	= term { (+|-) term }
term		= factor { (*|/) factor }
factor		= number | ( expression )
```

*expression*
 * An expression consists of a *term* followed by zero or more
   instances of a term prefixed by either a `+` or `-` operator.
 * In simpler terms, an expression can be a single term or
   multiple terms added or subtracted together.

*term*
 * A term consists of a *factor* followed by zero or more
   instances of a factor prefixed by either a `*` or `/` operator.
 * In simpler terms, a term can be a single factor or
   multiple factors multiplied or divided together.

*factor*
a factor can be one of the following:
 * `number`: A numeric value.
 * `( expression )`: A complete expression enclosed in
   parentheses, allowing for nested expressions.


### sample

How does this work in practice?

```text
2 * (3 + 4) / 5
```
1. `2` is a *factor*.
2. `(3 + 4)` is an expression enclosed in parentheses, acting as a *factor*.
3. `5` is a *factor*.
4. This entire structure is a *term* due to the `*` and `/` operators between the factors.


### parsing steps

A.) Identify *factors*:
 * Atomic units like *numbers* (`3`, `5`, `2`, `4`).
 * Parenthesized *expressions* like `(2 * 3)` or `(3 + 4)`.

B.) Build *terms*:
 * Combine *factors* using `*` or `/`.
 * For example, `2 * (3 + 4)` is a *term*.

C.) Construct *expressions*:
 * Combine *terms* using `+` or `-`.
 * For instance, `2 * (3 + 4) / 5` can be part of a larger *expression*.


## compiling the parsed expressions



## from assembly to code

## running code

