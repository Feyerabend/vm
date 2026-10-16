; Chapter 10 found a program that wrote one element past the end of
; its array, and nothing noticed. On the heap, something notices.

main:   PUSH 15
        NEW             ; local 0: an array of 15, elements 0 to 14
        PUSH 0          ; local 1: i
loop:   LOAD 1
        PUSH 15
        PUSH 1
        ADD
        LT              ; i < 16: one too many, as in the old sample
        JZ done
        LOAD 0
        LOAD 1
        LOAD 1
        SETF            ; a[i] = i
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP loop
done:   HALT
