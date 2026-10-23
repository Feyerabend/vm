i The smallest P4 program that does something, written by hand:
i
i   program hello(output);
i   begin
i       writeln('Hello, world!')
i   end.
i
i The main program is procedure l3. Its frame needs 9 words: five
i for the mark, and 5 to 8 for the files. wrs takes the string's
i address, the width to write it in, its length, and the file.
l 3
 ent 1 l 4
 ent 2 l 5
 lca'Hello, world!   '
 ldci 13
 ldci 13
 lao 6
 csp wrs
 lao 6
 csp wln
 retp
l 4=9
l 5=4
q
 mst 0
 cup 0 l 3
 stp
q
