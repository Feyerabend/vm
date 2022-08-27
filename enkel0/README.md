# Virtual Machines

Simple compiler from parsed text to assembly, to running code on a virtual machine.

![Simplified BNF for enkel/0, a simple compiler](assets/images/enkel0.png)

## enkel0

The language is called *enkel/0* which is Swedish for "simple/0" in the spirit of PL/0.
The language inherits and have similarities with PL/0. Let's make some preliminary
observations of some features from *enkel/0*.

A simple program could be written as:

```
var x;

begin
  x is 7;
  print x
end.

```

Programs always ends with a period. Statements are *seperated* by a semicolon, and not as
in C *terminated* with a semicolon. Several statements are grouped by _begin_ and _end_.
Global variables are set at the beginning af the program. Assignments is done by _is_
(and not as in Algol or Pascal with ":="). You can _print_ a variable (new line at the end).

Let's look at a little more complicated program, factorial:

```
procedure factorial[n];
  var m;
  begin
    if n = 1 then return 1;
    m is n - 1;
    call factorial[m];
    rval is (n * rval)
  end;

begin
  call factorial[10];
  print rval
end.
```

The main calling part of the program is at the bottom surrounded by _begin_ and _end_:

```
...

begin
  call factorial[10];
  print rval
end.
```

From here we call factorial above with the argument 10. From the returning procedure we
then print the returning value. The returning value is stored in the fixed predefined global
variable _rval_ (which always holds the current return value).

The procedure factorial is defined with an argument _n_:

```
procedure factorial[n];
  var m;
  begin
    if n = 1 then return 1;
    m is n - 1;
    call factorial[m];
    rval is (n * rval)
  end;

...
```

Local variables are declared thereafter, here _m_. A group of statements seperated by semicolon
is the core of the program. First compare the incomming argument _n_ with 1, if true then return
from procedure to the previous caller with the value 1 (stored in _rval_).

The local Variable _m_ is set to incomming _n_ minus 1. Another call recursively to factorial
with m as argument is done. Then from returning calls, the returning value in _rval_ is multiplied
with _n_ and returned. This is all done through the stack, and using the basics from the vm already
described. Actually the vm is still very small, although the language has grown in complexity,
but in a way that *we* understand programming easier.

...

