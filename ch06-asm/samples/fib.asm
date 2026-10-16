; The first ten Fibonacci numbers.
; The stack holds a b n, where n counts down to zero.

        PUSH 0          ; a
        PUSH 1          ; b
        PUSH 10         ; n
loop:   DUP
        JZ end          ; leave when n = 0
        PUSH 1
        SUB             ; a b n-1
        ROT
        ROT             ; n a b
        OVER
        PRINT           ; print a
        SWAP
        OVER
        ADD             ; n b (a + b)
        ROT             ; b (a + b) n
        JMP loop
end:    HALT
