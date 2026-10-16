; AND, OR and XOR work on the bits of 32-bit two's complement values.
        PUSH 12
        PUSH 10
        AND
        PRINT           ; 8
        PUSH 12
        PUSH 10
        OR
        PRINT           ; 14
        PUSH 12
        PUSH 10
        XOR
        PRINT           ; 6
        PUSH -1
        PUSH 255
        AND
        PRINT           ; 255
        PUSH -2147483648
        PUSH 1
        OR
        PRINT           ; -2147483647
        PUSH 5
        PUSH -1
        XOR
        PRINT           ; -6
        HALT
