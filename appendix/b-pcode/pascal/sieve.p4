l 1
 ent 1 l 2
 ent 2 l 3
i   7: for i := 2 to n do prime[i] := true;
 ldci 2
 sroi 108
 ldci 100
 sroi 111
l 4
 ldoi 108
 ldoi 111
 leqi
 fjp l 5
 lao 9
 ldoi 108
 chki 2 100
 deci 2
 ixa 1
 ldcb 1
 stob
 ldoi 108
 inci 1
 sroi 108
 ujp l 4
l 5
i   8: i := 2;
 ldci 2
 sroi 108
i   9: while i * i <= n do begin
l 6
 ldoi 108
 ldoi 108
 mpi
 ldci 100
 leqi
 fjp l 7
i  10: if prime[i] then begin
 lao 9
 ldoi 108
 chki 2 100
 deci 2
 ixa 1
 indb 0
 fjp l 8
i  11: j := i * i;
 ldoi 108
 ldoi 108
 mpi
 sroi 109
i  12: while j <= n do begin
l 10
 ldoi 109
 ldci 100
 leqi
 fjp l 11
i  13: prime[j] := false;
 lao 9
 ldoi 109
 chki 2 100
 deci 2
 ixa 1
 ldcb 0
 stob
i  14: j := j + i
 ldoi 109
 ldoi 108
 adi
 sroi 109
 ujp l 10
l 11
l 8
i  17: i := i + 1
 ldoi 108
 ldci 1
 adi
 sroi 108
 ujp l 6
l 7
i  19: count := 0;
 ldci 0
 sroi 110
i  20: for i := 2 to n do
 ldci 2
 sroi 108
 ldci 100
 sroi 112
l 12
 ldoi 108
 ldoi 112
 leqi
 fjp l 13
i  21: if prime[i] then begin
 lao 9
 ldoi 108
 chki 2 100
 deci 2
 ixa 1
 indb 0
 fjp l 14
i  22: write(i:4);
 ldoi 108
 ldci 4
 lao 6
 csp wri
i  23: count := count + 1;
 ldoi 110
 ldci 1
 adi
 sroi 110
i  24: if count mod 10 = 0 then writeln
 ldoi 110
 ldci 10
 mod
 ldci 0
 equi
 fjp l 16
 lao 6
 csp wln
l 16
l 14
 ldoi 108
 inci 1
 sroi 108
 ujp l 12
l 13
i  26: writeln;
 lao 6
 csp wln
i  27: writeln(count:1, ' primes')
 ldoi 110
 ldci 1
 lao 6
 csp wri
 lca' primes         '
 ldci 7
 ldci 7
 lao 6
 csp wrs
 lao 6
 csp wln
 retp
l 2=113
l 3=4
q
 mst 0
 cup 0 l 1
 stp
q
