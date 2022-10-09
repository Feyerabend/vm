#  production rules
#  S -> abc | ac
#  A -> a | D
#  D -> a b

      call    :S
      stop

S:
      call    :A
      false   :SX
      match   c
SX:
      return

A:
      match   a
      then    b
      then    c
      true    :AX
      match   a
      then    b
AX:
      return
