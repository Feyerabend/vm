; Linked lists: cells of two fields, (value, next), with 0 for the
; end. The list 1, 2, ..., 10 is built, printed, reversed by turning
; every next pointer around, and printed again.

main:   PUSH 10
        CALL range 1    ; local 0: the list
        LOAD 0
        CALL show 1
        DROP
        LOAD 0
        CALL reverse 1
        STORE 0
        LOAD 0
        CALL show 1
        DROP
        HALT

; cons(value, next): a new cell
cons:   PUSH 2
        NEW
        DUP
        PUSH 0
        LOAD 0
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; range(n): the list 1, 2, ..., n, built from the back
range:  PUSH 0          ; local 1: the list so far
rnext:  LOAD 0
        JZ rdone
        LOAD 0
        LOAD 1
        CALL cons 2
        STORE 1
        LOAD 0
        PUSH 1
        SUB
        STORE 0
        JMP rnext
rdone:  LOAD 1
        RET

; show(list): print the values on one line, separated by spaces
show:   LOAD 0
        PUSH 0
        EQ
        JZ snext
        PUSH 10
        EMIT
        PUSH 0
        RET
snext:  LOAD 0
        PUSH 0
        GETF
        CALL digits 1
        DROP
        PUSH 32
        EMIT
        LOAD 0
        PUSH 1
        GETF
        STORE 0
        JMP show

; digits(n): write a small positive number without a newline
digits: LOAD 0
        PUSH 10
        LT
        JZ dmore
        LOAD 0
        PUSH 48
        ADD
        EMIT
        PUSH 0
        RET
dmore:  LOAD 0
        PUSH 10
        DIV
        CALL digits 1
        DROP
        LOAD 0
        PUSH 10
        MOD
        PUSH 48
        ADD
        EMIT
        PUSH 0
        RET

; reverse(list): local 1 is what is reversed so far, local 2 the next cell
reverse:
        PUSH 0
        PUSH 0
again:  LOAD 0
        PUSH 0
        EQ
        JZ turn
        LOAD 1
        RET
turn:   LOAD 0
        PUSH 1
        GETF
        STORE 2         ; next = list.next
        LOAD 0
        PUSH 1
        LOAD 1
        SETF            ; list.next = reversed
        LOAD 0
        STORE 1         ; reversed = list
        LOAD 2
        STORE 0         ; list = next
        JMP again
