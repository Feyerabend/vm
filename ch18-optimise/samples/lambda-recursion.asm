main:
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_1
        SETF
        DUP
        PUSH 1
        OVER
        SETF
        LOAD 0
        PUSH 10
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_2
        SETF
        DUP
        PUSH 1
        OVER
        SETF
        LOAD 1
        PUSH 20
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_3
        SETF
        DUP
        PUSH 1
        OVER
        SETF
        LOAD 2
        PUSH 1071
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 462
        OVER
        PUSH 0
        GETF
        CALLI 2
        DUP
        PRINT
        DROP
        PUSH 2
        NEW
        DUP
        PUSH 0
        PUSH fun_4
        SETF
        DUP
        PUSH 1
        OVER
        SETF
        LOAD 3
        PUSH 2
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 3
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

; fun n -> ..., capturing: fact
fun_1:
        LOAD 1
        PUSH 2
        LT
        JZ L5
        PUSH 1
        JMP L6
L5:
        LOAD 1
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        PUSH 1
        SUB
        OVER
        PUSH 0
        GETF
        CALLI 2
        MUL
L6:
        RET

; fun n -> ..., capturing: fib
fun_2:
        LOAD 1
        PUSH 2
        LT
        JZ L7
        LOAD 1
        JMP L8
L7:
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        PUSH 1
        SUB
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        PUSH 2
        SUB
        OVER
        PUSH 0
        GETF
        CALLI 2
        ADD
L8:
        RET

; fun a -> ..., capturing: gcd
fun_3:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_9
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
        RET

; fun m -> ..., capturing: ack
fun_4:
        PUSH 3
        NEW
        DUP
        PUSH 0
        PUSH fun_10
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

; fun b -> ..., capturing: a gcd
fun_9:
        LOAD 1
        PUSH 0
        EQ
        JZ L11
        LOAD 0
        PUSH 1
        GETF
        JMP L12
L11:
        LOAD 0
        PUSH 2
        GETF
        LOAD 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        LOAD 0
        PUSH 1
        GETF
        LOAD 1
        MOD
        OVER
        PUSH 0
        GETF
        CALLI 2
L12:
        RET

; fun n -> ..., capturing: ack m
fun_10:
        LOAD 0
        PUSH 2
        GETF
        PUSH 0
        EQ
        JZ L13
        LOAD 1
        PUSH 1
        ADD
        JMP L14
L13:
        LOAD 1
        PUSH 0
        EQ
        JZ L15
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 2
        GETF
        PUSH 1
        SUB
        OVER
        PUSH 0
        GETF
        CALLI 2
        PUSH 1
        OVER
        PUSH 0
        GETF
        CALLI 2
        JMP L16
L15:
        LOAD 0
        PUSH 1
        GETF
        LOAD 0
        PUSH 2
        GETF
        PUSH 1
        SUB
        OVER
        PUSH 0
        GETF
        CALLI 2
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
L16:
L14:
        RET
