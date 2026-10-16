; A linked list of 1 to 5, built from two-field cells (value, next),
; with 0 as the end, then summed.
main:   PUSH 0          ; local 0: the list so far
        PUSH 5          ; local 1: n
build:  LOAD 1
        JZ sum
        PUSH 2
        NEW             ; cell
        DUP
        PUSH 0
        LOAD 1
        SETF            ; cell.value = n
        DUP
        PUSH 1
        LOAD 0
        SETF            ; cell.next = list
        STORE 0         ; list = cell
        LOAD 1
        PUSH 1
        SUB
        STORE 1
        JMP build
sum:    PUSH 0          ; local 2: total
walk:   LOAD 0
        PUSH 0
        EQ
        JZ add
        LOAD 2
        PRINT
        HALT
add:    LOAD 2
        LOAD 0
        PUSH 0
        GETF
        ADD
        STORE 2
        LOAD 0
        PUSH 1
        GETF
        STORE 0
        JMP walk
