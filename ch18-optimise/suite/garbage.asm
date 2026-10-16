; Make 100000 blocks of 10 values, keeping none of them. Far more
; than any heap in this book can hold at once, but never more than
; one block is reachable, so a machine that reclaims unreachable
; blocks, as the specification requires, never runs out.
main:   PUSH 100000     ; local 0: count
loop:   LOAD 0
        JZ done
        PUSH 10
        NEW
        DROP
        LOAD 0
        PUSH 1
        SUB
        STORE 0
        JMP loop
done:   PUSH 100
        EMIT
        PUSH 111
        EMIT
        PUSH 110
        EMIT
        PUSH 101
        EMIT
        PUSH 10
        EMIT
        HALT
