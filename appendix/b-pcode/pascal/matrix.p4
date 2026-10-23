l 1
 ent 1 l 2
 ent 2 l 3
i   6: for i := 1 to 3 do
 ldci 1
 sroi 36
 ldci 3
 sroi 39
l 4
 ldoi 36
 ldoi 39
 leqi
 fjp l 5
i   7: for j := 1 to 3 do begin
 ldci 1
 sroi 37
 ldci 3
 sroi 40
l 6
 ldoi 37
 ldoi 40
 leqi
 fjp l 7
i   8: a[i, j] := i + j;
 lao 9
 ldoi 36
 chki 1 3
 deci 1
 ixa 3
 ldoi 37
 chki 1 3
 deci 1
 ixa 1
 ldoi 36
 ldoi 37
 adi
 stoi
i   9: b[i][j] := i * j
 lao 18
 ldoi 36
 chki 1 3
 deci 1
 ixa 3
 ldoi 37
 chki 1 3
 deci 1
 ixa 1
 ldoi 36
 ldoi 37
 mpi
 stoi
 ldoi 37
 inci 1
 sroi 37
 ujp l 6
l 7
 ldoi 36
 inci 1
 sroi 36
 ujp l 4
l 5
i  11: for i := 1 to 3 do
 ldci 1
 sroi 36
 ldci 3
 sroi 41
l 8
 ldoi 36
 ldoi 41
 leqi
 fjp l 9
i  12: for j := 1 to 3 do begin
 ldci 1
 sroi 37
 ldci 3
 sroi 42
l 10
 ldoi 37
 ldoi 42
 leqi
 fjp l 11
i  13: c[i, j] := 0;
 lao 27
 ldoi 36
 chki 1 3
 deci 1
 ixa 3
 ldoi 37
 chki 1 3
 deci 1
 ixa 1
 ldci 0
 stoi
i  14: for k := 1 to 3 do
 ldci 1
 sroi 38
 ldci 3
 sroi 43
l 12
 ldoi 38
 ldoi 43
 leqi
 fjp l 13
i  15: c[i, j] := c[i, j] + a[i, k] * b[k, j]
 lao 27
 ldoi 36
 chki 1 3
 deci 1
 ixa 3
 ldoi 37
 chki 1 3
 deci 1
 ixa 1
 lao 27
 ldoi 36
 chki 1 3
 deci 1
 ixa 3
 ldoi 37
 chki 1 3
 deci 1
 ixa 1
 indi 0
 lao 9
 ldoi 36
 chki 1 3
 deci 1
 ixa 3
 ldoi 38
 chki 1 3
 deci 1
 ixa 1
 indi 0
 lao 18
 ldoi 38
 chki 1 3
 deci 1
 ixa 3
 ldoi 37
 chki 1 3
 deci 1
 ixa 1
 indi 0
 mpi
 adi
 stoi
 ldoi 38
 inci 1
 sroi 38
 ujp l 12
l 13
 ldoi 37
 inci 1
 sroi 37
 ujp l 10
l 11
 ldoi 36
 inci 1
 sroi 36
 ujp l 8
l 9
i  17: a := c;
 lao 9
 lao 27
 mov 9
i  18: for i := 1 to 3 do begin
 ldci 1
 sroi 36
 ldci 3
 sroi 44
l 14
 ldoi 36
 ldoi 44
 leqi
 fjp l 15
i  19: for j := 1 to 3 do write(a[i, j]:5);
 ldci 1
 sroi 37
 ldci 3
 sroi 45
l 16
 ldoi 37
 ldoi 45
 leqi
 fjp l 17
 lao 9
 ldoi 36
 chki 1 3
 deci 1
 ixa 3
 ldoi 37
 chki 1 3
 deci 1
 ixa 1
 indi 0
 ldci 5
 lao 6
 csp wri
 ldoi 37
 inci 1
 sroi 37
 ujp l 16
l 17
i  20: writeln
 lao 6
 csp wln
 ldoi 36
 inci 1
 sroi 36
 ujp l 14
l 15
 retp
l 2=46
l 3=5
q
 mst 0
 cup 0 l 1
 stp
q
