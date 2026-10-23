i The program of nested.p, in P4 and written by hand:
i
i   program nested(output);
i   var total: integer;
i       procedure outer;
i       var k: integer;
i           procedure down;
i           begin
i               if k > 0 then begin
i                   writeln(k);
i                   total := total + k;
i                   k := k - 1;
i                   down
i               end
i           end;
i       begin
i           k := 5;
i           down
i       end;
i   begin
i       total := 0;
i       outer;
i       writeln(total)
i   end.
i
i The main program is at level 1, outer at 2, down at 3. total is a
i variable of the main program, so it has a fixed address, 9, and ldo
i and sro reach it directly. k is at offset 5 in outer's frame, after
i the five words of the mark; down finds it one level out (lodi 1 5).
i mst p sets the static link of the frame it begins: p is the level of
i the caller, minus the level of the one called, plus one. outer calls
i down with mst 0, and down calls itself with mst 1.
i
i down
l 4
 ent 1 l 5
 ent 2 l 6
 lodi 1 5
 ldci 0
 grti
 fjp l 7
 lodi 1 5
 ldci 1
 lao 6
 csp wri
 lao 6
 csp wln
 ldoi 9
 lodi 1 5
 adi
 sroi 9
 lodi 1 5
 ldci 1
 sbi
 stri 1 5
 mst 1
 cup 0 l 4
l 7
 retp
l 5=5
l 6=5
i outer
l 3
 ent 1 l 8
 ent 2 l 9
 ldci 5
 stri 0 5
 mst 0
 cup 0 l 4
 retp
l 8=6
l 9=5
i the main program
l 2
 ent 1 l 10
 ent 2 l 11
 ldci 0
 sroi 9
 mst 0
 cup 0 l 3
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
 cup 0 l 2
 stp
q
