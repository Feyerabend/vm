l 1
 ent 1 l 2
 ent 2 l 3
i   4: for i := 1 to 4 do
 ldci 1
 sroi 9
 ldci 4
 sroi 10
l 4
 ldoi 9
 ldoi 10
 leqi
 fjp l 5
i   5: case i of
 ldoi 9
 ujp l 6
l 8
i   6: 1, 2: writeln('small');
 lca'small           '
 ldci 5
 ldci 5
 lao 6
 csp wrs
 lao 6
 csp wln
 ujp l 7
l 9
i   7: 4: writeln('four')
 lca'four            '
 ldci 4
 ldci 4
 lao 6
 csp wrs
 lao 6
 csp wln
 ujp l 7
l 6
 chki 1 4
 deci 1
 xjp l 10
l 10
 ujp l 8
 ujp l 8
 ujc
 ujp l 9
l 7
 ldoi 9
 inci 1
 sroi 9
 ujp l 4
l 5
 retp
l 2=11
l 3=5
q
 mst 0
 cup 0 l 1
 stp
q
