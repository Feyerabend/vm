# Virtual Machines

Debugging has been an integral part of computing since
the early days of programming. In many ways, programming
remains a *craft*, and debugging is a critical aspect of
that craft.
Early debugging tools were fundamental yet highly effective.
Techniques such as logging[^log], single-stepping through code,
and setting breakpoints to halt execution for detailed
inspection were very useful. These methods allowed developers
to meticulously trace and resolve issues.
In this exploration, we’ll revisit these simple but powerful
debugging tools and see how they are still relevant when
working with virtual machines, or really in any programming
environment.

[^log]: A more in depth discussion of the usefulness is done
in [ED.md](debug/ED.md).


## assembling & disassembling

Taking an assembler from previous, we can turn it into something which
analyses our "machine code," a disassembler. It reverses the process,
takes the integers and turn them into easier to understandable mnemonics,
the "assembly language."

The assembler works as previously:

```shell
> python3 asm.py -i sample.a -o sample.b
> python3 asm.py -i callret.a -o callret.b
> python3 asm.py -i fact.a -o callret.b
> ls
..
callret.a   fact.a      sample.a
callret.b   fact.b      sample.b
..
```

### disassembler

If we take the following 'binary' in 'sample.b':

```code
38,13,0,28,0,12,0,27,1,5,11,16,27,1,30,
0,24,12,0,27,1,31,28,3,12,3,29,0,2,0,12,
0,14,0,18,30,0,24,24,27,10,29,0,2,0,14,
0,22,8
```

we can convert it into what it previously was
assembled from:

```shell
> python3 disasm.py -i sample.b -o sample.d
> cat sample.d
L0:
	LDARG 0     # 013 000
	ST 0        # 028 000
	LD 0        # 012 000
	SET 1       # 027 001
	EQ          # 005
	JPZ :L16    # 011 016
	SET 1       # 027 001
	STORE 0     # 030 000
	RET         # 024
L16:
	LD 0        # 012 000
	SET 1       # 027 001
	SUB         # 031
	ST 3        # 028 003
	LD 3        # 012 003
	STARG 0     # 029 000
	CALL :L0    # 002 000
	LD 0        # 012 000
	LOAD 0      # 014 000
	MUL         # 018
	STORE 0     # 030 000
	RET         # 024
	RET         # 024
START:
	SET 10      # 027 010
	STARG 0     # 029 000
	CALL :L0    # 002 000
	LOAD 0      # 014 000
	PRINT       # 022
	HALT        # 008
```

Disassemblers can be useful, when e.g. the source isn't available
or when you want to inspect the machine and the program in this
context.


## debug vm

### tracing

Tracing involves inserting print statements or logging calls
into the code to output the program's state and the values of
variables or in this case mostly the stack at various points
during execution. This helps to follow the program's flow and
understand where things might be going wrong.

### single step

Single-stepping allows the programmer to execute the program
one line or instruction at a time. This lets you closely examine
the program's behavior at each step and observe how the stack
(or in case: variables) and the system state change with each
executed line of code.

### breakpoints

Breakpoints are markers set in the code where the execution
will pause, allowing the developer to inspect the program state
at specific points. This is useful for examining the conditions
leading up to a particular point in the code, especially where
issues are suspected to occur.


### simple debugging workflow

1. __setting breakpoints__: set breakpoints at critical sections or
   where one suspect a bug might be,
2. __run to breakpoint__: the program runs normally until it hits a
   breakpoint,
3. __inspect__: once paused, inspect stack, variables, other memory,
   to understand the program's condition at that moment,
4. __single step__: after inspection, single-step through subsequent
   lines to observe changes and further diagnose issues.
   or just let the program *continue*,
5. __trace__: supplementary to breakpoints and stepping, trace logs
   provide a broader picture of program flow, stack and variable 
   states throughout the execution.

### dvm

A simple implementation of some debugging tools inside a previously
seen vm, let you choose for 'singlestep', setting 'breakpoints' and an
optional 'trace'.

```shell
> python3 dvm.py --singlestep true --breakpoints 14,16 --trace true --input sample.b
```

![Debug VM](../assets/images/dvm.png)

Inside the vm, there are features that allow you to single-step
through the code if selected at the start. When single-stepping
is no longer needed, the 'continue' command can execute the code
without pausing at each step.

A trace can display various elements, such as the current stack,
the program counter, the executing operator and operand, and
other options like arrays, arguments, and variables. The trace
can be turned off, and the options can be selected dynamically.
For example, choosing "pos" would show the *program counter*,
*operation/operand*, and the *stack*, while "pv" would show the
*program counter* and *variables*. In this case the trace isn't
a log in a file, but only displayed on the screen.

Breakpoints will halt the program and wait for further instructions.

![Debug VM](../assets/images/dvm2.png)

Test with included samples such as 'fact.a' and 'callret.a'
where they are easy to follow, and see what happends when
they are executed through the debugger.

The `dvm.py` file is essentially the previous `vm.py` and
contains the implementation of the virtual machine.
It defines the operations supported by the VM,
such as arithmetic operations, logical operations, control
flow operations, and more. Each operation is represented by
an opcode, and the VM processes a sequence of these opcodes
to perform computations.


## test dvm

While debugging the programs that the VM executes is
crucial, ensuring the VM itself functions correctly
is equally important. Developing a suite of test programs
not only helps in specifying the machine's behavior
but also aids in validating its consistency when the
VM is ported to other platforms.

A test suite serves as both a specification and documentation
for the VM, outlining its expected behavior and providing
clear examples of its operation. It aids in debugging by
quickly identifying bugs and regressions, ensuring that new
changes or optimizations do not disrupt existing functionality.
Additionally, when porting the VM to different platforms, the
test suite helps verify that the port maintains consistency
with the original implementation, allowing for early detection
of platform-specific issues.
To execute some illustrative tests and validate the
functionality of the VM, run the `dvmtest.py` script.

```shell
> python3 dvmtest.py
```

This script leverages many components from the `dvm.py`
file to perform a series of operations and tests,
ensuring the VM works correctly across various scenarios.
*The tests are not exhaustive,
but they illustrate the principal idea.*

The `dvmtest.py` file contains a suite of tests designed
to validate the functionality of the VM. Each test focuses
on specific operations or scenarios to ensure the VM
handles them accordingly. But they are only tests, they
do not verify that the vm is always correct. For that
we would have to prove them somehow -- which will not
be done here. The tests include: arithmetics,
division by zero, logical and comparison operators,
arrays, function calls.
