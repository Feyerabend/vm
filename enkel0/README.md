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
then print the returning value. The returning value is stored in the fixed predefined
global variable _rval_ (which always holds the current return value).

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

Local variables are declared thereafter, here _m_. A group of statements seperated by
semicolon is the core of the program. First compare the incomming argument _n_ with 1,
if true then return from procedure to the previous caller with the value 1 (stored in _rval_).

The local Variable _m_ is set to incomming _n_ minus 1. Another call recursively to factorial
with m as argument is done. Then from returning calls, the returning value in _rval_ is multiplied
with _n_ and returned. This is all done through the stack, and using the basics from the vm already
described. Actually the vm is still very small, although the language has grown in complexity,
but in a way that *we* understand programming easier.


### insertion sort

```
array A:10;

procedure nl[];
  begin
    emit 13; emit 10
  end;

procedure swap[a, b];
  var u;
  begin
    u is A.a;
    A.a is A.b;
    A.b is u
  end;

procedure write[n];
  var j;
  begin
    j is 0;
    do
      begin
        print A.j;
        j is j + 1
      end
    while j < n;
    call nl[]
  end;

procedure insert[n];
  var i, j, m;
  begin
    i is 0;
    do
      begin
        j is i;
        m is i;
        do
          begin
            if A.j < A.m then m is j;
            j is j + 1
          end
        while j < n;
        call swap[i, m];
        i is i + 1
      end
    while i < n
  end;

begin
  A.0 is 90;
  A.1 is 45;
  A.2 is 4;
  A.3 is 56;
  A.4 is 1;
  A.5 is 99;
  A.6 is 8;
  A.7 is 50;
  A.8 is 32;
  A.9 is 10;

  call write[10];
  call insert[10];
  call write[10]
end.
```

Result from compiling, assembling and running:

```
- - - - - - - - - - - -
90
45
4
56
1
99
8
50
32
10

1
4
8
10
32
45
50
56
90
99

- - - - - - - - - - - -
```

...

