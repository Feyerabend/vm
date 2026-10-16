; A plain loop, 20 million rounds of arithmetic on locals. Nothing
; but the most common instructions, which is where dispatch shows.
main:   PUSH 20000000   ; local 0: count
        PUSH 0          ; local 1: sum
loop:   LOAD 0
        JZ done
        LOAD 1
        LOAD 0
        PUSH 7
        AND
        ADD
        STORE 1
        LOAD 0
        PUSH 1
        SUB
        STORE 0
        JMP loop
done:   LOAD 1
        PRINT
        HALT
