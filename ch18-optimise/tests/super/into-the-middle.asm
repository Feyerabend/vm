; A jump to the second instruction of a pair must run just that one.
        PUSH 10         ; local 0
        PUSH 3
        JMP second
        LOAD 0
second: PUSH 4          ; LOAD 0, PUSH 4 is a pair; this skips the LOAD
        ADD
        PRINT           ; 3 + 4 = 7
        LOAD 0
        PUSH 1
        ADD
        PRINT           ; 11
        HALT
