; Not a sensible program, and never run: it is here to check that
; the disassembler loses nothing even when the words do not make
; sense as instructions.

        PUSH 1
        .word 99        ; no instruction has code 99
        JMP 1           ; a jump into the middle of PUSH 1
        .word 1         ; PUSH, but its operand is missing
