#  production rules of an ETF grammar
#  Expression-Term-Factor:
#
#  S -> E $
#  E -> T | E + T
#  T -> F | T * F
#  F -> i | ( E )
#
#  take as input (from a wff)
#  infix representation, then translate to
#  the corresponding prefix expression
#  <expression>-grammar:
#
#  <expression> ::= <term> | <expression> + <term>
#        <term> ::= <factor> | <term> * <factor>
#      <factor> ::= i | ( <expression> )
#  

      call    :S
      stop

S:
      call    :E
      false   :SX
      match   $         # end of input
SX:
      return

E:
      call    :T
      false   :EX
E1:
      match   +
      false   :E2
      call    :T
      false   :EX
      print   +
      true    :E1
E2:
      tflag
EX:
      return

T:
      call    :F
      false   :TX
T1:
      match   *
      false   :T2
      call    :F
      false   :TX
      print   *
      true    :T1
T2:
      tflag
TX:
      return

F:
      match   i
      false   :F1
      print   i
      true    :FX
F1:
      match   (
      false   :FX
      call    :E
      false   :FX
      match   )
FX:
      return
