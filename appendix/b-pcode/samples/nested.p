; A procedure nested in another, calling itself. In PL/0:
;
;   var total;
;   procedure outer;
;       var k;
;       procedure down;
;       begin
;           if k > 0 then begin
;               ! k;
;               total := total + k;
;               k := k - 1;
;               call down
;           end
;       end;
;   begin
;       k := 5;
;       call down
;   end;
;   begin
;       total := 0;
;       call outer;
;       ! total
;   end.
;
; down is at level 2. It finds k one level out, in outer's frame, and
; total two levels out, in the main program's. Each time down calls
; itself, the new frame's dynamic link is the old down, but its static
; link is still outer: where down was written, not who called it.

        jmp main

down:   int 3
        lod 1 3         ; k
        lit 0
        opr gtr
        jpc end
        lod 1 3
        opr write
        lod 2 3         ; total := total + k
        lod 1 3
        opr add
        sto 2 3
        lod 1 3         ; k := k - 1
        lit 1
        opr sub
        sto 1 3
        cal 1 down      ; down is declared one level out from here
end:    opr ret

outer:  int 4
        lit 5
        sto 0 3
        cal 0 down      ; ... and in outer itself, from here
        opr ret

main:   int 4
        lit 0
        sto 0 3
        cal 0 outer
        lod 0 3
        opr write
        opr ret
