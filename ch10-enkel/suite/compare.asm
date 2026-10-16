; LT and EQ leave 1 or 0.
        PUSH 1
        PUSH 2
        LT
        PRINT           ; 1
        PUSH 2
        PUSH 1
        LT
        PRINT           ; 0
        PUSH 2
        PUSH 2
        LT
        PRINT           ; 0
        PUSH -5
        PUSH 3
        LT
        PRINT           ; 1
        PUSH 4
        PUSH 4
        EQ
        PRINT           ; 1
        PUSH 4
        PUSH -4
        EQ
        PRINT           ; 0
        HALT
