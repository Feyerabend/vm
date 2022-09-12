# Virtual Machines

## enkel/0

![enkel/0](../assets/images/logo.png)

A more formal ENBF like description of the language *enkel/0*:


```ebnf
 program = block "." .
 
 block =
     ["const" ident "=" number {"," ident "=" number} ";"]
     ["array" ident "=" number {"," ident "=" number} ";"]
     ["var" ident {"," ident} ";"]
     {"procedure" ident "[" ident {"," ident} "]" ";" block ";"}
      statement .
 
 statement =
     ident ["." index] "is" expression
     | "call" ident "[" ident {"," ident} "]"
     | "begin" statement {";" statement } "end"
     | "if" condition "then" statement { "else" statement }
     | "while" condition "do" statement
     | "do" statement "while" condition
     | return [factor]
     | print factor
     | emit factor .
 
 condition =
     expression ("="|"#"|"<"|"<="|">"|">=") expression .
 
 expression = ["-"] term {("+"|"-"|"or"|"xor") term } .
 
 term = factor {("*"|"/"|"%"|"and") factor } .
 
 factor =
     ident ["." index]
     | number
     | "(" expression ")" .

 index =
     ident
     | number .
```


### Program and Block

* If we start with how the structure of a program looks like, it consists of a *`<block>`* and `.`.
    All programs ends with a period.

* The *`<block>`* may have a `const` definition at the start, an `array`, or global variables `var`.
    Constants are global and may not be changed, only assigned once at the start. Arrays are also
    global (also have no checks for out of index adressing). Global variables may be assigned and
    reassigned throughout the program.

* After the initialisation there are an optional list of `procedure`s. The procedure is recognized
    by a program unique identifier *`<ident>`*. Then there is an optional list of arguments that
    comes from the call to the procedure. The arguments (values) are copied from the call to the
    procedure. Each argument *`<ident>`* is separated with a `,` comma. The arguments work as
    local variables throughout the procedure. The procedure *`<block>`* is ended with a `;` semicolon.

* Then at last there are statements that are the first to be called, and contain the main code of
    the program. A program might thus only consists of *`<statement>`* (in a *`<block>`*).


### Statement

A *`<statement>`* may consist of:

* An identifier *`<ident>`*, assigned by `is` to the value of an evaluated *`<expression>`*.
    The identifier might be in the form of an array which is treated as "two variables glued
    together by a period".
* A `call` with an identifier `<ident>` and possible arguments in the format of *`<factor>`*,
    separated by a `,` comma.
* A group of statements starting with `begin` and ending with `end`. The statements themselves
    are separated by a `;` (semicolon). This might be one of the thing you might want to change,
    e.g. with curly brackets, as in c, instead.
* A conditional jump, with `if` and `then`. This statement may include optional `else`. Thus
    if a *`<condition>`* has been made (true), then *`<statement>`* that follow will be executed,
    else if the condition was false, other *`<statement>`* might be executed instead.
* Two conditional jump structures are `while` *`<condition>`* `do` *`<statement>`*,
    and the reverse `do` *`<statement>`* `while` *`<condition>`*. As long as the *`<condition>`*'
    is met, the *`<statement>`*  will be exectuted continously. The latter do-while executes at
    least one *`<statement>`*, which the former while-do does not.
* A `return`statement with optional return value. All return values are also copied to a special
    `rval` global variable. Therefore `rval` can also be treated as a ordinary global variable,
    although storing a value will be overwritten as soon as a call with returning value is made.
* There is a `print` of integer values.
* And `emit`can be used to display an ASCII character.


### Condition

* The *`<condition>`* occurs mostly together with some jump instruction, if-else-statements,
    while-do, or do-while. *Anyting else than 0 is taken as true.* It also departures from
    expressions which are compared with relative operations such as `<` less than or equal `=`.
    A special symbol `#` stands for "not equal" (other notations could be e.g. "<>" or "!=").


### Expression

* The *`<expression>`* can be a *`<term>`* with an optionary unary minus before. Or it (also)
    could be addition with a plus sign `+`, or subtractions with a minus sign `-`, or a logical
    `or` or `xor`.


### Term

* The *`<term>`* can be a *`<factor>`*. It can also be a *`<factor>`* with operators `*`, `/`, `%`
    or `and` connecting to the other *`<factor>`*.


### Factor

* The *`<factor>`* takes an ordinary *`<ident>`* or an identifier with an index i.e. an array,
    or it is a *`<number>`*, or it is an *`<expression>`* with parantheses around it.


### Index

* The implementation of arrays has been very restricted to only care for global arrays.
    In that way they are easy to handle. Arrays are basically global variables poiting to an
    array in the vm, with an attached *`<index>`* which points out where the value is, or the
    slot that will be assigned with a value. Also to keep the implementation small only a *`<number>`*
    (integer) or an identifier *`<ident>`* is allowed.


## ASCII and emit

In order to get printed text, there is an option of putting out letters each at a time.
Using the code table for ASCII we can emit a character at a time.

```text
       0 nul    1 soh    2 stx    3 etx    4 eot    5 enq    6 ack    7 bel
       8 bs     9 ht    10 nl    11 vt    12 np    13 cr    14 so    15 si
      16 dle   17 dc1   18 dc2   19 dc3   20 dc4   21 nak   22 syn   23 etb
      24 can   25 em    26 sub   27 esc   28 fs    29 gs    30 rs    31 us
      32 sp    33  !    34  "    35  #    36  $    37  %    38  &    39  '
      40  (    41  )    42  *    43  +    44  ,    45  -    46  .    47  /
      48  0    49  1    50  2    51  3    52  4    53  5    54  6    55  7
      56  8    57  9    58  :    59  ;    60  <    61  =    62  >    63  ?
      64  @    65  A    66  B    67  C    68  D    69  E    70  F    71  G
      72  H    73  I    74  J    75  K    76  L    77  M    78  N    79  O
      80  P    81  Q    82  R    83  S    84  T    85  U    86  V    87  W
      88  X    89  Y    90  Z    91  [    92  \    93  ]    94  ^    95  _
      96  `    97  a    98  b    99  c   100  d   101  e   102  f   103  g
     104  h   105  i   106  j   107  k   108  l   109  m   110  n   111  o
     112  p   113  q   114  r   115  s   116  t   117  u   118  v   119  w
     120  x   121  y   122  z   123  {   124  |   125  }   126  ~   127 del
```

To print "Hello" emit 'H', 'e', 'l', 'l', and 'o' with a new line at the end
(carridge return 13 and line feed 10), a statement can look like:

```pascal
begin emit 72; emit 101; emit 108; emit 108; emit 111; emit 13; emit 10 end
```




