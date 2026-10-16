{ The towers of Hanoi: move n discs from peg a to peg c, using b.

  To move n discs, move n - 1 out of the way onto the spare peg, move
  the biggest one, and move the n - 1 back on top of it. Each move is
  printed as two digits, from and to: 13 means from peg 1 to peg 3. }

var moves;

procedure move[from, to];
begin
    emit from + 48;
    emit to + 48;
    emit 32;
    moves is moves + 1
end;

procedure hanoi[n, a, b, c];
begin
    if n > 0 then
    begin
        call hanoi[n - 1, a, c, b];
        call move[a, c];
        call hanoi[n - 1, b, a, c]
    end
end;

begin
    moves is 0;
    call hanoi[4, 1, 2, 3];
    emit 10;
    print moves     { 2^4 - 1 = 15 }
end.
