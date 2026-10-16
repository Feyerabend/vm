; 3
        PUSH 0
        PUSH 10
        STOREM
; 3
L1:
        PUSH 0
        LOADM
        PUSH 0
        LT
        PUSH 0
        EQ
        JZ L2
; 4
        PUSH 0
        LOADM
        CALL print_number 1
        DROP
; 5
        PUSH 32
        EMIT
; 6
        PUSH 0
        PUSH 0
        LOADM
        PUSH 0
        PUSH 2
        SUB
        ADD
        STOREM
        JMP L1
L2:
; 7
        PUSH 10
        EMIT
; 9
        PUSH 1
        PUSH 1
        STOREM
; 9
L3:
        PUSH 1
        LOADM
        PUSH 3
        SWAP
        LT
        PUSH 0
        EQ
        JZ L4
; 10
        PUSH 1
        LOADM
        PUSH 1
        EQ
        JZ L5
; 10
        CALL u_ONE 0
        DROP
L5:
; 10
        PUSH 1
        LOADM
        PUSH 2
        EQ
        JZ L7
; 10
        CALL u_TWO 0
        DROP
L7:
; 10
        PUSH 1
        LOADM
        PUSH 3
        EQ
        JZ L9
; 10
        CALL u_THREE 0
        DROP
L9:
; 11
        PUSH 1
        PUSH 1
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L3
L4:
; 12
        PUSH 100
        EMIT
        PUSH 111
        EMIT
        PUSH 110
        EMIT
        PUSH 101
        EMIT
        PUSH 10
        EMIT
; 13
        HALT
; 15
u_ONE:
; 16
        PUSH 111
        EMIT
        PUSH 110
        EMIT
        PUSH 101
        EMIT
        PUSH 10
        EMIT
; 17
        PUSH 0
        RET
; 19
u_TWO:
; 20
        PUSH 116
        EMIT
        PUSH 119
        EMIT
        PUSH 111
        EMIT
        PUSH 10
        EMIT
; 21
        PUSH 0
        RET
; 23
u_THREE:
; 24
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 114
        EMIT
        PUSH 101
        EMIT
        PUSH 101
        EMIT
        PUSH 10
        EMIT
; 25
        PUSH 0
        RET
        HALT

; run-time library: print_number(n) prints n with no newline
print_number:
        LOAD 0
        PUSH 0
        LT
        JZ print_negate
        PUSH 45                 ; '-'
        EMIT
        LOAD 0                  ; n is already negative
        JMP print_digits_of
print_negate:
        PUSH 0
        LOAD 0
        SUB                     ; -n
print_digits_of:
        CALL print_digits 1
        RET

; print_digits(m), for m <= 0, prints the digits of -m
print_digits:
        LOAD 0
        PUSH -9
        LT                      ; m < -9: more than one digit
        JZ print_last
        LOAD 0
        PUSH 10
        DIV
        CALL print_digits 1     ; all digits but the last
        DROP
print_last:
        PUSH 48                 ; '0'
        PUSH 0
        LOAD 0
        PUSH 10
        MOD
        SUB                     ; -(m mod 10), from 0 to 9
        ADD
        EMIT
        PUSH 0
        RET
