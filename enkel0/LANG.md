# Virtual Machines

## vmenkel


Description of the language *enkel/0*. ...

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
            | return [factor]
            | print factor
            | emit factor ]

condition = expression (=|#|<|<=|>|<=) expression

expression = [-] term { (+|-|or|xor) term }

term = factor { (*|/|%|and) factor }

factor = ident[. index] | number | ( expression )

index = (ident | number)
```



![Simplified BNF for enkel/0, a simple compiler](assets/images/enkel0.png)





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

```text
emit 72; emit 101; emit 108; emit 108; emit 111; emit 13; emit 10
```




