# Virtual Machines

## Interpreter technique

Close to "virtual machines" there is in principal a "interpreter technique".
The main point of the technique can be described as:[^5]

[^5]: In main translated excerpt from the Swedish journal *Modern elektronik*, no. 8, 1981.
Ideas and facts by Hans Beckman, Johan Finnved, ed. Gunnar Christernin. In this exact part
they mention examples of floating point calculation, and compilers should be able to use
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

![Principles of an interpreter technique](../assets/images/interpreter.png)


## Metcalfe machine

call <label>
: (possibly recursive)

false <label>
: conditional jump, if flag false then jump to label

flag false
: set flag to false

flag true
: set flag to true

match <item>
: compare one item with the (non visible) input. if match the set flag true, else set to false

print <item>
: print current item to output

return
: return from call (pop from stack address and set the pc)

stop
: stop the machine

then <item>
:compare the next item (after match) on input. make a logical and with current flag, i.e. if previous set of flag is true and the current, then they both are true, otherwise set flag false

true <label>
: conditional jump, if flag is true



