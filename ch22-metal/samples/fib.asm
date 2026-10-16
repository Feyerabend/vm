; fib(20), recursively: 21,891 calls. Calls and returns.
main:   PUSH 20
        CALL fib 1
        PRINT
        HALT
fib:    LOAD 0
        PUSH 2
        LT
        JZ more
        LOAD 0
        RET
more:   LOAD 0
        PUSH 1
        SUB
        CALL fib 1
        LOAD 0
        PUSH 2
        SUB
        CALL fib 1
        ADD
        RET
