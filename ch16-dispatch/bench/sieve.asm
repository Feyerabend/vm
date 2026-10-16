; The sieve of Eratosthenes on the heap, up to 60000, ten times over:
; GETF and SETF, and a fresh block each time for the collector.
main:   PUSH 10         ; local 0: rounds
round:  LOAD 0
        JZ done
        PUSH 60000
        CALL sieve 1
        PRINT
        LOAD 0
        PUSH 1
        SUB
        STORE 0
        JMP round
done:   HALT

; sieve(n): the number of primes below n
sieve:  LOAD 0
        NEW             ; local 1: marks
        PUSH 2          ; local 2: p
        PUSH 0          ; local 3: count
outer:  LOAD 2
        LOAD 0
        LT
        JZ finish
        LOAD 1
        LOAD 2
        GETF
        JZ prime
        JMP next
prime:  LOAD 3
        PUSH 1
        ADD
        STORE 3
        LOAD 2          ; mark only while p < n / p: p * p itself
        LOAD 0          ; would overflow 32 bits for large p, wrap
        LOAD 2          ; negative, and pass the test below
        DIV
        LT
        JZ next
        LOAD 2
        LOAD 2
        MUL             ; local 4: m = p * p
inner:  LOAD 4
        LOAD 0
        LT
        JZ endin
        LOAD 1
        LOAD 4
        PUSH 1
        SETF
        LOAD 4
        LOAD 2
        ADD
        STORE 4
        JMP inner
endin:  DROP
next:   LOAD 2
        PUSH 1
        ADD
        STORE 2
        JMP outer
finish: LOAD 3
        RET
