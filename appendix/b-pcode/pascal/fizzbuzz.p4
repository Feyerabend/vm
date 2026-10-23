l 1
 ent 1 l 2
 ent 2 l 3
i   5: for i := 1 to 20 do
 ldci 1
 sroi 9
 ldci 20
 sroi 10
l 4
 ldoi 9
 ldoi 10
 leqi
 fjp l 5
i   6: case i mod 15 of
 ldoi 9
 ldci 15
 mod
 ujp l 6
l 8
i   7: 0: writeln('FizzBuzz');
 lca'FizzBuzz        '
 ldci 8
 ldci 8
 lao 6
 csp wrs
 lao 6
 csp wln
 ujp l 7
l 9
i   8: 3, 6, 9, 12: writeln('Fizz');
 lca'Fizz            '
 ldci 4
 ldci 4
 lao 6
 csp wrs
 lao 6
 csp wln
 ujp l 7
l 10
i   9: 5, 10: writeln('Buzz');
 lca'Buzz            '
 ldci 4
 ldci 4
 lao 6
 csp wrs
 lao 6
 csp wln
 ujp l 7
l 11
i  10: 1, 2, 4, 7, 8, 11, 13, 14: writeln(i:1)
 ldoi 9
 ldci 1
 lao 6
 csp wri
 lao 6
 csp wln
 ujp l 7
l 6
 chki 0 14
 xjp l 12
l 12
 ujp l 8
 ujp l 11
 ujp l 11
 ujp l 9
 ujp l 11
 ujp l 10
 ujp l 9
 ujp l 11
 ujp l 11
 ujp l 9
 ujp l 10
 ujp l 11
 ujp l 9
 ujp l 11
 ujp l 11
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
