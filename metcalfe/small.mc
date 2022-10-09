#     S -> A B
#     A -> x | xz
#     B -> y | zy

      call    :S
      stop

S:
      call    :A
      false:  :SX
      call    :B
SX:
      return

A:
      match   x
      true    :AX
      match   xz
AX:
      return

B:
      match   y
      true    :BX
      match   zy
BX:
      return
