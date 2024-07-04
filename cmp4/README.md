# Virtual Machines

A compiler, assembler and a virtual machine working to get out
the result from an expression written in plain text, like '(98 - 6767 + 7987)'.

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

Test the sample with:

```shell
> make clean
> make cmp4
```


## syntax of expressions

```ebnf
expression	= term { (+|-) term }

term		= factor { (*|/) factor }

factor		= ident | number | ( expression )
```

*expression*
* An expression consists of a term followed by zero or more
  instances of a term prefixed by either a `+` or `-` operator.
* In simpler terms, an expression can be a single term or
  multiple terms added or subtracted together.

*term*
* A term consists of a factor followed by zero or more
  instances of a factor prefixed by either a `*` or `/` operator.
* In simpler terms, a term can be a single factor or
  multiple factors multiplied or divided together.

*factor*
A factor can be one of the following:
* `number`: A numeric value.
* `( expression )`: A complete expression enclosed in
  parentheses, allowing for nested expressions.


### graphical representations[^novars]

#### Expression:
![expression ..](https://user-images.githubusercontent.com/271797/188278982-1ff42147-4e27-490e-ad9f-1b465ed131be.svg)

#### Term:
![term](https://user-images.githubusercontent.com/271797/188279089-32abec43-650d-4acb-9d3c-37bb86bd49fe.svg)

#### Factor:
![factor](https://user-images.githubusercontent.com/271797/188279057-9cc5ec8d-0c7e-4af0-a579-10491d51caf2.svg)

[^novars]: __NOTE: we do not have any identifiers yet, so the "IDENT" in the diagram is not relevant for now.__


### sample

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
* For example, `2 * (3 + 4)` is a term.

C.) Construct *expressions*:
* Combine *terms* using `+` or `-`.
* For instance, `2 * (3 + 4) / 5` can be part of a larger *expression*.
