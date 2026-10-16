; Divides by zero three calls deep, to show what the debugger
; prints when a program traps.

main:   PUSH 3
        CALL down 1
        HALT

; down(n): divide 100 by n, then call down(n - 1)
down:   PUSH 100
        LOAD 0
        DIV
        DROP
        LOAD 0
        PUSH 1
        SUB
        CALL down 1
        RET
