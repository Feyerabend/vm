; 11
        PUSH 84
        EMIT
        PUSH 104
        EMIT
        PUSH 105
        EMIT
        PUSH 110
        EMIT
        PUSH 107
        EMIT
        PUSH 32
        EMIT
        PUSH 111
        EMIT
        PUSH 102
        EMIT
        PUSH 32
        EMIT
        PUSH 97
        EMIT
        PUSH 32
        EMIT
        PUSH 110
        EMIT
        PUSH 117
        EMIT
        PUSH 109
        EMIT
        PUSH 98
        EMIT
        PUSH 101
        EMIT
        PUSH 114
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
; 13
        PUSH 0
        PUSH 512
        STOREM
; 14
        PUSH 0
        LOADM
        PUSH 0
        LT
        JZ L1
; 15
        PUSH 0
        PUSH 0
        STOREM
L1:
; 17
        PUSH 0
        LOADM
        PUSH 4095
        SWAP
        LT
        JZ L3
; 18
        PUSH 0
        PUSH 4095
        STOREM
L3:
; 22
        CALL u_RANDOM 0
        DROP
; 23
        PUSH 1
        PUSH 0
        LOADM
        PUSH 10
        DIV
        PUSH 10
        MUL
        STOREM
; 24
        PUSH 2
        PUSH 0
        LOADM
        PUSH 1
        LOADM
        SUB
        STOREM
; 25
        CALL u_RANDOM 0
        DROP
; 26
        PUSH 3
        PUSH 0
        LOADM
        PUSH 10
        DIV
        PUSH 10
        MUL
        STOREM
; 27
        PUSH 4
        PUSH 0
        LOADM
        PUSH 3
        LOADM
        SUB
        STOREM
; 28
        PUSH 5
        PUSH 0
        STOREM
; 31
u_AGAIN:
; 32
        PUSH 87
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 114
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 105
        EMIT
        PUSH 115
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 104
        EMIT
        PUSH 117
        EMIT
        PUSH 114
        EMIT
        PUSH 107
        EMIT
        PUSH 108
        EMIT
        PUSH 101
        EMIT
        PUSH 63
        EMIT
        PUSH 32
        EMIT
        PUSH 69
        EMIT
        PUSH 110
        EMIT
        PUSH 116
        EMIT
        PUSH 101
        EMIT
        PUSH 114
        EMIT
        PUSH 32
        EMIT
        PUSH 99
        EMIT
        PUSH 111
        EMIT
        PUSH 108
        EMIT
        PUSH 117
        EMIT
        PUSH 109
        EMIT
        PUSH 110
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 110
        EMIT
        PUSH 32
        EMIT
        PUSH 114
        EMIT
        PUSH 111
        EMIT
        PUSH 119
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
; 34
        PUSH 6
        PUSH 2
        STOREM
; 35
        PUSH 7
        PUSH 1
        STOREM
; 37
        PUSH 6
        LOADM
        PUSH 0
        LT
        PUSH 0
        EQ
        JZ L5
; 38
        PUSH 6
        LOADM
        PUSH 9
        SWAP
        LT
        PUSH 0
        EQ
        JZ L7
; 39
        PUSH 7
        LOADM
        PUSH 0
        LT
        PUSH 0
        EQ
        JZ L9
; 40
        PUSH 7
        LOADM
        PUSH 9
        SWAP
        LT
        PUSH 0
        EQ
        JZ L11
; 41
        JMP u_PROCESS
L11:
L9:
L7:
L5:
; 46
        PUSH 84
        EMIT
        PUSH 104
        EMIT
        PUSH 97
        EMIT
        PUSH 116
        EMIT
        PUSH 32
        EMIT
        PUSH 108
        EMIT
        PUSH 111
        EMIT
        PUSH 99
        EMIT
        PUSH 97
        EMIT
        PUSH 116
        EMIT
        PUSH 105
        EMIT
        PUSH 111
        EMIT
        PUSH 110
        EMIT
        PUSH 32
        EMIT
        PUSH 105
        EMIT
        PUSH 115
        EMIT
        PUSH 32
        EMIT
        PUSH 111
        EMIT
        PUSH 102
        EMIT
        PUSH 102
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 103
        EMIT
        PUSH 114
        EMIT
        PUSH 105
        EMIT
        PUSH 100
        EMIT
        PUSH 33
        EMIT
        PUSH 10
        EMIT
; 47
        JMP u_AGAIN
; 50
u_PROCESS:
; 51
        PUSH 5
        PUSH 5
        LOADM
        PUSH 1
        ADD
        STOREM
; 52
        PUSH 84
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 72
        EMIT
        PUSH 117
        EMIT
        PUSH 114
        EMIT
        PUSH 107
        EMIT
        PUSH 108
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 105
        EMIT
        PUSH 115
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
; 53
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        LT
        JZ L13
; 54
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        LT
        JZ L15
; 55
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 110
        EMIT
        PUSH 111
        EMIT
        PUSH 114
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 119
        EMIT
        PUSH 101
        EMIT
        PUSH 115
        EMIT
        PUSH 116
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L15:
L13:
; 58
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        EQ
        JZ L17
; 59
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        LT
        JZ L19
; 60
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 110
        EMIT
        PUSH 111
        EMIT
        PUSH 114
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L19:
L17:
; 63
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        SWAP
        LT
        JZ L21
; 64
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        LT
        JZ L23
; 65
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 110
        EMIT
        PUSH 111
        EMIT
        PUSH 114
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 97
        EMIT
        PUSH 115
        EMIT
        PUSH 116
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L23:
L21:
; 68
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        SWAP
        LT
        JZ L25
