; EQ on references compares identity, not contents. A reference is
; never equal to a number. Two copies of one reference see the same
; fields. Local 0 is block r, local 1 is block s.
main:   PUSH 1
        NEW
        PUSH 1
        NEW
        CALL test 2
        HALT
test:   LOAD 0
        LOAD 0
        EQ
        PRINT           ; 1: r is r
        LOAD 0
        LOAD 1
        EQ
        PRINT           ; 0: r and s are different blocks, though alike
        LOAD 0
        PUSH 0
        EQ
        PRINT           ; 0: a reference is not the number 0
        LOAD 0
        DUP             ; two copies of r
        PUSH 0
        PUSH 99
        SETF            ; write through one copy
        PUSH 0
        GETF            ; read through the other
        PRINT           ; 99
        PUSH 0
        RET
