#  production rules
#  S -> a | xA
#  A -> Sz | SyA

      call    :S
      stop

S:
      match   a
      true    :SX
      match   x
      call    :A
SX:
      return

A:
      call    :S
      false   :AX
      match   z
      true    :AX
      call    :S
      false   :AX
      match   y
      call    :A
AX:
      return
