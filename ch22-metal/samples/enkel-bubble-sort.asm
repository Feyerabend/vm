main:
; 50: A.0 is 90;
        PUSH 1
        PUSH 90
        STOREM
; 51: A.1 is 45;
        PUSH 2
        PUSH 45
        STOREM
; 52: A.2 is 4;
        PUSH 3
        PUSH 4
        STOREM
; 53: A.3 is 56;
        PUSH 4
        PUSH 56
        STOREM
; 54: A.4 is 1;
        PUSH 5
        PUSH 1
        STOREM
; 55: A.5 is 99;
        PUSH 6
        PUSH 99
        STOREM
; 56: A.6 is 8;
        PUSH 7
        PUSH 8
        STOREM
; 57: A.7 is 50;
        PUSH 8
        PUSH 50
        STOREM
; 58: A.8 is 32;
        PUSH 9
        PUSH 32
        STOREM
; 59: A.9 is 10;
        PUSH 10
        PUSH 10
        STOREM
; 61: call write[10];
        PUSH 10
        CALL p_write 1
        DROP
; 62: call bubble[10];
        PUSH 10
        CALL p_bubble 1
        DROP
; 63: call write[10]
        PUSH 10
        CALL p_write 1
        DROP
        HALT

; procedure nl
p_nl:
; 5: emit 10
        PUSH 10
        EMIT
        PUSH 0
        RET

; procedure swap
p_swap:
        PUSH 0
; 11: u is A.a;
        PUSH 1
        LOAD 0
        ADD
        LOADM
        STORE 2
; 12: A.a is A.b;
        PUSH 1
        LOAD 0
        ADD
        PUSH 1
        LOAD 1
        ADD
        LOADM
        STOREM
; 13: A.b is u
        PUSH 1
        LOAD 1
        ADD
        LOAD 2
        STOREM
        PUSH 0
        RET

; procedure write
p_write:
        PUSH 0
; 19: j is 0;
        PUSH 0
        STORE 1
; 20: do
L1:
; 22: print A.j;
        PUSH 1
        LOAD 1
        ADD
        LOADM
        PRINT
; 23: j is j + 1
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        LOAD 1
        LOAD 0
        LT
        PUSH 0
        EQ
        JZ L1
; 26: call nl[]
        CALL p_nl 0
        DROP
        PUSH 0
        RET

; procedure bubble
p_bubble:
        PUSH 0
        PUSH 0
        PUSH 0
; 32: l is n - 1;
        LOAD 0
        PUSH 1
        SUB
        STORE 3
; 33: do
L2:
; 35: k is 0;
        PUSH 0
        STORE 1
; 36: do
L3:
; 38: kk is k + 1;
        LOAD 1
        PUSH 1
        ADD
        STORE 2
; 39: if A.k > A.kk then call swap[k, kk];
        PUSH 1
        LOAD 1
        ADD
        LOADM
        PUSH 1
        LOAD 2
        ADD
        LOADM
        SWAP
        LT
        JZ L4
        LOAD 1
        LOAD 2
        CALL p_swap 2
        DROP
L4:
; 40: k is k + 1
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        LOAD 1
        LOAD 3
        LT
        PUSH 0
        EQ
        JZ L3
; 43: l is l - 1
        LOAD 3
        PUSH 1
        SUB
        STORE 3
        LOAD 3
        PUSH 0
        SWAP
        LT
        PUSH 0
        EQ
        JZ L2
        PUSH 0
        RET
