; Euclid's algorithm.

main:   PUSH 1071
        PUSH 462
        CALL gcd 2
        PRINT
        PUSH 17
        PUSH 5
        CALL gcd 2
        PRINT
        HALT

; gcd(a, b): local 0 is a, local 1 is b
gcd:    LOAD 1
        JZ done         ; gcd(a, 0) = a
        LOAD 1
        LOAD 0
        LOAD 1
        MOD
        CALL gcd 2      ; gcd(b, a mod b)
        RET
done:   LOAD 0
        RET
