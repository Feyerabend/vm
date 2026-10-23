l 2
 ent 1 l 3
 ent 2 l 4
i  11: t := x; x := y; y := t
 loda 0 5
 indi 0
 stri 0 7
 loda 0 5
 loda 0 6
 indi 0
 stoi
 loda 0 6
 lodi 0 7
 stoi
 retp
l 3=8
l 4=2
l 5
 ent 1 l 6
 ent 2 l 7
i  17: for i := 1 to 7 do
 ldci 1
 stri 0 6
 ldci 7
 stri 0 8
l 8
 lodi 0 6
 lodi 0 8
 leqi
 fjp l 9
i  18: for j := 8 downto i + 1 do
 ldci 8
 stri 0 7
 lodi 0 6
 ldci 1
 adi
 stri 0 9
l 10
 lodi 0 7
 lodi 0 9
 geqi
 fjp l 11
i  19: if a[j] < a[j - 1] then swap(a[j], a[j - 1])
 loda 0 5
 lodi 0 7
 chki 1 8
 deci 1
 ixa 1
 indi 0
 loda 0 5
 lodi 0 7
 ldci 1
 sbi
 chki 1 8
 deci 1
 ixa 1
 indi 0
 lesi
 fjp l 12
 mst 1
 loda 0 5
 lodi 0 7
 chki 1 8
 deci 1
 ixa 1
 loda 0 5
 lodi 0 7
 ldci 1
 sbi
 chki 1 8
 deci 1
 ixa 1
 cup 2 l 2
l 12
 lodi 0 7
 deci 1
 stri 0 7
 ujp l 10
l 11
 lodi 0 6
 inci 1
 stri 0 6
 ujp l 8
l 9
 retp
l 6=10
l 7=9
l 14
 ent 1 l 15
 ent 2 l 16
i  25: for i := 1 to 8 do write(a[i]:4);
 ldci 1
 stri 0 6
 ldci 8
 stri 0 7
l 17
 lodi 0 6
 lodi 0 7
 leqi
 fjp l 18
 loda 0 5
 lodi 0 6
 chki 1 8
 deci 1
 ixa 1
 indi 0
 ldci 4
 lao 6
 csp wri
 lodi 0 6
 inci 1
 stri 0 6
 ujp l 17
l 18
i  26: writeln
 lao 6
 csp wln
 retp
l 15=8
l 16=3
l 1
 ent 1 l 19
 ent 2 l 20
i  30: a[1] := 31; a[2] := 4; a[3] := 15; a[4] := -9;
 lao 9
 ldci 1
 chki 1 8
 deci 1
 ixa 1
 ldci 31
 stoi
 lao 9
 ldci 2
 chki 1 8
 deci 1
 ixa 1
 ldci 4
 stoi
 lao 9
 ldci 3
 chki 1 8
 deci 1
 ixa 1
 ldci 15
 stoi
 lao 9
 ldci 4
 chki 1 8
 deci 1
 ixa 1
 ldci 9
 ngi
 stoi
i  31: a[5] := 26; a[6] := 5; a[7] := 3; a[8] := 0;
 lao 9
 ldci 5
 chki 1 8
 deci 1
 ixa 1
 ldci 26
 stoi
 lao 9
 ldci 6
 chki 1 8
 deci 1
 ixa 1
 ldci 5
 stoi
 lao 9
 ldci 7
 chki 1 8
 deci 1
 ixa 1
 ldci 3
 stoi
 lao 9
 ldci 8
 chki 1 8
 deci 1
 ixa 1
 ldci 0
 stoi
i  32: show(a);
 mst 0
 lao 9
 cup 1 l 14
i  33: sort(a);
 mst 0
 lao 9
 cup 1 l 5
i  34: show(a)
 mst 0
 lao 9
 cup 1 l 14
 retp
l 19=18
l 20=6
q
 mst 0
 cup 0 l 1
 stp
q
