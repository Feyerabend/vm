; DUP, DROP, SWAP, OVER and ROT. Printing pops from the top.
        PUSH 1
        PUSH 2
        PUSH 3          ; 1 2 3
        ROT             ; 2 3 1
        PRINT           ; 1
        PRINT           ; 3
        PRINT           ; 2
        PUSH 4
        PUSH 5
        SWAP            ; 5 4
        PRINT           ; 4
        PRINT           ; 5
        PUSH 6
        PUSH 7
        OVER            ; 6 7 6
        PRINT           ; 6
        PRINT           ; 7
        DUP             ; 6 6
        PRINT           ; 6
        PRINT           ; 6
        PUSH 8
        PUSH 9
        DROP
        PRINT           ; 8
        HALT
