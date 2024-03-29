# Virtual machines

*A fragment of a compiler.*[^1] Starts with an abstract tree and gives an assembled program.

[^1]: A short history of compilers give some ideas on what they are orhave been:
https://www.wikiwand.com/en/History_of_compiler_construction

## cmp1

To make the previous virtual machines more practical, we could add a compiler for some
high-level language. But we will take the unusual step here to begin from the machine,
and work our way upwards, towards the language[^2]. There is a rather long history of
syntactical analysis and compiler constructions that at least starts with Noam Chomsky
and his attempts at formalizing and recognizing structures in (natural) languages.[^3]
Then individuals such as Peter Naur, John Backus, Niklaus Wirth and many, many, many
others in the 60'ties and 70'ties advanced the techniques for compiler
constructions, syntactical analysis and other closeby research.

[^2]: For the suggestion of the "incremental" approach to constructing compilers,
see http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf (which I discoved after *doing* it).
[^3]: One such interesting book from the late 50'ties is Chomsky, Noam,
*Syntactic structures*, Mouton, The Hague, 1957.

In the file `cmp1.c` you will find a sort of introduction to how we could look at a
semantic contruction or abstraction in the form of a tree. Some nodes are representation
of constants, or numbers, if you prefer. One other node represent addition and another
multiplication. These nodes are nested together to represent a "semantic" view of the
arithmetical sample: "(32 + 53) * 90". In this way we could build trees that represent
more artithmetical expressions, or control structures, assignments of variables,
procedures, etc. That is, we could represent *programs* in this way (cf. abstract
syntax tree, AST[^4]).

[^4]: See https://en.wikipedia.org/wiki/Abstract_syntax_tree

From the tree we can compile it to the representation in assembly that can eventually
be used by the virtual machine.

### build or construct

```c
typedef struct node {
    int type;
    int value;
    struct node *node1, *node2;
} node;
```

A node consists of a type which is CONSTANT, ADD or MULTIPLY. To the node we can also
add an integer value. Only the CONSTANT type in our case has an integer value (and then
*interpreted* as an integer value). A node can point to other nodes. Thus, a "tree" of
nodes can be built.

```text
 q MULTIPLY
 ├── p CONSTANT 90
 └─┬ x ADD
   ├── y CONSTANT 32
   └── z CONSTANT 53
```

### deconstruct or analyze

Then when we compile we break down the elements to translate them into our vm-instructions.
For example the ADD instruction takes both its child nodes (recursively) for futher break down:

```c
 void compile(node *n) {
    switch (n->type) {

    	...

        case ADD:
            compile(n->node1);
            compile(n->node2);
            printf("ADD\n"); 
            break;

```

## run

Test the sample with:

```shell
> make clean
> make cmp1
```

Then, if everything worked, no errors were produced, then run it by:

```shell
> ./cmp1
```

The result should be in print:

```assembly
SET 32
SET 53
ADD
SET 90
MUL
```

