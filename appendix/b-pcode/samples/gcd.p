; Euclid's algorithm, by subtraction. In PL/0:
;
;   var x, y;
;   begin
;       x := 84; y := 36;
;       while x # y do begin
;           if x > y then x := x - y;
;           if y > x then y := y - x
;       end;
;       ! x
;   end.
;
; The main program is a procedure too: its frame is the three words
; every frame has, then x at offset 3 and y at offset 4.

        jmp main
main:   int 5
        lit 84
        sto 0 3
        lit 36
        sto 0 4
while:  lod 0 3
        lod 0 4
        opr neq
        jpc done
        lod 0 3
        lod 0 4
        opr gtr
        jpc second
        lod 0 3
        lod 0 4
        opr sub
        sto 0 3
second: lod 0 4
        lod 0 3
        opr gtr
        jpc while
        lod 0 4
        lod 0 3
        opr sub
        sto 0 4
        jmp while
done:   lod 0 3
        opr write
        opr ret
