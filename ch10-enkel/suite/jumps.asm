; JZ jumps on zero only; any other value, negative too, falls through.
        PUSH 0
        JZ a
        PUSH 99
        PRINT
a:      PUSH -1
        JZ b
        PUSH 1
        PRINT           ; 1
b:      PUSH 5
        JZ c
        PUSH 2
        PRINT           ; 2
        JMP c
        PUSH 99
        PRINT
c:      HALT