; 69
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        EQ
        JZ L27
; 70
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 101
        EMIT
        PUSH 97
        EMIT
        PUSH 115
        EMIT
        PUSH 116
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L27:
L25:
; 73
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        SWAP
        LT
        JZ L29
; 74
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        SWAP
        LT
        JZ L31
; 75
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 115
        EMIT
        PUSH 111
        EMIT
        PUSH 117
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 97
        EMIT
        PUSH 115
        EMIT
        PUSH 116
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L31:
L29:
; 78
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        EQ
        JZ L33
; 79
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        SWAP
        LT
        JZ L35
; 80
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 115
        EMIT
        PUSH 111
        EMIT
        PUSH 117
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L35:
L33:
; 83
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        LT
        JZ L37
; 84
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        SWAP
        LT
        JZ L39
; 85
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 115
        EMIT
        PUSH 111
        EMIT
        PUSH 117
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 119
        EMIT
        PUSH 101
        EMIT
        PUSH 115
        EMIT
        PUSH 116
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L39:
L37:
; 88
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        LT
        JZ L41
; 89
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        EQ
        JZ L43
; 90
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 119
        EMIT
        PUSH 101
        EMIT
        PUSH 115
        EMIT
        PUSH 116
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
L43:
L41:
; 93
        PUSH 2
        LOADM
        PUSH 6
        LOADM
        EQ
        JZ L45
; 94
        PUSH 4
        LOADM
        PUSH 7
        LOADM
        EQ
        JZ L47
; 95
        JMP u_RIGHT
L47:
L45:
; 98
        PUSH 5
        LOADM
        PUSH 6
        SWAP
        LT
        JZ L49
; 99
        JMP u_TOOLONG
L49:
; 101
        PUSH 89
        EMIT
        PUSH 111
        EMIT
        PUSH 117
        EMIT
        PUSH 32
        EMIT
        PUSH 104
        EMIT
        PUSH 97
        EMIT
        PUSH 118
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 97
        EMIT
        PUSH 107
        EMIT
        PUSH 101
        EMIT
        PUSH 110
        EMIT
        PUSH 32
        EMIT
; 102
        PUSH 5
        LOADM
        CALL print_number 1
        DROP
; 103
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 117
        EMIT
        PUSH 114
        EMIT
        PUSH 110
        EMIT
        PUSH 115
        EMIT
        PUSH 32
        EMIT
        PUSH 115
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 102
        EMIT
        PUSH 97
        EMIT
        PUSH 114
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
; 104
        JMP u_AGAIN
; 108
u_RIGHT:
; 109
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 46
        EMIT
        PUSH 82
        EMIT
        PUSH 73
        EMIT
        PUSH 71
        EMIT
        PUSH 72
        EMIT
        PUSH 84
        EMIT
        PUSH 32
        EMIT
        PUSH 72
        EMIT
        PUSH 69
        EMIT
        PUSH 82
        EMIT
        PUSH 69
        EMIT
        PUSH 33
        EMIT
        PUSH 10
        EMIT
; 110
        PUSH 89
        EMIT
        PUSH 111
        EMIT
        PUSH 117
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 111
        EMIT
        PUSH 107
        EMIT
        PUSH 32
        EMIT
; 111
        PUSH 5
        LOADM
        CALL print_number 1
        DROP
; 112
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 117
        EMIT
        PUSH 114
        EMIT
        PUSH 110
        EMIT
        PUSH 115
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 102
        EMIT
        PUSH 105
        EMIT
        PUSH 110
        EMIT
        PUSH 100
        EMIT
        PUSH 32
        EMIT
        PUSH 105
        EMIT
        PUSH 116
        EMIT
        PUSH 46
        EMIT
        PUSH 10
        EMIT
; 113
        HALT
; 117
u_TOOLONG:
; 118
        PUSH 89
        EMIT
        PUSH 111
        EMIT
        PUSH 117
        EMIT
        PUSH 32
        EMIT
        PUSH 104
        EMIT
        PUSH 97
        EMIT
        PUSH 118
        EMIT
        PUSH 101
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 97
        EMIT
        PUSH 107
        EMIT
        PUSH 101
        EMIT
        PUSH 110
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 111
        EMIT
        PUSH 111
        EMIT
        PUSH 32
        EMIT
        PUSH 108
        EMIT
        PUSH 111
        EMIT
        PUSH 110
        EMIT
        PUSH 103
        EMIT
        PUSH 32
        EMIT
        PUSH 111
        EMIT
        PUSH 118
        EMIT
        PUSH 101
        EMIT
        PUSH 114
        EMIT
        PUSH 32
        EMIT
        PUSH 116
        EMIT
        PUSH 104
        EMIT
        PUSH 105
        EMIT
        PUSH 115
        EMIT
        PUSH 46
        EMIT
        PUSH 32
        EMIT
        PUSH 89
        EMIT
        PUSH 111
        EMIT
        PUSH 117
        EMIT
        PUSH 32
        EMIT
        PUSH 108
        EMIT
        PUSH 111
        EMIT
        PUSH 115
        EMIT
        PUSH 101
        EMIT
        PUSH 33
        EMIT
        PUSH 10
        EMIT
; 119
        HALT
; 125
u_RANDOM:
; 126
        PUSH 0
        PUSH 5
        PUSH 0
        LOADM
        MUL
        PUSH 35
        ADD
        STOREM
; 127
        PUSH 8
        PUSH 0
        LOADM
        PUSH 4096
        DIV
        STOREM
; 128
        PUSH 0
        PUSH 0
        LOADM
        PUSH 8
        LOADM
        PUSH 4096
        MUL
        SUB
        STOREM
; 129
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
