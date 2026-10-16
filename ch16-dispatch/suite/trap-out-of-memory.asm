; Keep every block reachable, in a list, until there is no room left.
; Every machine runs out in the end; the specification does not say
; when, only where: at the NEW.
        PUSH 0          ; local 0: the list
loop:   PUSH 2
        NEW
        DUP
        PUSH 1
        LOAD 0
        SETF            ; cell.next = list
        STORE 0
        JMP loop
