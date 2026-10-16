<p align="center"><img src="../assets/logo-enkel.png" width="480" alt="enkel/0"></p>

# The enkel/0 language

*enkel* is Swedish for *simple*. The language belongs to the family
of Niklaus Wirth's PL/0 and Pascal, and like them it is meant to be
read: keywords instead of symbols, and one way to do each thing.

## Grammar

```ebnf
program    = block "." .

block      = [ "const" name "=" number { "," name "=" number } ";" ]
             [ "array" name ":" number { "," name ":" number } ";" ]
             [ "var" name { "," name } ";" ]
             { "procedure" name "[" [ name { "," name } ] "]" ";" block ";" }
             statement .

statement  = variable "is" expression
           | "call" name "[" [ expression { "," expression } ] "]"
           | "begin" statement { ";" statement } "end"
           | "if" condition "then" statement [ "else" statement ]
           | "while" condition "do" statement
           | "do" statement "while" condition
           | "return" [ expression ]
           | "print" expression
           | "emit" expression
           | (nothing) .

condition  = expression [ ( "=" | "#" | "<" | "<=" | ">" | ">=" ) expression ] .
expression = term { ( "+" | "-" | "or" | "xor" ) term } .
term       = factor { ( "*" | "/" | "%" | "and" ) factor } .
factor     = variable | number | "(" expression ")" | "-" factor .
variable   = name [ "." ( name | number | "(" expression ")" ) ] .
```

Comments are written `{ like this }` and may span lines.

## Names

- **`const`** names a number. It cannot be changed.
- **`array`** declares a global array: `array A:10` has elements
  `A.0` to `A.9`. Arrays can only be declared at the top of the
  program.
- **`var`** at the top of the program declares global variables. In a
  procedure, it declares local variables, which exist only while that
  call lasts.
- **`procedure`** declares a procedure. Its arguments are local
  variables too, holding copies of the values it was called with.
  Procedures can call themselves and each other, in any order.
  They cannot be declared inside other procedures.

Every global variable and every array element starts as 0. A local
variable starts as 0 too.

## Statements

- `x is e` assigns. `#` means *not equal*.
- `call p[a, b]` calls a procedure. It is a statement, not an
  expression: the result of a call, if any, is found afterwards in the
  global variable **`rval`**.
- `return e` leaves the procedure, and sets `rval` to e. A `return`
  without a value, or the end of the procedure, leaves `rval` as it
  was. A `return` in the main program ends the program.
- `print e` prints e as a number, on a line of its own.
- `emit e` prints the character with code e: `emit 65` prints `A`,
  `emit 10` ends a line.
- `if`, `while`, and `do ... while` take a condition. Any expression
  is a condition: 0 is false, anything else is true.
- `and`, `or` and `xor` work on the bits of numbers: `13 and 6` is 4.

## Arithmetic

As in the machine: 32-bit integers that wrap around, and division
that rounds towards zero.

## Arrays are not checked

`A.i` with i outside the array reads or writes whatever lies next to
it in memory, with no warning. The compiler does catch a *constant*
index that is out of range, such as `A.10` for `array A:10`, but not
one that is computed while the program runs.
