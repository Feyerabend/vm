# Virtual Machines

*Simple compiler from parsed text to assembly, to running code on a virtual machine.*


## compile and run

There is already a file `sample.bas` in the main directory, which you can compile and
run ...




## basal/0

```ebnf
 newline = NL

 program =
      statement NL .

 statements =
     statement NL statements
     | statement

 statement =
     LET ident "=" expression NL
     | "GOTO" label NL
     | "GOSUB" label NL
     | "IF" condition "THEN" "NL" statement NL { "ELSE" statement NL } NL "ENDIF"
     | "WHILE" condition "DO" NL statement NL "ENDWHILE"
     | "FOR" ident = number "TO" number {STEP number} NL statement "NEXT" number
     | "RETURN" NL
     | "PRINT" [number | string[";"]] "NL"

 condition =
     expression ("="|"<>"|"<"|"<="|">"|">=") expression .

 expression =  term {("+"|"-"|"or"|"xor") term} .

 term = factor {("*"|"/") factor} .

 factor =
     ident
     | ["-"|"+"] number
     | "(" expression ")" .
```

The language is called *basal/0* which is Swedish for "basic/0" in the spirit of PL/0
and enkel/0. The language inherits and have similarities with BASIC.

A simple program could be written as:

```basic
LET x = 5
PRINT x
```
