; f has no locals, so it cannot pass one on, even though the caller's
; values are on the stack below.
main:   PUSH 1
        PUSH 2
        CALL f 0
        HALT
f:      CALL g 1
g:      RET
