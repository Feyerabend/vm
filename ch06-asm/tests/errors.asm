; Every line below the first is wrong in some way the assembler
; must notice. The test checks that it reports all of them.

start:  PUSH 1
        PUSH
        PUSH 1 2
        PUSH ten
        JUMP start
        JMP nowhere
        LOAD -1
        CALL start
start:  HALT
        .word
        PUSH 99999999999
