l 2
 ent 1 l 3
 ent 2 l 4
i   5: if n > 0 then begin
 lodi 0 5
 ldci 0
 grti
 fjp l 5
i   6: move(n - 1, source, spare, target);
 mst 1
 lodi 0 5
 ldci 1
 sbi
 lodc 0 6
 lodc 0 8
 lodc 0 7
 cup 4 l 2
i   7: writeln('disc ', n:1, ' from ', source, ' to ', target);
 lca'disc            '
 ldci 5
 ldci 5
 lao 6
 csp wrs
 lodi 0 5
 ldci 1
 lao 6
 csp wri
 lca' from           '
 ldci 6
 ldci 6
 lao 6
 csp wrs
 lodc 0 6
 ldci 1
 lao 6
 csp wrc
 lca' to             '
 ldci 4
 ldci 4
 lao 6
 csp wrs
 lodc 0 7
 ldci 1
 lao 6
 csp wrc
 lao 6
 csp wln
i   8: move(n - 1, spare, target, source)
 mst 1
 lodi 0 5
 ldci 1
 sbi
 lodc 0 8
 lodc 0 7
 lodc 0 6
 cup 4 l 2
l 5
 retp
l 3=9
l 4=9
l 1
 ent 1 l 7
 ent 2 l 8
i  13: move(3, 'A', 'C', 'B')
 mst 0
 ldci 3
 ldcc 'A'
 ldcc 'C'
 ldcc 'B'
 cup 4 l 2
 retp
l 7=9
l 8=9
q
 mst 0
 cup 0 l 1
 stp
q
