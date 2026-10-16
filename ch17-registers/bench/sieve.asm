; The sieve of Eratosthenes up to 60000, ten times over, in one block
; that is cleared between rounds. (Chapter 16's version makes a new
; block every round; the register machine has no garbage collector,
; and would run out of room.)
main:   PUSH 60000
        NEW             ; local 0: marks
        PUSH 10         ; local 1: rounds
round:  LOAD 1
        JZ done
        LOAD 0
        CALL sieve 1
        PRINT
        LOAD 1
        PUSH 1
        SUB
        STORE 1
        JMP round
done:   HALT

; sieve(marks): clear it, then count the primes below its length
sieve:  PUSH 0          ; local 1: i
clear:  LOAD 1
        LOAD 0
        LEN
        LT
        JZ start
        LOAD 0
        LOAD 1
        PUSH 0
        SETF
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP clear
start:  PUSH 2
        STORE 1         ; local 1: p
        PUSH 0          ; local 2: count
outer:  LOAD 1
        LOAD 0
        LEN
        LT
        JZ finish
        LOAD 0
        LOAD 1
        GETF
        JZ prime
        JMP next
prime:  LOAD 2
        PUSH 1
        ADD
        STORE 2
        LOAD 1          ; mark only while p < n / p, so that p * p
        LOAD 0          ; cannot overflow
        LEN
        LOAD 1
        DIV
        LT
        JZ next
        LOAD 1
        LOAD 1
        MUL             ; local 3: m = p * p
inner:  LOAD 3
        LOAD 0
        LEN
        LT
        JZ endin
        LOAD 0
        LOAD 3
        PUSH 1
        SETF
        LOAD 3
        LOAD 1
        ADD
        STORE 3
        JMP inner
endin:  DROP
next:   LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP outer
finish: LOAD 2
        RET
