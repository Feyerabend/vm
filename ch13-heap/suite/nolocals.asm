; A call with no arguments starts with no locals, and can make some.
main:   PUSH 1
        CALL f 0
        PRINT           ; 3
        PRINT           ; 1
        HALT
f:      PUSH 3
        LOAD 0
        RET
