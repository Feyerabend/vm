; Memory starts as all zeros, keeps what is stored, and is shared by
; every call.
main:   PUSH 0
        LOADM
        PRINT           ; 0
        PUSH 4095
        LOADM
        PRINT           ; 0
        PUSH 7
        PUSH 42
        STOREM
        PUSH 7
        LOADM
        PRINT           ; 42
        CALL f 0
        DROP
        PUSH 4095
        LOADM
        PRINT           ; 7
        PUSH 0
        LOADM
        PRINT           ; -9
        HALT
f:      PUSH 4095
        PUSH 7
        STOREM
        PUSH 0
        PUSH -9
        STOREM
        PUSH 0
        RET
