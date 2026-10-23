{ case, as P4 compiles it: a jump through a table. }
program fizzbuzz(output);
var i: integer;
begin
    for i := 1 to 20 do
        case i mod 15 of
            0: writeln('FizzBuzz');
            3, 6, 9, 12: writeln('Fizz');
            5, 10: writeln('Buzz');
            1, 2, 4, 7, 8, 11, 13, 14: writeln(i:1)
        end
end.
