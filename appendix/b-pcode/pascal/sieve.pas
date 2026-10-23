{ The primes below 100, by Eratosthenes' sieve. }
program sieve(output);
const n = 100;
var prime: array [2..n] of boolean;
    i, j, count: integer;
begin
    for i := 2 to n do prime[i] := true;
    i := 2;
    while i * i <= n do begin
        if prime[i] then begin
            j := i * i;
            while j <= n do begin
                prime[j] := false;
                j := j + i
            end
        end;
        i := i + 1
    end;
    count := 0;
    for i := 2 to n do
        if prime[i] then begin
            write(i:4);
            count := count + 1;
            if count mod 10 = 0 then writeln
        end;
    writeln;
    writeln(count:1, ' primes')
end.
