#     S -> c A d
#     A -> a b | a

      call    :S
      stop

S:
      match   c
      false   :SX
      call    :A
      false   :SX
      match   d
SX:
      return

A:
      match   ab
      true    :AX
      match   a
AX:
      return
