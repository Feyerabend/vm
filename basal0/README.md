# Virtual Machines

*Simple compiler from parsed text to assembly, to running code on a virtual machine.*


## compile and run

There is already a file `sample.bas` in the main directory, which you can compile and
run:

```shell
> make all
> ./build.sh
```


## basal/0

```ebnf
 newline = NL

 program =
      statements NL .

 statements =
     statement NL statements
     | statement NL .

 statement =
     "!" label 
     | "GOTO" label
     | "GOSUB" label
*    | "ON" ident "GOTO" label {, label}
*    | "ON" ident "GOSUB" label {, label}
     | "LET" ident "=" expression
     | "IF" condition "THEN" NL statements NL { "ELSE" statements NL } "ENDIF"
     | "WHILE" condition "DO" NL statements NL "ENDWHILE"
*    | "FOR" ident "=" number "TO" number {"STEP" number} NL statements "NEXT" ident
     | "RETURN"
     | "END"
     | "PRINT" (number | string[";"]) .

 condition =
     expression ("="|"<>"|"<"|"<="|">"|">=") expression .

 expression =  term {("+"|"-") term} .

 term = factor {("*"|"/") factor} .

 factor =
     ident
     | ["-"|"+"] number
     | "(" expression ")" .
```

The language is called *basal/0* which is Swedish for "basic/0" in the spirit of *PL/0*
and *enkel/0*. The language inherits and have similarities with BASIC. The main point
here is to illustrate how a compiler can address manipulation of tokens, in this case,
to enhance the language. Also BASIC has a relatively simple syntax to build from, as
it mostly relies on simple statements that do not require to much energy to parse.


## sample

A simple program could be written as:

```basic
LET x = 5
PRINT x
```

This translates, as previously, to:

```assembly
START:
  SET	5
  STORE	0
  LOAD	0
  PRINT
END:
  HALT
```

The intermediary file `tokens.csv` looks like:

```csv
"type"|"text"
"0"|"
"
"0"|"
"
"504"|"LET"
"2"|"x"
"200"|"="
"1"|"5"
"0"|"
"
"502"|"PRINT"
"2"|"x"
"0"|"
"
"0"|"
"
"511"|"END"
"0"|"
"
"0"|"
"
```

The order in which compilation and running is also in principal as previously:

```shell
> python3 compiler.py -i sample.bas -o sample.a
> python3 asm.py -i sample.a -o sample.b
> ./runvm sample.b
```

The main chain of events is in `compiler.py` itself. Here first tokens are picked from the input text `tok.py` and `lexer.py`.
Then the result is stored as a Python dictionary to a text file `tokens.csv`. The textfile is then put through a "filter" where
syntactic extras as `FOR-NEXT`, `ON-GOSUB` and `ON-GOTO` are translated into tokens that are equivalent but comprehensible to
the compiler `parse.py`. From the compilation a pass through the assembler `asm.py` give the binary to the running vm.
There is thus a possibility to compile without the extra filter, and thus not have access to extra sugar.

There are many (intensional) limits to this language. One limit is how `FOR-NEXT` works. No expressions are allowed, 
only numbers, to keep things simple. This allows for looping "downwards" from a higher number to a lower, negative
numbers (not expressions) had to be added to `STEP`.

