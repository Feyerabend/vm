main:
; 28: moves is 0;
        PUSH 1
        PUSH 0
        STOREM
; 29: call hanoi[4, 1, 2, 3];
        PUSH 4
        PUSH 1
        PUSH 2
        PUSH 3
        CALL p_hanoi 4
        DROP
; 30: emit 10;
        PUSH 10
        EMIT
; 31: print moves     { 2^4 - 1 = 15 }
        PUSH 1
        LOADM
        PRINT
        HALT

; procedure move
p_move:
; 11: emit from + 48;
        LOAD 0
        PUSH 48
        ADD
        EMIT
; 12: emit to + 48;
        LOAD 1
        PUSH 48
        ADD
        EMIT
; 13: emit 32;
        PUSH 32
        EMIT
; 14: moves is moves + 1
        PUSH 1
        PUSH 1
        LOADM
        PUSH 1
        ADD
        STOREM
        PUSH 0
        RET

; procedure hanoi
p_hanoi:
; 19: if n > 0 then
        LOAD 0
        PUSH 0
        SWAP
        LT
        JZ L1
; 21: call hanoi[n - 1, a, c, b];
        LOAD 0
        PUSH 1
        SUB
        LOAD 1
        LOAD 3
        LOAD 2
        CALL p_hanoi 4
        DROP
; 22: call move[a, c];
        LOAD 1
        LOAD 3
        CALL p_move 2
        DROP
; 23: call hanoi[n - 1, b, a, c]
        LOAD 0
        PUSH 1
        SUB
        LOAD 2
        LOAD 1
        LOAD 3
        CALL p_hanoi 4
        DROP
L1:
        PUSH 0
        RET
