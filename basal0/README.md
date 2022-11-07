# Virtual Machines

*Simple compiler from parsed text to assembly, to running code on a virtual machine.*


## compile and run

There is already a file `sample.bas` in the main directory, which you can compile and
run

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
     "LET" ident "=" expression
     | "GOTO" label
     | "GOSUB" label
     | "!" label
     | "IF" condition "THEN" NL statement NL { "ELSE" statement NL } "ENDIF"
     | "WHILE" condition "DO" NL statement NL "ENDWHILE"
     | "FOR" ident "=" number "TO" number {"STEP" number} NL statement "NEXT" number
     | "RETURN"
     | "END"
     | "PRINT" [number | string[";"]] .

 condition =
     expression ("="|"<>"|"<"|"<="|">"|">=") expression .

 expression =  term {("+"|"-") term} .

 term = factor {("*"|"/") factor} .

 factor =
     ident
     | ["-"|"+"] number
     | "(" expression ")" .
```

The language is called *basal/0* which is Swedish for "basic/0" in the spirit of PL/0
and enkel/0. The language inherits and have similarities with BASIC. The main point
here is to illustrate how a compiler can address manipulation of tokens, in this case,
to enhance the language. Also BASIC has a relatively simple syntax to build from.

A simple program could be written as:

```basic
LET x = 5
PRINT x
```
