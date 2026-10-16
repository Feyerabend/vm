# Ordered choice, and how far undoing goes.
#
#   S = A B "$"
#   A = "a" "c" | "a"
#   B = "c" "b" | "d"
#
# Each alternative is a rule of its own, so that when it fails half
# way, its return puts the input back for the next one. But once A has
# returned with success, nothing can make it try its other way: "a c b"
# is in the language (A as "a", then B as "c b"), and it is not
# accepted, since A takes "a c" first, and B is left with "b".

        call S
        stop

S:      call A
        false S9
        call B
        false S9
        match $
S9:     return

A:      call A1
        true A9
        call A2
A9:     return
A1:     match a
        false A19
        match c
        false A19
        print ac
A19:    return
A2:     match a
        false A29
        print a
A29:    return

B:      call B1
        true B9
        call B2
B9:     return
B1:     match c
        false B19
        match b
        false B19
        print cb
B19:    return
B2:     match d
        false B29
        print d
B29:    return
