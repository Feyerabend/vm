# Virtual Machines
Virtual machines samples[^1]. A collection of virtual machines to teach or understand some
ideas and inner workings of virtual machines. They are solely intended for show of principles,
and not for uses in any other way.

[^1]: My best inspiration for the simple machines here comes from Bartosz Sypytowski:
https://bartoszsypytkowski.com/simple-virtual-machine/ from whom I derived most of the code,
even though some bugs were corrected.

## vm1
### compile with gcc installed; `gcc vm1.c` at the command line, then run with `./a.out`.

*A very simple virtual machine implemented as a stack machine.
As an example: Push two numbers on the stack. Each at a time.
Then add the two numbers. Place the result back on stack. Then print sum.*

> int program[] = {
        SET, 33,
        SET, 44,
        ADD,
        PRINT,
        HALT
};

In `vm1.c` the important functions are:
- `VM* newVM(int* code, int pc)` which allocates vm, struct for the stack, code array, program counter (pc) and stack pointer (sp). 
- `void freeVM(VM* vm)` deallocates vm.
- `int pop(VM* vm)` moves the pointer (sp) at the array for the stack to pop a value, stack impl. here as a fixed array.
- `void push(VM* vm, int v)` push a value on stack.
- `int nextcode(VM* vm)` move the pointer (pc) at the array to the next code in line. Can be value or operation depending on previous code. 
- `run(VM* vm)` the "processor". Picks a code from the array, and finds out what the operation will do, and execute on it.


## vm2
### compile with gcc installed; `make` at the command line, then run `./fib`.

*A machine that takes inspiration from the programming language FORTH.
It can be seen that the language here is very close to both the stack operations
and the traditional machine/assembly language. Hence, programs can use and be optimized
in line of being "forthified" (adopted to suit FORTH thinking).*

The sample chosen to illustrate extended from the previous vm1-machine is the Fibonacci series:
1, 1, 2, 3, 5, 8, 13 ... which can be defined as a mathematical recursive function:

```
F(0) = 0
F(1) = 1
F(n) = F(n − 1) + F(n − 2), n > 1
n ∈ ℕ
```

Applied from the FORTH-thinking we have the following operations at the core:

```
TWODUP
ADD
ROT
DROP
```

First duplicate what is already on stack, the two top items `TWODUP` (or `2DUP`),
such that if we have "1 2" after would be left with "1 2 1 2".
Next add the two numbers on the stack "1 2" becomes "3", and the first two still
are there such that "1 2 3". Then rotation `ROT` would get "2 3 1", and we then `DROP` the top,
"2 3". That is, the numbers that remain will be added next time. And so on. 

## vm3
### compile with gcc installed; sample `make bin` at the command line, then run by `./bin`.

The VM has been extended with some new features, which makes it a little bit more powerful.
There are added some extra jump instructions to the vm, also comparison and a storage facility to
accommodate for iterations (vs. vm1). Moreover there is also a small framework for call/return.
You can store arguments which can be retrieved, use local variables in the function / procedure,
and return value. The "activation records", usually associated with call/return and stack machines,
are stored on the stack, with the exception for arguments used with the call (parameters).[^2] These
"records" are alternatives to the heap solution for memory allocation. The most obvious problem
with activation records (vs. heap) are that memory allocations have to be known at compile time.
Further, there are also both global variables and local variables.

[^2]: More on "activation records" can be found e.g.: https://ruslanspivak.com/lsbasi-part17/.
See also: https://en.wikipedia.org/wiki/Call_stack#Structure and https://en.wikipedia.org/wiki/Calling_convention.
One exception in the implementation of vm3 is that the parameters passed together with the procedure call
are only *transferred* to the procedure, and can not be relied upon inside the procedure. They
will be invalid in case of nested procedure calls, e.g. The parameters used should therefore only
be regarded stored as "scratch registers". The parameters should therefore be copied to local variables,
if they have any permanency inside the procedure.

Besides the VM there is also an assembler to simplify programming. It is written in *Python3* which
ease the handling of strings, and have some nice features for list processing.[^3] Using C would be
a bit longer and perhaps harder to read code.

[^3]: Here I borrowed some useful code from
https://github.com/vladris/pixie/wiki/Dust-Assembler,
and looked at some confusing code from
https://github.com/amsanei/Assembler-with-python.

Still we have no debugging support, error messaging, file handling, etc. you can find in any
corresponding system. The purpose here is to be as clear as possible to what goes on with regard
to the machine rather than other stuff. It is thus NOT for use with any other purpose than to teach
and understand som simple principles of what a VM could be.


#### Sample

To test this VM, try a program named `bin` for translating decimal numbers into binary.
First start with the assembly text in `bin.a` and convert it to the appropriate machine code:

```
> python3 ./asm.py bin.a bin.b
```

Which convert the assembly code in `bin.a` to the machine code for VM3. There is also a file named
`bin.b` which contains the machine code. Then copy the code produced either from screen (if available)
or from the generated file `bin.b`. Open the c-file `bin.c` with an editor, and paste the code (replace)
in the array named "program". Save the c-file `bin.c` with your changes. Now:

```
> make clean
> make bin
```

Then, if everything worked, no errors were produced, then run it by:

```
> ./bin
```

A binary number should appear on the screen.

