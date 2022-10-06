#  production rules
#  of an ETF grammar
#  (expression-term-factor)

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
