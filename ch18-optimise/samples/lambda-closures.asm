main:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_1
        SETF
        LOAD 0
        PUSH 5
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        PUSH 10
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_2
        SETF
        LOAD 2
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
        DROP
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_3
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_4
        SETF
        LOAD 3
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 4
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        LOAD 3
        LOAD 4
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        PUSH 100
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_5
        SETF
        DUP
        PUSH 1
        LOAD 5
        SETF
        PUSH 0
        LOAD 6
        PUSH 1
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

; fun x -> ..., capturing: nothing
fun_1:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_6
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun f -> ..., capturing: nothing
fun_2:
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

; fun f -> ..., capturing: nothing
fun_3:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_8
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun x -> ..., capturing: nothing
fun_4:
        PUSH 3
        LOAD 1
        MUL
        RET

; fun x -> ..., capturing: n
fun_5:
        LOAD 1
        LOAD 0
        PUSH 1
        GETF
        ADD
        RET

; fun y -> ..., capturing: x
fun_6:
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        ADD
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

; fun g -> ..., capturing: f
fun_8:
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

; fun x -> ..., capturing: f g
fun_9:
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 2
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