The same procedure goes for the other samples `factorial`, `fibonacci` (recursive version) and `prime` (numbers).


## chip8

Next a virtual machine (or interpreter) that has been widespread and used in many computers, even
calculators. It started its life running on a processor RCA1802[^4], and systems such as COSMAC VIP
from the late 70-ties. Joseph Weisbecker which both invented the physical processor[^5] and the
application of a virtual "processor" CHIP-8, also had a daughter Joyce which is considered as the
first female video game programmer/designer.

[^4]: https://en.wikipedia.org/wiki/RCA_1802.

[^5]: Even before the Intel 4004 (around 1970/1971) Joseph Weisbecker conceived and designed the
processor FRED with only discrete logic. Intel is considered to be the first commercial company
with a processor to the market. However both RCA and Intel didn't at first understand the importance
of this idea what was to become the microprocessor. As a side note the 4004 was first used in
Busicom calculators, but the japanese software was adapted through a mechanism close to "virtual machine".

There is a much larger story here, much to unpack, but we limit the focus to the virtual machine __*CHIP-8*__.
This implementation here by Dustin Roepsch (among the many thousands there are) of Chip 8 in C, only depends
on Ncurses: https://github.com/dustinroepsch/Chip8-curses. Ncurses is a library dating back into the
80-ties, starting as a "clone" of Curses.[^6] This implies that it can be run in a *terminal window* with
very, very simplified graphics, i.e. text, and also has a nice keyboard connection to C.

This version by Roepsch has the benefit of being rather simple to understand and also few dependencies,
i.e. easy to get up and running on many environments.

[^6]: See: https://en.wikipedia.org/wiki/Curses_(programming_library) and https://en.wikipedia.org/wiki/Ncurses.

To get going, after downloading, try:

```
> mkdir build
> cd build
> cmake ../
> make
```

If all went well, you will find in the `build/bin` the compiled binary of Chip8. Start up:

```
> ./Chip8 <rom_file>
```

Where you provide your binary sample Chip-8 file. You can find some at: https://github.com/kripod/chip8-roms,
or search the web.


## cmp1

To make the previous virtual machines more practical, we could add a compiler for some high-level language. But we
will take the unusual step here to begin from the machine, and work our way upwards, to the language. There is a
rather long history of syntactical analysis and compiler constructions that at least starts with Noam Chomsky and
his attempts at formalizing and recognizing structures in (natural) languages.[^7] Then individuals such as Peter Naur,
John Backus, Niklaus Wirth and many, many, many others in the 60'ties and 70'ties advanced the techniques for compiler
constructions, syntactical analysis and other closeby research.

[^6]: One such interesting book from the late 50'ties is Chomsky, Noam, *Syntactic structures*, Mouton, The Hague, 1957.

In the file `cmp1.c` you will find a sort of introduction to how we could look at a semantic contruction or abstraction
in the form of a tree. Some nodes are representation of constants, or numbers, if you prefer. One other node represent
addition and another multiplication. These nodes are nested together to represent a "sematic" view of the arithmetical
sample: "(32 + 53) * 90". In this way we could build trees that represent more artithmetical expressions, or control
structures, assignments of variables, procedures, etc. That is, we could represent *programs* in this way (cf. abstract
syntax tree, AST).

From the tree we can compile it to the representation in assembly that can eventually be used by the virtual machine.

Test the sample with:

```
> make clean
> make cmp1
```

Then, if everything worked, no errors were produced, then run it by:

```
> ./cmp1
```

The result should be:

```
SET 32
SET 53
ADD
SET 90
MUL
```


## cmp2

We'll now make a jump from the *sematics* (abstractions) to *syntax* of programs. In this case we will chose the syntax
from the famous educational PL/0 language by Niklaus Wirth which has been around for mayn years.[^7] Maybe you will find
it very close resemblance to Pascal, which is no surprise, as Wirth also is behind Pascal, but PL/0 is much more limited:

```
var x, squ, answer;

procedure square;
begin
   squ := x * x
end;

begin
   x := 1;
   while x <= 10 do
   begin
      call square;
      answer := squ;
      x := x + 1
   end
end.
```

The above program calculates square of x, x * x or x² of a given number. Right now there is no way to print the
result, but also there is no semantics at all. So you will not be able to run the program. It is for you to inspect
the syntactical structures, and what parsing does from the side of a text representation of simple program.

There is a wikipage which also gives part implementation of the syntactical analysis for PL/0:
https://en.wikipedia.org/wiki/Recursive_descent_parser as an example of recursive decent parsing.

[^7]: https://en.wikipedia.org/wiki/PL/0

What is lacking is a scanner that checks for tokens in a stream, and gives the parser each "comprehensive" element
here added as `scan.c` and `scan.h`.

To run `sample1.pas` compile the parser (and scanner):

```
> make clean
> make par1
```

Then run the parser by:

```
> ./par1 < sample1.pas
```

This will give a long list of parsed elements. There are some very poor error checking and warnings. But unless
you are wery well acquainted with the program you test, you will probably not guess correctly what the problem
(syntax error) will be or what is indicated from the parsing. Again, this is not how parsers should be written,
but some code that will hopwfully show what parsing in a very general way looks like.
At this stage our interest is only with the *syntax* and not if the program is correct in any other way.
