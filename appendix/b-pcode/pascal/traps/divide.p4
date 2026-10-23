l 1
 ent 1 l 2
 ent 2 l 3
i   4: a := 7; b := 0;
 ldci 7
 sroi 9
 ldci 0
 sroi 10
i   5: writeln(a div b)
 ldoi 9
 ldoi 10
 dvi
 ldci 11
 lao 6
 csp wri
 lao 6
 csp wln
 retp
l 2=11
l 3=3
q
 mst 0
 cup 0 l 1
 stp
q
