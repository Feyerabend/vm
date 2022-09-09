# Virtual Machines

Simple compiler from parsed text to assembly, to running code on a virtual machine.


## compile and run

There is already a file `sample.p` in the main directory, which you can compile and run:

```shell
> make all
> ./compile.sh
```

The result should be the classical `Hello world`. All the program does is emit ASCII characters:

```pascal
begin
  emit 72;
  emit 101;
  emit 108;
  emit 108;
  emit 111;
  emit 32;
  emit 119;
  emit 111;
  emit 114;
  emit 108;
  emit 100;
  emit 13;
  emit 10
end.
```

The simplest way to run the samples is to copy them to the "local root" directory and change the
name to `sample.p`. Then no change of script `compile.sh` is needed.


## enkel/0

![enkel/0](../assets/images/logo.png)

```ebnf
program = block .

block = [ const ident = number {, ident = number} ; ]
        [ array ident : number {, ident : number} ; ]
        [ var ident {, ident} ; ]
        { procedure ident[ [ident {, ident}] ] ; block ; }
          statement

statement = [ ident[. index] is expression
            | call ident[ [factor {, factor}] ]
            | begin statement {; statement } end 
            | if condition then statement { else statement }
            | while condition do statement
            | do statement while condition
            | return [factor]
            | print factor
            | emit factor ]

condition = expression (=|#|<|<=|>|<=) expression

expression = [-] term { (+|-|or|xor) term }

term = factor { (*|/|%|and) factor }

factor = ident[. index] | number | ( expression )

index = (ident | number)
```

The language is called *enkel/0* which is Swedish for "simple/0" in the spirit of PL/0.
The language inherits and have similarities with [PL/0](). Let's make some preliminary
observations of some features from *enkel/0*. A more detailed description can be found in
[LANG.md](LANG.md).

A simple program could be written as:

```pascal
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

```pascal
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

```pascal
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

```pascal
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

The local variable _m_ is set to incomming _n_ minus 1. Another call recursively to
factorial with m as argument is done. Then from returning calls, the returning value in
_rval_ is multiplied with _n_ and returned. This is all done through the stack, and using
the basics from the vm already described. Actually the vm is still very small, although
the language has grown in complexity, but in a way that *we* understand programming easier.


#### note

We could also write the program as:

```pascal
procedure factorial[n];
  var m, o;
  begin
    if n = 1 then return 1;
    o is n - 1;
    call factorial[o];
    return (n * rval)
  end;

begin
  call factorial[10];
  print rval
end.
```

This will however generate an assembler file which have two consecutive returns, due to how
the code is generated:

```text
RET
RET
```

Now you can choose how to eliminate this. Should a flag be inserted which flags for when
a `RET` has been generated, or should the assembler take care of the double `RET`? Or do
you have another solution that could take care of this unnecessary extra?


### insertion sort

```pascal
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

```shell
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

