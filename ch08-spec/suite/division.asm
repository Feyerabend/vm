; DIV rounds towards zero; MOD has the sign of the dividend.
        PUSH 7
        PUSH 2
        DIV
        PRINT           ; 3
        PUSH -7
        PUSH 2
        DIV
        PRINT           ; -3
        PUSH 7
        PUSH -2
        DIV
        PRINT           ; -3
        PUSH -7
        PUSH -2
        DIV
        PRINT           ; 3
        PUSH 7
        PUSH 2
        MOD
        PRINT           ; 1
        PUSH -7
        PUSH 2
        MOD
        PRINT           ; -1
        PUSH 7
        PUSH -2
        MOD
        PRINT           ; 1
        PUSH -7
        PUSH -2
        MOD
        PRINT           ; -1
        HALT
