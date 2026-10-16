; The Collatz sequence from 27: halve when even, else 3n + 1,
; until 1 is reached. Prints the number of steps it takes.

main:   PUSH 27
        CALL steps 1
        PRINT
        HALT

; steps(n): local 0 is n, local 1 counts the steps
steps:  PUSH 0
loop:   LOAD 0
        PUSH 1
        EQ
        JZ step
        LOAD 1
        RET
step:   LOAD 0
        PUSH 2
        MOD
        JZ even
        LOAD 0          ; odd: n = 3n + 1
        PUSH 3
        MUL
        PUSH 1
        ADD
        JMP store
even:   LOAD 0          ; even: n = n / 2
        PUSH 2
        DIV
store:  STORE 0
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP loop
