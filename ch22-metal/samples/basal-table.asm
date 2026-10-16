; 3
        PUSH 0
        PUSH 1
        STOREM
; 3
L1:
        PUSH 0
        LOADM
        PUSH 9
        SWAP
        LT
        PUSH 0
        EQ
        JZ L2
; 4
        PUSH 1
        PUSH 1
        STOREM
; 4
L3:
        PUSH 1
        LOADM
        PUSH 9
        SWAP
        LT
        PUSH 0
        EQ
        JZ L4
; 5
        PUSH 2
        PUSH 0
        LOADM
        PUSH 1
        LOADM
        MUL
        STOREM
; 6
        PUSH 2
        LOADM
        PUSH 10
        LT
        JZ L5
; 7
        PUSH 32
        EMIT
L5:
; 9
        PUSH 2
        LOADM
        CALL print_number 1
        DROP
; 10
        PUSH 32
        EMIT
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
        PUSH 10
        EMIT
; 13
        PUSH 0
        PUSH 0
        LOADM
        PUSH 1
        ADD
        STOREM
        JMP L1
L2:
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
