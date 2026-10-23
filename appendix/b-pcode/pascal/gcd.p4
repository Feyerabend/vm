l 2
 ent 1 l 3
 ent 2 l 4
i   5: if b = 0 then gcd := a
 lodi 0 6
 ldci 0
 equi
 fjp l 5
 lodi 0 5
 stri 0 0
 ujp l 6
l 5
i   6: else gcd := gcd(b, a mod b)
 mst 1
 lodi 0 6
 lodi 0 5
 lodi 0 6
 mod
 cup 2 l 2
 stri 0 0
l 6
 reti
l 3=7
l 4=8
l 1
 ent 1 l 7
 ent 2 l 8
i  10: writeln(gcd(12, 18):4, gcd(17, 5):4, gcd(1071, 462):4, gcd(0, 7):4)
 mst 0
 ldci 12
 ldci 18
 cup 2 l 2
 ldci 4
 lao 6
 csp wri
 mst 0
 ldci 17
 ldci 5
 cup 2 l 2
 ldci 4
 lao 6
 csp wri
 mst 0
 ldci 1071
 ldci 462
 cup 2 l 2
 ldci 4
 lao 6
 csp wri
 mst 0
 ldci 0
 ldci 7
 cup 2 l 2
 ldci 4
 lao 6
 csp wri
 lao 6
 csp wln
 retp
l 7=9
l 8=7
q
 mst 0
 cup 0 l 1
 stp
q
