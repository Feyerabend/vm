{ Wirth's eight queens, from Algorithms + Data Structures = Programs:
  every way to put eight queens on a chess board, none attacking
  another. The arrays of diagonals run from -7 and from 2. }
program queens(output);
var row: array [1..8] of integer;
    free: array [1..8] of boolean;
    up: array [2..16] of boolean;
    down: array [-7..7] of boolean;
    i, solutions: integer;

    procedure show;
    var k: integer;
    begin
        for k := 1 to 8 do write(row[k]:2);
        writeln
    end;

    procedure try(column: integer);
    var r: integer;
    begin
        for r := 1 to 8 do
            if free[r] and up[r + column] and down[r - column] then begin
                row[column] := r;
                free[r] := false; up[r + column] := false; down[r - column] := false;
                if column < 8 then try(column + 1)
                else begin
                    solutions := solutions + 1;
                    if solutions <= 3 then show
                end;
                free[r] := true; up[r + column] := true; down[r - column] := true
            end
    end;

begin
    for i := 1 to 8 do free[i] := true;
    for i := 2 to 16 do up[i] := true;
    for i := -7 to 7 do down[i] := true;
    solutions := 0;
    try(1);
    writeln(solutions:1, ' solutions')
end.
