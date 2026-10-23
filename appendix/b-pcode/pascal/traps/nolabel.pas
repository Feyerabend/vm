program nolabel(output);
var i: integer;
begin
    for i := 1 to 4 do
        case i of
            1, 2: writeln('small');
            4: writeln('four')
        end
end.
