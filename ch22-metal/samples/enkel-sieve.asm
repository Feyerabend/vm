main:
; 12: p is 2;
        PUSH 1
        PUSH 2
        STOREM
; 13: while p * p < size do
L1:
        PUSH 1
        LOADM
        PUSH 1
        LOADM
        MUL
        PUSH 200
        LT
        JZ L2
; 15: if marked.p = 0 then
        PUSH 4
        PUSH 1
        LOADM
        ADD
        LOADM
        PUSH 0
        EQ
        JZ L3
; 17: m is p * p;
        PUSH 2
        PUSH 1
        LOADM
        PUSH 1
        LOADM
        MUL
        STOREM
; 18: while m < size do
L5:
        PUSH 2
        LOADM
        PUSH 200
        LT
        JZ L6
; 20: marked.m is 1;
        PUSH 4
        PUSH 2
        LOADM
        ADD
        PUSH 1
        STOREM
; 21: m is m + p
        PUSH 2
        PUSH 2
        LOADM
        PUSH 1
        LOADM
        ADD
        STOREM
        JMP L5
L6:
L3:
; 24: p is p + 1
        PUSH 1
        PUSH 1
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L1
L2:
; 27: count is 0;
        PUSH 3
        PUSH 0
        STOREM
; 28: p is 2;
        PUSH 1
        PUSH 2
        STOREM
; 29: while p < size do
L7:
        PUSH 1
        LOADM
        PUSH 200
        LT
        JZ L8
; 31: if marked.p = 0 then
        PUSH 4
        PUSH 1
        LOADM
        ADD
        LOADM
        PUSH 0
        EQ
        JZ L9
; 33: print p;
        PUSH 1
        LOADM
        PRINT
; 34: count is count + 1
        PUSH 3
        PUSH 3
        LOADM
        PUSH 1
        ADD
        STOREM
L9:
; 36: p is p + 1
        PUSH 1
        PUSH 1
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L7
L8:
; 38: print count
        PUSH 3
        LOADM
        PRINT
        HALT
