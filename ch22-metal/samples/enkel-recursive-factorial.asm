main:
; 12: call factorial[10];
        PUSH 10
        CALL p_factorial 1
        DROP
; 13: print rval
        PUSH 0
        LOADM
        PRINT
        HALT

; procedure factorial
p_factorial:
        PUSH 0
; 5: if n = 1 then return 1;
        LOAD 0
        PUSH 1
        EQ
        JZ L1
        PUSH 0
        PUSH 1
        STOREM
        PUSH 0
        RET
L1:
; 6: m is n - 1;
        LOAD 0
        PUSH 1
        SUB
        STORE 1
; 7: call factorial[m];
        LOAD 1
        CALL p_factorial 1
        DROP
; 8: rval is (n * rval)
        PUSH 0
        LOAD 0
        PUSH 0
        LOADM
        MUL
        STOREM
        PUSH 0
        RET
