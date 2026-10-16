; Chapter 15's samples/garbage.lam, with power 18, compiled by lambda.py:
; a quarter of a million closure calls, and a million short-lived blocks.
main:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_1
        SETF
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_2
        SETF
        DUP
        PUSH 1
        LOAD 0
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_3
        SETF
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_4
        SETF
        DUP
        PUSH 1
        OVER
        SETF
        DUP
        PUSH 2
        LOAD 2
        SETF
        LOAD 3
        PUSH 18
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 0
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        SWAP
        DROP
        DROP
        HALT

; fun a -> ..., capturing: nothing
fun_1:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_5
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun x -> ..., capturing: pair
fun_2:
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_6
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun f -> ..., capturing: nothing
fun_3:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_7
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun k -> ..., capturing: power twice
fun_4:
        PUSH 4
        NEW
        DUP
        PUSH 0
        PUSH fun_8
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 1
        GETF
        SETF
        DUP
        PUSH 3
        LOAD 0
        PUSH 2
        GETF
        SETF
        RET

; fun b -> ..., capturing: a
fun_5:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_9
        SETF
        DUP
        PUSH 1
        LOAD 0
        PUSH 1
        GETF
        SETF
        DUP
        PUSH 2
        LOAD 1
        SETF
        RET

; fun a -> ..., capturing: nothing
fun_6:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_10
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun x -> ..., capturing: f
fun_7:
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun f -> ..., capturing: k power twice
fun_8:
        LOAD 0
        PUSH 1
        GETF
        PUSH 0
        EQ
        JZ L11
        LOAD 1
        JMP L12
L11:
        LOAD 0
        PUSH 3
        GETF
        LOAD 0
        PUSH 2
        GETF
        LOAD 0
        PUSH 1
        GETF
        PUSH 1
        SUB
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
L12:
        RET

; fun f -> ..., capturing: a b
fun_9:
        LOAD 1
        LOAD 0
        PUSH 1
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 2
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun b -> ..., capturing: a
fun_10:
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        ADD
        RET
