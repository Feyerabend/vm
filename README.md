
# Virtual Machines

This collection of virtual machine examples[^1] is designed to help you
grasp some of the fundamental ideas and inner workings of virtual machines.
We’ll start with experimental implementations and gradually move toward
more advanced concepts like parsing, compiling, garbage collection, and
beyond. These examples are meant primarily for educational purposes and
are not intended for practical, real-world applications.

[^1]: My inspiration for the basic code of these simple machines comes
from Bartosz Sypytkowski: https://bartoszsypytkowski.com/simple-virtual-machine/.
While I derived much of the main code from his work, I have corrected bugs
and made numerous additions along the way. For further reading, you may also
want to check out the Wikipedia page on virtual machines:
https://en.wikipedia.org/wiki/Virtual_machine, or a comprehensive guide to
various abstract machines:
https://www.rw.cdl.uni-saarland.de/people/diehl/private/pubs/articleDiehlHartelSestoft.pdf.

These examples assume you have some basic knowledge of computer science,
like what you might gain from an introductory programming course. However,
they are also intended to be interesting for those who want to delve deeper
into the subject of virtual machines.

In this collection, we will explore a wide range of virtual machines, from
simple stack-based machines to more complex systems like a simplified JVM.
Along the way, we've delved into the principles of compilers, parsers, and
memory management, showing how these concepts interact with and build upon
each other. Whether you’re just beginning to explore virtual machines or
looking to deepen your understanding, these examples provide a foundation
for further study.

My journey into virtual machines began years ago with UCSD Pascal on
the Apple II around 1980 or 1981. But enough about that—-let’s dive
into the world of VMs together!


### A Note on Concepts

The term "virtual machine" can often be interchanged with "emulator,"
"interpreter," and similar terms. It’s important not to get too caught
up in the definitions here. The key idea is the abstraction that separates
the underlying mechanics from the levels above. We should focus on
understanding this abstraction rather than getting lost in the many
overlapping and sometimes ambiguous definitions.

The terms "virtual machine" and "interpreter" have been used in various
fields, from the Apollo Guidance Computer[^2] to the code from Busicom
that was interpreted[^3] to run on the Intel 4004, and even Steve Wozniak's
routines in SWEET16.[^4]

[^2]: For more information on the Apollo Guidance Computer,
visit: https://en.wikipedia.org/wiki/Apollo_Guidance_Computer.
The assembly language manual can be found at:
https://www.ibiblio.org/apollo/assembly_language_manual.html.

[^3]: For more on the Intel 4004, see: https://en.wikipedia.org/wiki/Intel_4004.

[^4]: For details on SWEET16, check: https://en.wikipedia.org/wiki/SWEET16.
You might also want to read the November 1977 issue of Byte:
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

We have a look at an early virtual machine used for games starting in the
late 70's: CHIP-8. (*Not my code. Much better.*)


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
or fetch numbers through some mechanics for variables. The program (expression)
is compiled to a assembly variant, and from that assembled to code, which
runs on a virtual machine.


### 10. [enkel/0](/enkel0)

A more complete compiler for our own language, with some similarities to
[Pascal](https://en.wikipedia.org/wiki/Pascal_(programming_language)),
[PL/0](https://en.wikipedia.org/wiki/PL/0) and other procedural languages
of the same generation.
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


### 11. [vm4](/vm4)

To examplify two virtual machines, a second implementation of the vm has
been done in Python3. They are not really mirrors of each other, as
they differ in behaviours. Thus a *specification* is needed of a vm
that they both implement.


### 12. [jvm1](/jvm1)

We experiment with a simple, very simple, implementation of a kind of
[Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine),
start with reading Java-classes (in Python3). The parallel with the specification
can be seen quite clearly in the implementation.


### 13. [jvm2](/jvm2)

Next is a implementation of also running some code from the reading of the file.
It keeps to the absolute minimum and can only cope with a 'hello world' program
for illustration.


### 14. [pitiful](/pitiful)

A small JVM written in C.


### 15. [ps](/ps)

Incorporating graphic capabilities into a virtual machine by integrating
concepts from *PostScript*.


### 16. [debug](/debug)

Some traditional debugging tools, such as single step, trace, and logging,
are introduced. Additionally, a small test suite is included to make the
VM easier to manage and e.g. to minimize the risk of breaking functionality
during porting.


### 17. [parse](/parse)

Parsers have a long tradition. Ordinary recursive decent parsers can be
constructed by hand, but also be automated. An interesting more recent
development is *combinator parsers*.


### 18. [vm5](/vm5)

Memory management in the form of a simple *garbage collector* named
*mark-and-sweep* is introduced, and a sample is given of a virtual machine
that manipulates a managed list as a dynamic data structure.


### 19. [add](/add)

This comparison explores addition from two perspectives: a low-level
hardware using a full adder in Verilog, and a high-level abstract using
lambda calculus. The hardware approach focuses on implementing binary
addition in circuits, while the abstract approach uses mathematical
functions to represent and manipulate numbers in a more formal, logical
sense. Together, they show the spectrum of abstraction in computer
science, from physical hardware to theoretical computation.


## License

Every folder with code should be in the main self-contained, and few if any
dependencies. For each folder, if no other license has been explicitly added
in that folder, the general *Unlicense* apply. In other cases where a license
has been added to the folder, the added license is applied and valid only in
the case for the content of that folder.
