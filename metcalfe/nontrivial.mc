
#     S -> A c
#     A -> a | B
#     B -> a b


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
      true    :AX
      call    :B
AX:
      return

B:
      match   ab
      return
