{ Reads a count, then that many numbers, from input. }
program sum(input, output);
var n, i, x, total: integer;
begin
    read(n);
    total := 0;
    for i := 1 to n do begin
        read(x);
        total := total + x
    end;
    writeln('the sum of ', n:1, ' numbers is ', total:1)
end.
