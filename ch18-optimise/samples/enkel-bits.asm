main:
; 24: call ones[255]; print rval;          { 8 }
        PUSH 255
        CALL p_ones 1
        DROP
        PUSH 0
        LOADM
        PRINT
; 25: call ones[1023 xor 15]; print rval;  { 6 }
        PUSH 1023
        PUSH 15
        XOR
        CALL p_ones 1
        DROP
        PUSH 0
        LOADM
        PRINT
; 26: call binary[10]; emit 10;
        PUSH 10
        CALL p_binary 1
        DROP
        PUSH 10
        EMIT
; 27: call binary[(12 or 3) and 13]; emit 10
        PUSH 12
        PUSH 3
        OR
        PUSH 13
        AND
        CALL p_binary 1
        DROP
        PUSH 10
        EMIT
        HALT

; procedure ones
p_ones:
        PUSH 0
; 8: count is 0;
        PUSH 0
        STORE 1
; 9: while n do                  { a condition can be any value: 0 is false }
L1:
        LOAD 0
        JZ L2
; 11: count is count + (n and 1);
        LOAD 1
        LOAD 0
        PUSH 1
        AND
        ADD
        STORE 1
; 12: n is n / 2
        LOAD 0
        PUSH 2
        DIV
        STORE 0
        JMP L1
L2:
; 14: return count
        PUSH 0
        LOAD 1
        STOREM
        PUSH 0
        RET
        PUSH 0
        RET

; procedure binary
p_binary:
; 19: if n > 1 then call binary[n / 2];
        LOAD 0
        PUSH 1
        SWAP
        LT
        JZ L3
        LOAD 0
        PUSH 2
        DIV
        CALL p_binary 1
        DROP
L3:
; 20: emit (n and 1) + 48
        LOAD 0
        PUSH 1
        AND
        PUSH 48
        ADD
        EMIT
        PUSH 0
        RET
