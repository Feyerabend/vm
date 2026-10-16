; Refused: the stack is one value deep at 'join' on one path, and two
; on the other. A register machine needs to know which register holds
; the top, and here it cannot.
        PUSH 1
        JZ one
        PUSH 2
        PUSH 3
        JMP join
one:    PUSH 4
join:   PRINT
        HALT
