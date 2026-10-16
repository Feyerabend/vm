; Factorial, recursively.

main:   PUSH 5
        CALL fact 1
        PRINT
        PUSH 10
        CALL fact 1
        PRINT
        HALT

; fact(n): local 0 is n
fact:   LOAD 0
        PUSH 2
        LT
        JZ recurse      ; n >= 2
        PUSH 1
        RET
recurse:
        LOAD 0          ; n
        LOAD 0
        PUSH 1
        SUB
        CALL fact 1     ; fact(n - 1)
        MUL
        RET
