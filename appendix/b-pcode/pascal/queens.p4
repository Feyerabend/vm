l 2
 ent 1 l 3
 ent 2 l 4
i  14: for k := 1 to 8 do write(row[k]:2);
 ldci 1
 stri 0 5
 ldci 8
 stri 0 6
l 5
 lodi 0 5
 lodi 0 6
 leqi
 fjp l 6
 lao 9
 lodi 0 5
 chki 1 8
 deci 1
 ixa 1
 indi 0
 ldci 2
 lao 6
 csp wri
 lodi 0 5
 inci 1
 stri 0 5
 ujp l 5
l 6
i  15: writeln
 lao 6
 csp wln
 retp
l 3=7
l 4=3
l 7
 ent 1 l 8
 ent 2 l 9
i  21: for r := 1 to 8 do
 ldci 1
 stri 0 6
 ldci 8
 stri 0 7
l 10
 lodi 0 6
 lodi 0 7
 leqi
 fjp l 11
i  22: if free[r] and up[r + column] and down[r - column] then begin
 lao 17
 lodi 0 6
 chki 1 8
 deci 1
 ixa 1
 indb 0
 lao 25
 lodi 0 6
 lodi 0 5
 adi
 chki 2 16
 deci 2
 ixa 1
 indb 0
 and
 lao 40
 lodi 0 6
 lodi 0 5
 sbi
 chki -7 7
 deci -7
 ixa 1
 indb 0
 and
 fjp l 12
i  23: row[column] := r;
 lao 9
 lodi 0 5
 chki 1 8
 deci 1
 ixa 1
 lodi 0 6
 stoi
i  24: free[r] := false; up[r + column] := false; down[r - column] := false;
 lao 17
 lodi 0 6
 chki 1 8
 deci 1
 ixa 1
 ldcb 0
 stob
 lao 25
 lodi 0 6
 lodi 0 5
 adi
 chki 2 16
 deci 2
 ixa 1
 ldcb 0
 stob
 lao 40
 lodi 0 6
 lodi 0 5
 sbi
 chki -7 7
 deci -7
 ixa 1
 ldcb 0
 stob
i  25: if column < 8 then try(column + 1)
 lodi 0 5
 ldci 8
 lesi
 fjp l 14
 mst 1
 lodi 0 5
 ldci 1
 adi
 cup 1 l 7
 ujp l 15
l 14
i  27: solutions := solutions + 1;
 ldoi 56
 ldci 1
 adi
 sroi 56
i  28: if solutions <= 3 then show
 ldoi 56
 ldci 3
 leqi
 fjp l 16
 mst 1
 cup 0 l 2
l 16
l 15
i  30: free[r] := true; up[r + column] := true; down[r - column] := true
 lao 17
 lodi 0 6
 chki 1 8
 deci 1
 ixa 1
 ldcb 1
 stob
 lao 25
 lodi 0 6
 lodi 0 5
 adi
 chki 2 16
 deci 2
 ixa 1
 ldcb 1
 stob
 lao 40
 lodi 0 6
 lodi 0 5
 sbi
 chki -7 7
 deci -7
 ixa 1
 ldcb 1
 stob
l 12
 lodi 0 6
 inci 1
 stri 0 6
 ujp l 10
l 11
 retp
l 8=8
l 9=7
l 1
 ent 1 l 18
 ent 2 l 19
i  35: for i := 1 to 8 do free[i] := true;
 ldci 1
 sroi 55
 ldci 8
 sroi 57
l 20
 ldoi 55
 ldoi 57
 leqi
 fjp l 21
 lao 17
 ldoi 55
 chki 1 8
 deci 1
 ixa 1
 ldcb 1
 stob
 ldoi 55
 inci 1
 sroi 55
 ujp l 20
l 21
i  36: for i := 2 to 16 do up[i] := true;
 ldci 2
 sroi 55
 ldci 16
 sroi 58
l 22
 ldoi 55
 ldoi 58
 leqi
 fjp l 23
 lao 25
 ldoi 55
 chki 2 16
 deci 2
 ixa 1
 ldcb 1
 stob
 ldoi 55
 inci 1
 sroi 55
 ujp l 22
l 23
i  37: for i := -7 to 7 do down[i] := true;
 ldci 7
 ngi
 sroi 55
 ldci 7
 sroi 59
l 24
 ldoi 55
 ldoi 59
 leqi
 fjp l 25
 lao 40
 ldoi 55
 chki -7 7
 deci -7
 ixa 1
 ldcb 1
 stob
 ldoi 55
 inci 1
 sroi 55
 ujp l 24
l 25
i  38: solutions := 0;
 ldci 0
 sroi 56
i  39: try(1);
 mst 0
 ldci 1
 cup 1 l 7
i  40: writeln(solutions:1, ' solutions')
 ldoi 56
 ldci 1
 lao 6
 csp wri
 lca' solutions      '
 ldci 10
 ldci 10
 lao 6
 csp wrs
 lao 6
 csp wln
 retp
l 18=60
l 19=6
q
 mst 0
 cup 0 l 1
 stp
q
