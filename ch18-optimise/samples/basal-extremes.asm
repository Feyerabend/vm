; 4
        PUSH 0
        PUSH 2147483647
        STOREM
; 5
        PUSH 0
        LOADM
        CALL print_number 1
        DROP
; 6
        PUSH 32
        EMIT
; 7
        PUSH 0
        LOADM
        PUSH 1
        ADD
        CALL print_number 1
        DROP
; 8
        PUSH 32
        EMIT
; 9
        PUSH 0
        PUSH 0
        LOADM
        SUB
        CALL print_number 1
        DROP
; 10
        PUSH 32
        EMIT
; 11
        PUSH 0
        CALL print_number 1
        DROP
; 12
        PUSH 32
        EMIT
; 13
        PUSH 0
        PUSH 7
        SUB
        CALL print_number 1
        DROP
; 14
        PUSH 10
        EMIT
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
