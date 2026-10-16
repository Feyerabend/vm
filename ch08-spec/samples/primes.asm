; The primes below 50, by trial division.
;
; Compare with ch05-files/samples/primes.txt: the same program, with
; every address counted by hand.

; main: local 0 is n, counting from 2 up to 49
main:   PUSH 2
next:   LOAD 0
        PUSH 50
        LT
        JZ end
        LOAD 0
        CALL prime 1
        JZ skip
        LOAD 0
        PRINT
skip:   LOAD 0
        PUSH 1
        ADD
        STORE 0
        JMP next
end:    HALT

; prime(n): 1 if n is prime, else 0
; local 0 is n, local 1 is the divisor d, starting at 2
prime:  PUSH 2
test:   LOAD 1
        LOAD 1
        MUL
        LOAD 0
        SWAP
        LT              ; n < d * d ?
        JZ divide
        PUSH 1          ; no divisor up to the square root: prime
        RET
divide: LOAD 0
        LOAD 1
        MOD
        JZ composite    ; d divides n
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP test
composite:
        PUSH 0
        RET
