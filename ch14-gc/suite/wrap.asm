; Arithmetic wraps around at 32 bits.
        PUSH 2147483647
        PUSH 1
        ADD
        PRINT           ; -2147483648
        PUSH -2147483648
        PUSH 1
        SUB
        PRINT           ; 2147483647
        PUSH 65536
        PUSH 65536
        MUL
        PRINT           ; 0
        PUSH 2147483647
        PUSH 2
        MUL
        PRINT           ; -2
        PUSH -2147483648
        PUSH -1
        MUL
        PRINT           ; -2147483648
        PUSH -2147483648
        PUSH -1
        DIV
        PRINT           ; -2147483648
        PUSH -2147483648
        PUSH -1
        MOD
        PRINT           ; 0
        PUSH 0
        PUSH -2147483648
        SUB
        PRINT           ; -2147483648
        HALT
