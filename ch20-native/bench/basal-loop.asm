; 2
        PUSH 0
        PUSH 0
        STOREM
; 3
        PUSH 1
        PUSH 1
        STOREM
; 3
L1:
        PUSH 1
        LOADM
        PUSH 300000
        SWAP
        LT
        PUSH 0
        EQ
        JZ L2
; 4
        PUSH 2
        PUSH 1
        LOADM
        PUSH 3
        MUL
        PUSH 2
        PUSH 4
        MUL
        SUB
        PUSH 10
        PUSH 5
        DIV
        ADD
        STOREM
; 5
        PUSH 2
        LOADM
        PUSH 100
        SWAP
        LT
        JZ L3
; 6
        CALL u_ADDIT 0
        DROP
L3:
; 8
        PUSH 1
        PUSH 1
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L1
L2:
; 9
        PUSH 0
        LOADM
        PRINT
; 10
        HALT
; 12
u_ADDIT:
; 13
        PUSH 0
        PUSH 0
        LOADM
        PUSH 2
        LOADM
        PUSH 1000
        DIV
        ADD
        STOREM
; 14
        PUSH 0
        RET
        HALT
