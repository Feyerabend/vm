main:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_1
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_2
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_3
        SETF
        LOAD 0
        PUSH 3
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 4
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        LOAD 3
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 10
        MUL
        LOAD 2
        LOAD 3
        OVER
        PUSH 0
        GETF
        CALLI 2
        ADD
        DUP
        PRINT
        DROP
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_4
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_5
        SETF
        PUSH 4
        NEW
        DUP
        PUSH 0
        PUSH fun_6
        SETF
        DUP
        PUSH 1
        LOAD 5
        SETF
        DUP
        PUSH 2
        LOAD 4
        SETF
        DUP
        PUSH 3
        OVER
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_7
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_8
        SETF
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_9
        SETF
        LOAD 6
        PUSH 20
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 7
        LOAD 10
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        LOAD 8
        LOAD 10
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        LOAD 7
        LOAD 9
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_10
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 6
        PUSH 10
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
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
        PUSH fun_11
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun p -> ..., capturing: nothing
fun_2:
        LOAD 1
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_12
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun p -> ..., capturing: nothing
fun_3:
        LOAD 1
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_13
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun f -> ..., capturing: nothing
fun_4:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_14
        SETF
        RET

; fun h -> ..., capturing: nothing
fun_5:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_15
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun n -> ..., capturing: cons nil range
fun_6:
        LOAD 1
        PUSH 0
        EQ
        JZ L16
        LOAD 0
        PUSH 2
        GETF
        JMP L17
L16:
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 3
        GETF
        LOAD 1
        PUSH 1
        SUB
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
L17:
        RET

; fun list -> ..., capturing: nothing
fun_7:
        LOAD 1
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_18
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 0
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun list -> ..., capturing: nothing
fun_8:
        LOAD 1
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_19
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 0
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun g -> ..., capturing: nothing
fun_9:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_20
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun x -> ..., capturing: nothing
fun_10:
        LOAD 1
        LOAD 1
        MUL
        RET

; fun b -> ..., capturing: a
fun_11:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_21
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
fun_12:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_22
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun a -> ..., capturing: nothing
fun_13:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_23
        SETF
        RET

; fun z -> ..., capturing: nothing
fun_14:
        LOAD 1
        RET

; fun t -> ..., capturing: h
fun_15:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_24
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

; fun h -> ..., capturing: nothing
fun_18:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_25
        SETF
        DUP
        PUSH 1
        LOAD 1
        SETF
        RET

; fun h -> ..., capturing: nothing
fun_19:
        PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH fun_26
        SETF
        RET

; fun list -> ..., capturing: g
fun_20:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_27
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

; fun f -> ..., capturing: a b
fun_21:
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
fun_22:
        LOAD 0
        PUSH 1
        GETF
        RET

; fun b -> ..., capturing: nothing
fun_23:
        LOAD 1
        RET

; fun f -> ..., capturing: h t
fun_24:
        PUSH 4
        NEW
        DUP
        PUSH 0
        PUSH fun_28
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

; fun acc -> ..., capturing: h
fun_25:
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        ADD
        RET

; fun acc -> ..., capturing: nothing
fun_26:
        LOAD 1
        PUSH 1
        ADD
        RET

; fun f -> ..., capturing: g list
fun_27:
        PUSH 4
        NEW
        DUP
        PUSH 0
        PUSH fun_29
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

; fun z -> ..., capturing: f h t
fun_28:
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 2
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 3
        GETF
        LOAD 0
        PUSH 1
        GETF
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
        RET

; fun z -> ..., capturing: f g list
fun_29:
        LOAD 0
        PUSH 3
        GETF
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_30
        SETF
        DUP
        PUSH 1
        LOAD 0
        PUSH 1
        GETF
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 2
        GETF
        SETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET

; fun h -> ..., capturing: f g
fun_30:
        PUSH 4
        NEW
        DUP
        PUSH 0
        PUSH fun_31
        SETF
        DUP
        PUSH 1
        LOAD 0
        PUSH 1
        GETF
        SETF
        DUP
        PUSH 2
        LOAD 0
        PUSH 2
        GETF
        SETF
        DUP
        PUSH 3
        LOAD 1
        SETF
        RET

; fun acc -> ..., capturing: f g h
fun_31:
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 2
        GETF
        LOAD 0
        PUSH 3
        GETF
        OVER
        PUSH 0
        GETF
        CALLI 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        RET
