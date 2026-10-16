; PUSH then SUB in an empty frame: the SUB's second pop underflows.
main:   CALL f 0
        HALT
f:      PUSH 1
        SUB
