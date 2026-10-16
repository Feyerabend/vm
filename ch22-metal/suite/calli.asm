; CALLI calls an address taken from the stack.
main:   PUSH 3
        PUSH 4
        PUSH add        ; the address of add, as a number
        CALLI 2
        PRINT           ; 7
        PUSH answer
        CALLI 0
        PRINT           ; 42
        PUSH add        ; addresses can be kept like any number
        PUSH 100
        SWAP
        STOREM
        PUSH 5
        PUSH 2
        PUSH 100
        LOADM
        CALLI 2
        PRINT           ; 7
        HALT
add:    LOAD 0
        LOAD 1
        ADD
        RET
answer: PUSH 42
        RET
