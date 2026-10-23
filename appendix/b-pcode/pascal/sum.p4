l 1
 ent 1 l 2
 ent 2 l 3
i   5: read(n);
 lao 9
 lao 5
 csp rdi
i   6: total := 0;
 ldci 0
 sroi 12
i   7: for i := 1 to n do begin
 ldci 1
 sroi 10
 ldoi 9
 sroi 13
l 4
 ldoi 10
 ldoi 13
 leqi
 fjp l 5
i   8: read(x);
 lao 11
 lao 5
 csp rdi
i   9: total := total + x
 ldoi 12
 ldoi 11
 adi
 sroi 12
 ldoi 10
 inci 1
 sroi 10
 ujp l 4
l 5
i  11: writeln('the sum of ', n:1, ' numbers is ', total:1)
 lca'the sum of      '
 ldci 11
 ldci 11
 lao 6
 csp wrs
 ldoi 9
 ldci 1
 lao 6
 csp wri
 lca' numbers is     '
 ldci 12
 ldci 12
 lao 6
 csp wrs
 ldoi 12
 ldci 1
 lao 6
 csp wri
 lao 6
 csp wln
 retp
l 2=14
l 3=4
q
 mst 0
 cup 0 l 1
 stp
q
