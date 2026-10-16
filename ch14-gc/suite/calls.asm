; Arguments become locals, deepest first; STORE changes a local;
; RET throws away whatever the call left and returns one value.
main:   PUSH 10
        PUSH 3
        CALL sub 2      ; sub(10, 3)
        PRINT           ; 7
        PUSH 100        ; stays below the call
        PUSH 1
        CALL messy 1
        PRINT           ; 42
        PRINT           ; 100: the caller's value is untouched
        PUSH 5
        CALL twice 1
        PRINT           ; 20
        HALT

sub:    LOAD 0
        LOAD 1
        SUB
        RET

messy:  PUSH 7
        PUSH 8
        PUSH 9          ; leave clutter behind
        PUSH 42
        RET

; twice(x) = double(double(x)), with x overwritten on the way
twice:  LOAD 0
        CALL double 1
        STORE 0
        LOAD 0
        CALL double 1
        RET

double: LOAD 0
        LOAD 0
        ADD
        RET
