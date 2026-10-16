; A function cannot pop its caller's values.
main:   PUSH 1
        CALL f 0
        HALT
f:      DROP
