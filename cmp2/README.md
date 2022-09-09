# Virtual machines

*Parsing programs from text.* Sample with educational language [PL/0](https://en.wikipedia.org/wiki/PL/0).
We give a pass on the rest of the compiler for the moment.


## cmp2

We'll now make a jump from the *semantics* (abstractions) to *syntax* of programs. In this case we will chose the syntax
from the famous educational PL/0 language by Niklaus Wirth which has been around for many years.[^1] Maybe you will find
it very close resemblance to Pascal, which is no surprise, as Wirth also is behind Pascal, but PL/0 is much more limited,
especially designed for education (parsers / compilers).

[^1]: https://en.wikipedia.org/wiki/PL/0


### parser

The syntax of PL/0 formalized:

```enbf
program = block "." .
 
 block =
     ["const" ident "=" num {"," ident "=" num} ";"]
     ["var" ident {"," ident} ";"]
     {"procedure" ident ";" block ";"} statement .
 
 statement =
     ident ":=" expression
     | "call" ident
     | "begin" statement {";" statement } "end"
     | "if" condition "then" statement
     | "while" condition "do" statement .
 
 condition =
     "odd" expression
     | expression ("="|"#"|"<"|"<="|">"|">=") expression .
 
 expression = ["+"|"-"] term {("+"|"-") term} .
 
 term = factor {("*"|"/") factor} .
 
 factor =
     ident
     | number
     | "(" expression ")" .

```

The core of the parser can be found in the file `par1.c`. There are some small additions to the
one that can be found at the wikipedia page, to have it running.


### scanner

The second main thing is the introduction of a *scanner*: `scan.c` and `scan.h`. This at first
identifies *"words"* in incoming text. A string of text such as:

```
varx,squ,answer;procedure
``` 

Into separate more, to the parser, meaningful items:

```
var
x
,
squ
,
answer
;
procedure

```

Each item is then picked up by the parser to piece together phrases that are even more
suitable for the grammar. Some items are identified at first (accept), and the others are
expected (expect). If the order is not correct the parsing fails. The “wording” doesn't
make sense for the parser.

(Again, there are many holes in this parsing, and warnings and errors are far from being
detected as they should be built into a *real* parser.)


## run

```pascal
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

The above program calculates square of x, x² or (x * x) of a given number. Right now there
is no way to print the result, but also there is no semantics at all. So you will not be able
to run the program. It is for you to inspect the *syntactical structures*, and what parsing
does from the side of a text representation of simple program.

There is a wikipage which also gives part implementation of the syntactical analysis for PL/0:
https://en.wikipedia.org/wiki/Recursive_descent_parser as an example of recursive decent parsing.

What is lacking is a scanner that checks for tokens in a stream, and gives the parser each
"comprehensive" element here added as `scan.c` and `scan.h`.

To run `sample1.pas` compile the parser as usual (and scanner):

```shell
> make clean
> make par1
```

Then run the parser:

```shell
> ./par1 < sample1.pas
```

This will give a long list of parsed elements. There are some very poor error checking and
warnings. But unless you are wery well acquainted with the program you test, you will probably
not guess correctly what the problem (syntax error) will be or what is indicated from the parsing.

Again, this is *not* how parsers should be written, but some code that will hopwfully show what
parsing in a very general way looks like. At this stage our interest is only with the *syntax*
and not if the program is correct in any other way.




