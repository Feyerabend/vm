# Virtual Machines

Virtual machine samples.[^1] A collection of virtual machines to teach
or understand some ideas and inner workings of virtual machines. They are
solely intended for show of principles, and not for uses in any other way.
The second objective is to downplay the separation between system programmers
and application programmers. Or even in some cases down to the hardware level,
programming of FPGA. More on this later on.

[^1]: My best inspiration for the code of simple machines *here* comes from
Bartosz Sypytowski: https://bartoszsypytkowski.com/simple-virtual-machine/
from whom I derived basically the main code, even though some bugs
were corrected and many more additions have been made along the way.
You also might have a look at the Wikipedia page on VMs:
https://en.wikipedia.org/wiki/Virtual_machine

These samples assume some understanding of elementary computer science,
as you would get from an introductory course in e.g. programming. They are
also presumed to be interesting for those who want to go further than the
elementary.

My interest in virtual machines started long time ago, first with
*UCSD Pascal* on the *Apple II* sometime around 1980 or 1981 ...


### A note on concepts

The term "virtual machine" can often be replaced by "emulator",
"interpreter" etc. and perhaps should not be restricted or qualified too much
right here. The idea of an abstraction that separates the underlying mechanics
from the levels above is what should be observed, not a deepend confusion of
concepts which already are often ambiguous.

The term "virtual machine" and also "interpreter" has been used for such diverse
fields as from the Apollo Guidance Computer,[^2] code from Busicom interpreted[^3]
to run on Intel 4004, and Steve Wozniack routines in SWEET16.[^4]

[^2]: This does not verify the reference, but gives general info on AGC,
https://en.wikipedia.org/wiki/Apollo_Guidance_Computer.
Also see manual https://www.ibiblio.org/apollo/assembly_language_manual.html.

[^3]: Nor this verify reference to VM, but general info on Intel 4004,
https://en.wikipedia.org/wiki/Intel_4004.

[^4]: SWEET16, https://en.wikipedia.org/wiki/SWEET16 but also in Byte no 11, 1977:
https://archive.org/details/BYTE_Vol_02-11_1977-11_Sweet_16/page/n151/mode/2up.

__WARNING: The machines and additives shown here are not complete
in any way. There are many missing necessary features and code that
should be amended were it written for real purposes. The idea is to show
and view certain aspects on coding/programming and to hide others.__



## *From virtual machines to compilers*


### 1. [vm1](/vm1)

We start off with a simple virtual stack machine. There is no error checking,
no warnings, you have to compile the machine if you only slightly change
the program, etc. The idea is to grasp what happens inside the virtual
machine and use code as the main instructive part.


### 2. [vm2](/vm2)

Next, the machine has been expanded with unconditional and conditional jumps,
some storage facilities, but also adding some concepts deriving from FORTH,
such as e.g. DROP, DUP, or SWAP. The algorithm of Fibonacci is used archetypically
with different implementations, where the concepts used from FORTH can be seen.
FORTH is also a language which can use a virtual machine and, as in C, it is
often close to the real machine on which it runs (often denoted by "low level
languages").


### 3. [vm3](/vm3)

This time we slim the machine down, get rid of the many extra powerful
concepts from FORTH. Instead we insert some "standard" concepts of call
and return through the use of "activation records".


### 4. [chip8](/chip8)

We have a look at an early virtual machine used for games starting
in the late 70's: CHIP-8. (*Not my code. Much better.*)


### 5. [cmp1](/cmp1)

Starting from the bottom, working our way up, here we take aim at the abstraction
of languages in a "tree". By getting an understanding of the language from pure
syntax to "abstract syntax tree" (AST), we lean toward the semantics. Especially
with formal languages such as in programming, this gets rather straightforward,
with some possible caveats.


### 6. [metcalfe](/metcalfe)

To explore some of the discoveries made early in the evolution of programming
languages and formalisations, an introduction to a simple token analyser
the "Metcalfe machine" is introduced for exploration. Even if the "machine"
never have had any lasting impact on parsing in general, the flexibility, as
you might make a separate small program, it is an interesting path. Usually
descriptive languages, or near descriptive, are used for generating tokenizers/parsers,
that are used today for parsing programming languages. Even simpler methods
can be adapted such as using e.g. regular expressions for separating "words" in
a programming language.


### 7. [cmp2](/cmp2)

We continue to focus on parsing, and look at parsing PL/0 programs. Also a scanner
is added for dealing with each "word" for input to a meaningful grammar.


### 8. [cmp3](/cmp3)

Arithmetical expressions can be compiled to bytecode/binary for the vm.
Mentions some, but do go into what, potential problems there are with parsing,
and division by zero as an example of runtime error.


### 9. [cmp4](/cmp4)

A compiler and vm for a simple calculator with no memory. No way to store
or fetch numbers through some mechanics for variables.


### 10. [enkel/0](/enkel0)

A more complete compiler for our own language, with some similarities to
"[Pascal](https://en.wikipedia.org/wiki/Pascal_(programming_language))"
[PL/0](https://en.wikipedia.org/wiki/PL/0) and other procedural languages.
It runs on its own virtual machine. Thus programs written in *enkel/0*
can be __ported to other environments__ (other implementations of the vm)
without much effort.


### 10. [basal/0](/basal0)

A compiler for a poor variant of "[BASIC](https://en.wikipedia.org/wiki/BASIC)"
which uses the previous vm (in C). The compiler is now written in the "rich"
high-level language Python3. The many features of Python make it much
easier to write certain tasks, but also thus hides some internal mechanism,
which can be useful to understand details in practice. This addition of a
compiler *basal/0* illustrates, together with *enkel/0*, how *different*
languages can be supported by the __same vm__. There are also some additional
remarks on how to look at extending a language, near "syntactic sugar".
I.e. a rewrite of the for us convenient language idioms to a, for the
machine, more suitable dressing.
