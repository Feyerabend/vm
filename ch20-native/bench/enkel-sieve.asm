main:
; 9: round is 0;
        PUSH 1
        PUSH 0
        STOREM
; 10: while round < 200 do
L1:
        PUSH 1
        LOADM
        PUSH 200
        LT
        JZ L2
; 12: p is 0;
        PUSH 2
        PUSH 0
        STOREM
; 13: while p < size do
L3:
        PUSH 2
        LOADM
        PUSH 4000
        LT
        JZ L4
; 15: marked.p is 0;
        PUSH 5
        PUSH 2
        LOADM
        ADD
        PUSH 0
        STOREM
; 16: p is p + 1
        PUSH 2
        PUSH 2
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L3
L4:
; 18: count is 0;
        PUSH 4
        PUSH 0
        STOREM
; 19: p is 2;
        PUSH 2
        PUSH 2
        STOREM
; 20: while p < size do
L5:
        PUSH 2
        LOADM
        PUSH 4000
        LT
        JZ L6
; 22: if marked.p = 0 then
        PUSH 5
        PUSH 2
        LOADM
        ADD
        LOADM
        PUSH 0
        EQ
        JZ L7
; 24: count is count + 1;
        PUSH 4
        PUSH 4
        LOADM
        PUSH 1
        ADD
        STOREM
; 25: m is p * p;
        PUSH 3
        PUSH 2
        LOADM
        PUSH 2
        LOADM
        MUL
        STOREM
; 26: if p < size / p then
        PUSH 2
        LOADM
        PUSH 4000
        PUSH 2
        LOADM
        DIV
        LT
        JZ L9
; 27: while m < size do
L11:
        PUSH 3
        LOADM
        PUSH 4000
        LT
        JZ L12
; 29: marked.m is 1;
        PUSH 5
        PUSH 3
        LOADM
        ADD
        PUSH 1
        STOREM
; 30: m is m + p
        PUSH 3
        PUSH 3
        LOADM
        PUSH 2
        LOADM
        ADD
        STOREM
        JMP L11
L12:
L9:
L7:
; 33: p is p + 1
        PUSH 2
        PUSH 2
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L5
L6:
; 35: round is round + 1
        PUSH 1
        PUSH 1
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L1
L2:
; 37: print count
        PUSH 4
        LOADM
        PRINT
        HALT
