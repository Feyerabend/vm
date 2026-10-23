# The pascal/0 language

pascal/0 is a small part of Pascal: enough to show what the P4 machine
was built for, nested procedures and typed values, and small enough to
compile in one pass by a program you can read in an evening. Every
pascal/0 program is a Pascal program, and prints the same with any
Pascal compiler; the tests check this against Free Pascal.

## Grammar

```ebnf
program     = "program" name [ "(" name { "," name } ")" ] ";" block "." .

block       = [ "const" name "=" constant ";" { name "=" constant ";" } ]
              [ "type" name "=" type ";" { name "=" type ";" } ]
              [ "var" names ":" type ";" { names ":" type ";" } ]
              { ( "procedure" name [ parameters ]
                | "function" name [ parameters ] ":" name ) ";" block ";" }
              compound .

parameters  = "(" group { ";" group } ")" .
group       = [ "var" ] names ":" name .
names       = name { "," name } .

type        = name
            | "array" "[" bounds { "," bounds } "]" "of" type .
bounds      = constant ".." constant .
constant    = [ "+" | "-" ] ( number | name ) | character .

compound    = "begin" statement { ";" statement } "end" .
statement   = variable ":=" expression
            | name ":=" expression                  (* a function's result *)
            | name [ "(" expression { "," expression } ")" ]
            | compound
            | "if" expression "then" statement [ "else" statement ]
            | "while" expression "do" statement
            | "repeat" statement { ";" statement } "until" expression
            | "for" name ":=" expression ( "to" | "downto" ) expression
                  "do" statement
            | "case" expression "of" case { ";" case } [ ";" ] "end"
            | (nothing) .
case        = constant { "," constant } ":" statement .

expression  = simple [ ( "=" | "<>" | "<" | "<=" | ">" | ">=" ) simple ] .
simple      = [ "+" | "-" ] term { ( "+" | "-" | "or" ) term } .
term        = factor { ( "*" | "div" | "mod" | "and" ) factor } .
factor      = number | character | variable | name [ "(" expression { "," expression } ")" ]
            | "(" expression ")" | "not" factor .
variable    = name { "[" expression { "," expression } "]" } .
```

Comments are written `{ like this }` or `(* like this *)`. Names and
keywords may be written in any case: `Begin`, `BEGIN` and `begin` are
the same word. A character is one character in quotes, `'a'`; a quote
is written twice, `''''`.

## Types

- **`integer`**, **`boolean`** and **`char`**, and arrays of them, and
  arrays of arrays: `array [1..3, 1..3] of integer` is the same as
  `array [1..3] of array [1..3] of integer`, and `a[i, j]` is `a[i][j]`.
  An array's index runs between two constants, numbers or characters:
  `array ['a'..'z'] of integer`.
- **`type`** gives a type a name. Two arrays have the same type only if
  they are declared with the same name, or in the same declaration.
- The constants **`true`**, **`false`** and **`maxint`** are
  predeclared.

## Procedures and functions

Procedures and functions can be declared inside each other, as deep as
you like, and an inner one uses the variables of those around it. They
can call themselves, and any procedure declared before them or around
them; pascal/0 has no `forward`, so two procedures cannot call each
other.

A **value parameter** is a local variable that starts with a copy of
the argument. A **`var` parameter** is the argument itself: the
procedure is given its address, and what it does to the parameter it
does to the caller's variable. Arrays can only be passed as `var`
parameters.

A function returns an `integer`, `boolean` or `char`. Inside it, its
own name on the left of `:=` sets the result; anywhere else, the name
calls it.

## Statements

- `for v := a to b do s` runs s with v from a up to b, and `downto`
  counts down. b is computed once, before the loop. v must be a
  variable of the procedure, or of the main program, not a parameter.
- `case e of` jumps to the branch with e's value among its labels. As
  in standard Pascal there is no `else`: a value with no label stops
  the program.
- `write` and `writeln` write integers, characters, booleans and
  strings, each optionally with a width, `x:5`. Without one, an integer
  takes 11 places, a boolean 5, a character 1, and a string its own
  length, as in Free Pascal's ISO mode. A string longer than its width
  is cut to it.
- `read` and `readln` read integers and characters from input.

The standard functions are `abs`, `sqr`, `odd`, `ord`, `chr`, `succ`,
`pred`, `eoln` and `eof`.

## What is left out

Real numbers, sets, records, pointers, files other than input and
output, subranges and enumerations as types, `goto`, `with`, `forward`,
procedures as parameters, and strings as values. The P4 machine can do
all of these; pascal/0 leaves them out to stay small, and adding some
of them is the exercises' work.

## Arithmetic

Integers have no limit on this machine. Free Pascal's have 32 bits,
so a program that goes past `maxint` is outside pascal/0: the two will
not agree. `div` rounds towards zero, and `mod` is never negative:
`-7 mod 2` is 1, and `x mod 0` or `x mod -2` stops the program.

## What is checked

The compiler checks types, as Pascal requires. The machine checks
the rest while the program runs: an index outside its array, a
division by zero, a `case` value with no label, and a variable used
before it is given a value. On the original P4 machine, that last one
read whatever was left in the word.
