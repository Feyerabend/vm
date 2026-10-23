l 1
 ent 1 l 2
 ent 2 l 3
i   5: for c := 'a' to 'z' do write(c);
 ldcc 'a'
 sroc 9
 ldcc 'z'
 sroc 11
l 4
 ldoc 9
 ldoc 11
 leqc
 fjp l 5
 ldoc 9
 ldci 1
 lao 6
 csp wrc
 ldoc 9
 ord
 inci 1
 chr
 sroc 9
 ujp l 4
l 5
i   6: writeln;
 lao 6
 csp wln
i   7: for c := 'Z' downto 'A' do write(c);
 ldcc 'Z'
 sroc 9
 ldcc 'A'
 sroc 12
l 6
 ldoc 9
 ldoc 12
 geqc
 fjp l 7
 ldoc 9
 ldci 1
 lao 6
 csp wrc
 ldoc 9
 ord
 deci 1
 chr
 sroc 9
 ujp l 6
l 7
i   8: writeln;
 lao 6
 csp wln
i   9: writeln(ord('A'):1, ' ', chr(97), ' ', succ('m'), pred('n'), ' ', ord(true):1);
 ldcc 'A'
 ord
 ldci 1
 lao 6
 csp wri
 ldcc ' '
 ldci 1
 lao 6
 csp wrc
 ldci 97
 chr
 ldci 1
 lao 6
 csp wrc
 ldcc ' '
 ldci 1
 lao 6
 csp wrc
 ldcc 'm'
 ord
 inci 1
 chr
 ldci 1
 lao 6
 csp wrc
 ldcc 'n'
 ord
 deci 1
 chr
 ldci 1
 lao 6
 csp wrc
 ldcc ' '
 ldci 1
 lao 6
 csp wrc
 ldcb 1
 ord
 ldci 1
 lao 6
 csp wri
 lao 6
 csp wln
i  10: b := 'a' < 'b';
 ldcc 'a'
 ldcc 'b'
 lesc
 srob 10
i  11: writeln(b, ' ', not b, ' ', odd(7):6, '|', 'x':3, '|', '''quoted''');
 ldob 10
 fjp l 8
 lca'true            '
 ldci 5
 ldci 4
 lao 6
 csp wrs
 ujp l 9
l 8
 lca'false           '
 ldci 5
 ldci 5
 lao 6
 csp wrs
l 9
 ldcc ' '
 ldci 1
 lao 6
 csp wrc
 ldob 10
 not
 fjp l 10
 lca'true            '
 ldci 5
 ldci 4
 lao 6
 csp wrs
 ujp l 11
l 10
 lca'false           '
 ldci 5
 ldci 5
 lao 6
 csp wrs
l 11
 ldcc ' '
 ldci 1
 lao 6
 csp wrc
 ldci 7
 odd
 fjp l 12
 lca'true            '
 ldci 6
 ldci 4
 lao 6
 csp wrs
 ujp l 13
l 12
 lca'false           '
 ldci 6
 ldci 5
 lao 6
 csp wrs
l 13
 ldcc '|'
 ldci 1
 lao 6
 csp wrc
 ldcc 'x'
 ldci 3
 lao 6
 csp wrc
 ldcc '|'
 ldci 1
 lao 6
 csp wrc
 lca''quoted'        '
 ldci 8
 ldci 8
 lao 6
 csp wrs
 lao 6
 csp wln
i  12: writeln('a string that is longer than sixteen characters, written in pieces')
 lca'a string that is'
 ldci 16
 ldci 16
 lao 6
 csp wrs
 lca' longer than six'
 ldci 16
 ldci 16
 lao 6
 csp wrs
 lca'teen characters,'
 ldci 16
 ldci 16
 lao 6
 csp wrs
 lca' written in piec'
 ldci 16
 ldci 16
 lao 6
 csp wrs
 lca'es              '
 ldci 2
 ldci 2
 lao 6
 csp wrs
 lao 6
 csp wln
 retp
l 2=13
l 3=4
q
 mst 0
 cup 0 l 1
 stp
q
