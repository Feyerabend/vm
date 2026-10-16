; References can be kept anywhere a value can: in memory, in locals,
; inside other blocks. JZ does not jump on a reference: it is not 0.
main:   PUSH 1
        NEW
        DUP
        PUSH 0
        PUSH 7
        SETF
        PUSH 100
        SWAP
        STOREM          ; memory[100] = r
        PUSH 100
        LOADM
        PUSH 0
        GETF
        PRINT           ; 7
        PUSH 1
        NEW             ; outer
        DUP
        PUSH 0
        PUSH 100
        LOADM
        SETF            ; outer.0 = r
        PUSH 0
        GETF
        PUSH 0
        GETF
        PRINT           ; 7, through outer
        PUSH 100
        LOADM
        JZ wrong
        PUSH 1
        PRINT           ; 1
        HALT
wrong:  PUSH 0
        PRINT
        HALT
