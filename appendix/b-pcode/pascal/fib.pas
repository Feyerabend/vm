program fib(output);
var n: integer;

    function fib(n: integer): integer;
    begin
        if n < 2 then fib := n
        else fib := fib(n - 1) + fib(n - 2)
    end;

begin
    n := 0;
    repeat
        write(fib(n):5);
        n := n + 1
    until n > 15;
    writeln
end.
