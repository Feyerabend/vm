l 2
 ent 1 l 3
 ent 2 l 4
i   6: if n < 2 then fib := n
 lodi 0 5
 ldci 2
 lesi
 fjp l 5
 lodi 0 5
 stri 0 0
 ujp l 6
l 5
i   7: else fib := fib(n - 1) + fib(n - 2)
 mst 1
 lodi 0 5
 ldci 1
 sbi
 cup 1 l 2
 mst 1
 lodi 0 5
 ldci 2
 sbi
 cup 1 l 2
 adi
 stri 0 0
l 6
 reti
l 3=6
l 4=8
l 1
 ent 1 l 7
 ent 2 l 8
i  11: n := 0;
 ldci 0
 sroi 9
i  12: repeat
l 9
i  13: write(fib(n):5);
 mst 0
 ldoi 9
 cup 1 l 2
 ldci 5
 lao 6
 csp wri
i  14: n := n + 1
 ldoi 9
 ldci 1
 adi
 sroi 9
 ldoi 9
 ldci 15
 grti
 fjp l 9
i  16: writeln
 lao 6
 csp wln
 retp
l 7=10
l 8=6
q
 mst 0
 cup 0 l 1
 stp
q
