program squares(output);
var i: integer;

    function square(x: integer): integer;
    begin
        square := x * x
    end;

begin
    for i := 1 to 5 do
        writeln(i:2, square(i):4)
end.
