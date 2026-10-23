program matrix(output);
type square = array [1..3, 1..3] of integer;
var a, b, c: square;
    i, j, k: integer;
begin
    for i := 1 to 3 do
        for j := 1 to 3 do begin
            a[i, j] := i + j;
            b[i][j] := i * j
        end;
    for i := 1 to 3 do
        for j := 1 to 3 do begin
            c[i, j] := 0;
            for k := 1 to 3 do
                c[i, j] := c[i, j] + a[i, k] * b[k, j]
        end;
    a := c;
    for i := 1 to 3 do begin
        for j := 1 to 3 do write(a[i, j]:5);
        writeln
    end
end.
