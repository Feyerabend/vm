; NEW makes a block of zeros; SETF and GETF write and read its fields.
        PUSH 3
        NEW             ; r
        DUP
        LEN
        PRINT           ; 3
        DUP
        PUSH 0
        PUSH 10
        SETF
        DUP
        PUSH 1
        PUSH 20
        SETF
        DUP
        PUSH 2
        PUSH 30
        SETF
        DUP
        PUSH 0
        GETF
        PRINT           ; 10
        DUP
        PUSH 1
        GETF
        PRINT           ; 20
        PUSH 2
        GETF
        PRINT           ; 30
        PUSH 0
        NEW
        LEN
        PRINT           ; 0: an empty block is allowed
        PUSH 5
        NEW
        PUSH 4
        GETF
        PRINT           ; 0: fields start as 0
        HALT
