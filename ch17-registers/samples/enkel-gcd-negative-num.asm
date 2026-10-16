main:
; 20: call gcd[1071, 462];
        PUSH 1071
        PUSH 462
        CALL p_gcd 2
        DROP
; 21: print rval
        PUSH 0
        LOADM
        PRINT
        HALT

; procedure max
p_max:
; 4: if a > b then return a;
        LOAD 0
        LOAD 1
        SWAP
        LT
        JZ L1
        PUSH 0
        LOAD 0
        STOREM
        PUSH 0
        RET
L1:
; 5: return b
        PUSH 0
        LOAD 1
        STOREM
        PUSH 0
        RET
        PUSH 0
        RET

; procedure gcd
p_gcd:
        PUSH 0
; 11: c is -a;
        PUSH 0
        LOAD 0
        SUB
        STORE 2
; 12: call max[a, c];
        LOAD 0
        LOAD 2
        CALL p_max 2
        DROP
; 13: a is rval;
        PUSH 0
        LOADM
        STORE 0
; 14: if b = 0 then return a;
        LOAD 1
        PUSH 0
        EQ
        JZ L3
        PUSH 0
        LOAD 0
        STOREM
        PUSH 0
        RET
L3:
; 15: c is a % b;
        LOAD 0
        LOAD 1
        MOD
        STORE 2
; 16: call gcd[b, c]
        LOAD 1
        LOAD 2
        CALL p_gcd 2
        DROP
        PUSH 0
        RET
