l 3
 ent 1 l 4
 ent 2 l 5
i  11: if k > 0 then begin
 lodi 1 5
 ldci 0
 grti
 fjp l 6
i  12: writeln(k:1);
 lodi 1 5
 ldci 1
 lao 6
 csp wri
 lao 6
 csp wln
i  13: total := total + k;
 ldoi 9
 lodi 1 5
 adi
 sroi 9
i  14: k := k - 1;
 lodi 1 5
 ldci 1
 sbi
 stri 1 5
i  15: down
 mst 1
 cup 0 l 3
l 6
 retp
l 4=5
l 5=5
l 2
 ent 1 l 8
 ent 2 l 9
i  20: k := 5;
 ldci 5
 stri 0 5
i  21: down
 mst 0
 cup 0 l 3
 retp
l 8=6
l 9=5
l 1
 ent 1 l 10
 ent 2 l 11
i  25: total := 0;
 ldci 0
 sroi 9
i  26: outer;
 mst 0
 cup 0 l 2
i  27: writeln(total:1)
 ldoi 9
 ldci 1
 lao 6
 csp wri
 lao 6
 csp wln
 retp
l 10=10
l 11=5
q
 mst 0
 cup 0 l 1
 stp
q
