; Strings as blocks of character codes.
;
; A string is a block with one character in each field, so its length
; is LEN. Here one is made, printed, reversed in place, and printed
; again.

main:   PUSH 5
        NEW             ; local 0: s, five characters
        LOAD 0
        PUSH 0
        PUSH 104        ; h
        SETF
        LOAD 0
        PUSH 1
        PUSH 101        ; e
        SETF
        LOAD 0
        PUSH 2
        PUSH 108        ; l
        SETF
        LOAD 0
        PUSH 3
        PUSH 108        ; l
        SETF
        LOAD 0
        PUSH 4
        PUSH 111        ; o
        SETF
        LOAD 0
        CALL print 1
        DROP
        LOAD 0
        CALL reverse 1
        DROP
        LOAD 0
        CALL print 1
        DROP
        HALT

; print(s): write every character of s, then a newline
print:  PUSH 0          ; local 1: i
ploop:  LOAD 1
        LOAD 0
        LEN
        LT              ; i < length ?
        JZ pdone
        LOAD 0
        LOAD 1
        GETF
        EMIT
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        JMP ploop
pdone:  PUSH 10
        EMIT
        PUSH 0
        RET

; reverse(s): swap the first and last characters, and so on inwards
reverse:
        PUSH 0          ; local 1: i, from the front
        LOAD 0
        LEN
        PUSH 1
        SUB             ; local 2: j, from the back
rloop:  LOAD 1
        LOAD 2
        LT              ; i < j ?
        JZ rdone
        LOAD 0
        LOAD 1
        GETF            ; local 3: the character at i
        LOAD 0
        LOAD 1
        LOAD 0
        LOAD 2
        GETF
        SETF            ; s[i] = s[j]
        LOAD 0
        LOAD 2
        LOAD 3
        SETF            ; s[j] = the old s[i]
        DROP
        LOAD 1
        PUSH 1
        ADD
        STORE 1
        LOAD 2
        PUSH 1
        SUB
        STORE 2
        JMP rloop
rdone:  PUSH 0
        RET
