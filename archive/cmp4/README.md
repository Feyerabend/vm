# Virtual Machines

A compiler, assembler and a virtual machine working to get out
the result (2) from an expression written in plain text, like
'2 * (3 + 4) / 5'.


## cmp4

In the compiler `cmp4.c` (and `cmp4.h`) you can find steps to a
small calculator that take as input expressions with multiplication,
addition etc. and delivers an 'assembly code' as 'MUL' and 'ADD'
etc. preparing for the stack oriented vitual machine. The compiler
uses a scanner `scan.c` (`scan.h`) to recognize what is an operator
like '*' or '+', and what is a number (integer) like '982' (also
called a 'tokenizer'). It will take as input 'sample.p' (program)
and output 'sample.a' (assembly).

After compiling expressions to assembly, an assembler `asm.py` (in
Python) puts together relevant virtual machine code to an output
as 'sample.b' ('binary', or really a string of 'integers').

At last the virtual machine `vm4.c` (and `vm4.h`) can run the code
with `runvmc.c`, and the desired output will print.


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
1. compile program ('sample.p'): `./cmp4 sample.p`
2. assemble output from compilation ('sample.a') to code ('sample.b'): `python3 ./asm.py -v -i sample.a -o sample.b`
3. run the code ('sample.b'): `./runvm sample.b`


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


### parsing steps (production rules)

We can also look at parsing from the other way, intead of breaking
down expression to pieces of fators, they can be built from the
factors, up:

A. Identify *factors*:
    * Atomic units like *numbers* (`3`, `5`, `2`, `4`).
    * Parenthesized *expressions* like `(2 * 3)` or `(3 + 4)`.

B. Build *terms*:
    * Combine *factors* using `*` or `/`.
    * For example, `2 * (3 + 4)` is a *term*.

C. Construct *expressions*:
    * Combine *terms* using `+` or `-`.
    * For instance, `2 * (3 + 4) / 5` can be part of a larger *expression*.


## 1. compiling the parsed expressions

In the parsing process of `cmp4.c`, `cmp4.h`, `scan.c` and `scan.h` a tree of nodes
are built. Recognizing a number (a factor), implies a node representing that number
as a value (by the function `atoi` in C). If there is a expression of say '2 + 4'
then a new node connects whatever is on the left ('2' as a node) to whatever is on
the right ('4' as a node) in a node which is qualified by a "type" 'ADD'. This
ultimate (recursive) tree of nodes, are then used in generating the assembled
variant of the program.[^onepass]

To get into some details, first we have something like:

```c
node* n = program();
compile(n);
```

From `program()` we get nodes in n. Then we transfer them to `compile(n)`.
Looking at the program, we go down into the details.

```c
node *n = nnode(PROG);
nextsym();
n->node1 = expression();
expect(PERIOD);
```

So we start with a root node made of type `PROG` and an expected end with `PERIOD`.
We analyze the from the top an assumption of an expression.

Then we check for the inner workings of the expression. We assume that we can find
types `PLUS` or `MINUS`. If we find those, we can att them to the tree of nodes.

```c
node *m, *n;
n = term();
while (sym == PLUS || sym == MINUS) {
  m = n;
  if (sym == PLUS)
    h = ADD;
  else if (sym == MINUS)
    h = SUB;
  else {
    ..
  }
  n = nnode(h);
  nextsym();
  n->node1 = m;
  n->node2 = term();
}
```

After building a tree of nodes (also called AST, abstract syxtax tree) we
construct a assembly version of the program. The latter converter takes the
nodes, bit by bit, and transform them. Then it writes that result to a file.

From the built tree, we choose which transformation to apply in each case.

```c
case ADD:
  compile(n->node1);
  compile(n->node2);
  fprintf(file, "\tADD\n");
  break;
case MULTIPLY:
  compile(n->node1);
  compile(n->node2);
  fprintf(file, "\tMUL\n");
  break;
case INUMBER:
  fprintf(file, "\tSET %d\n", n->value);
  break;
```

As a result we get somthing like what we find in 'sample.a' from
the compiler.

```assembly
  SET 2
  SET 3
  SET 4
  ADD
  MUL
  SET 5
  DIV
  PRINT
  HALT
```

[^onepass]: Not to get the program to long, the parsed tree (also called AST),
is *not* explicitly stored as a file, although this could be more clear.
Then a second pass could take that file to build the assembly. It is left as
an exercise to work that two part compiler out.


## 2. from the assembled program to the program as code

From the above assembly program we translate this into our virtual machine
code through a simple assembler `asm.py`.

```text
5,2,5,3,5,4,0,3,5,5,1,4,2
```

## 3. running the code

At last we can run the program with in principal the same virtual machine
we have gone through before with `vm.c`, `vm.h` and `runvmc.c`.

## check

In the world of programming, a compiler does more than just translate code from
a high-level language into machine code. It also plays a crucial role in assisting
programmers by ensuring their code is syntactically correct before the actual
compilation process begins. Syntax checking is a key step in this process, as
it helps identify and correct errors early, saving time and effort later on.

The syntax checking phase can involve substantial code and logic to thoroughly
validate the input code. In this context, we’re providing a simplified approach
to syntax checking, focusing on practical suggestions for how to verify your
code. For a more detailed and effective syntax validation, use the `check.py`
script. Running `check.py` will help you identify and address syntax issues
*before* you proceed with compiling your code.

By incorporating syntax checking into your workflow, you ensure that your code
is not only correctly written but also well-prepared for the next stages of
compilation. Running syntax checks before compiling allows you to catch and
correct potential errors early in the development process.

```shell
> python3 ./check.py -i sample.p
```
