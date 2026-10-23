l 2
 ent 1 l 3
 ent 2 l 4
i   6: square := x * x
 lodi 0 5
 lodi 0 5
 mpi
 stri 0 0
 reti
l 3=6
l 4=2
l 1
 ent 1 l 5
 ent 2 l 6
i  10: for i := 1 to 5 do
 ldci 1
 sroi 9
 ldci 5
 sroi 10
l 7
 ldoi 9
 ldoi 10
 leqi
 fjp l 8
i  11: writeln(i:2, square(i):4)
 ldoi 9
 ldci 2
 lao 6
 csp wri
 mst 0
 ldoi 9
 cup 1 l 2
 ldci 4
 lao 6
 csp wri
 lao 6
 csp wln
 ldoi 9
 inci 1
 sroi 9
 ujp l 7
l 8
 retp
l 5=11
l 6=6
q
 mst 0
 cup 0 l 1
 stp
q
