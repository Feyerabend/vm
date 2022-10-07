# Virtual Machines

## Interpreter technique

Close to "virtual machines" there is in principal an "interpreter technique".
The main point of the technique can be described as:[^1]

[^1]: In main translated excerpt from the Swedish journal *Modern elektronik*, no. 8, 1981.
Ideas and facts by Hans Beckman, Johan Finnved, ed. Gunnar Christernin. In this exact part
they mention examples of floating point calculation, and that compilers should be able to use
this technique.

1. the interpreter is called, with a list of instructions as argument
2. the interpreter takes an instruction from the incoming list,
3. do a look up in the internal list of instructions (types),
4. then the interpreter ”interprets” the instruction of what to do,
5. which points to an address list, and thus a corresponding handler for each (type of) instruction,
6. the handler is called, do something,
7. after handling, the call returns from the handler, and
8. the interpreter goes on to the next instruction, start over from 1 to 8 as long as there are instructions left
9. when all the instructions have been consumed, the interpreter returns to the main caller

![Principles of "interpreter technique"](../assets/images/interpreter.png)


## Metcalfe machine[^2]

__call &lt;label&gt;__
: Push current position of input and output on stack.
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
Also pop positions of input and output pointers from stack.

__stop__
: Stop the machine, print all of output.

__true &lt;label&gt;__
: Conditional jump, if `flag` is *true*.


I've given an attempt at creating a machine from the above description in `met.py` and
`calfe.py`. The former `met.py` translate a program in the language above to a corresponding
binary. The the latter `calfe.py` interpret the program and applies a given formula as a
string. It can be altered to a more productive program by changing the characters to be
recognized into tokens instead (using arrays e.g.).

```shell
> python3 met.py -v -i etf.mc -o etf.b
> python3 calfe.py
```


[^2]:Howard H. Metcalfe, "A Parametrized Compiler based on Machanical Linguistics",
*Annual Review in Automatic Programming: International Tracts in Computer Science
and Technology and Their Application*, Vol. 4, ed. Richard Goodman, The Macmillan
Company, New York, 1964. Reprinted Pergamon Press, 2014.

