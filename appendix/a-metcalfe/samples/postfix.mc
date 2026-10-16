# Infix to postfix: the order of operations a stack machine needs.
#
#   S = E "$"
#   E = T { ( "+" | "-" ) T }
#   T = F { ( "*" | "/" ) F }
#   F = name | number | "(" E ")"
#
# Each rule is a subroutine. A rule ends with the flag set if it
# matched, and clear if it did not.

        call S
        stop

S:      call E
        false S9
        match $
S9:     return

E:      call T
        false E9
E1:     match +
        false E2
        call T
        false E9
        print +
        true E1
E2:     match -
        false E3
        call T
        false E9
        print -
        true E1
E3:     flag true          # no more operators: E has matched
E9:     return

T:      call F
        false T9
T1:     match *
        false T2
        call F
        false T9
        print *
        true T1
T2:     match /
        false T3
        call F
        false T9
        print /
        true T1
T3:     flag true
T9:     return

F:      match ?
        false F1
        print ?
        true F9
F1:     match (
        false F9
        call E
        false F9
        match )
F9:     return
