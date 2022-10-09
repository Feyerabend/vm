# Virtual Machines

*Some explorations in syntax analysis*. As an example of
how to parse text, here we use an implementation of a
"machine" picking out characters (or tokens) from an input
"tape", matching expected characters and acting
accordingly (as a program). There is also an output "tape"
where we can store results.

Production rules are an old concept used in such theories
on parsing (other uses are e.g. expert systems). A simple
block of production rules are:

```
  S → A B
  A → a | ac
  B → b | cb
```

From this we can generate a limited set of products.

```
S → AB → aB → ab
S → AB → aB → acb
S → AB → acB → acb
S → AB → acB → accb
```
You can probably easily follow the substitutions for each
step where finite terms in lower case replace the upper
case placeholders.


## *Metcalfe machine*[^2]

In short here are the instructions the machine can use:

__call &lt;label&gt;__
: Push current position of input and output on a stack.
Call some subprogram/-routine at label (possibly recursive calls).

__false &lt;label&gt;__
: Conditional jump, if `flag` *false* then jump to label.

__flag *false*__
: Set `flag` to *false*.

__flag *true*__
: Set `flag` to *true*.

__match &lt;item&gt;__
: Compare one item with the input. Move input pointer forward.
If match the set `flag` *true*, else set `flag` to *false*.

__print &lt;item&gt;__
: Print current item to output.

__return__
: Return from call (pop from stack address and set the program counter).
Also pop positions of input and output pointers from a separate stack.

__stop__
: Stop the machine, print all of output.

__true &lt;label&gt;__
: Conditional jump, if `flag` is *true*.


I've given an attempt at creating a machine from the above description in
`met.py` and `calfe.py`. The former `met.py` translate a program in the
language above to a corresponding binary. The the latter `calfe.py` interpret
the program and applies a given formula as an array.

### run

A sample 'etf.mc' (simple text) which is an abbreviation for
'expression, term, factor' is a program for converting infix
expressions to prefix expressions. One such expression could be
e.g. '(45+89)' which translates into '+ 45 89'. If we allow for
a simple abstraction, we can put 'i' as placeholder for numbers
or variables. This machine can thus be used for simple parsing.

First compile or assemble the program 'etf.mc' (source code) into
'etf.b' (binary). Then run the binary with a sample file 'etf.test'
such as `(,i,+,i,)`. This is then parsed into a list
`['(', 'i', '+', 'i', ')']` for easier handling of cases where
matching is done with concatenated characters into their own
tokens, e.g. 'ab'.

```shell
> python3 met.py -v -i etf.mc -o etf.b
> python3 calfe.py -v -t etf.test -i etf.b -o etf.out
```

The result should be `+ i i`.

In the test file 'etf.test' there is a line at the end which reads:
`(,i,+,i,)`. Change that expression to reflect *your* tests
(or e.g. `(,(,i,+,i,),*,i,+,(,i,*,i,*,i,),)`).



[^2]:Howard H. Metcalfe, "A Parametrized Compiler based on Machanical Linguistics",
*Annual Review in Automatic Programming: International Tracts in Computer Science
and Technology and Their Application*, Vol. 4, ed. Richard Goodman, The Macmillan
Company, New York, 1964. Reprinted Pergamon Press, 2014.
