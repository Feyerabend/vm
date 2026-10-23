program gcd(output);

    function gcd(a, b: integer): integer;
    begin
        if b = 0 then gcd := a
        else gcd := gcd(b, a mod b)
    end;

begin
    writeln(gcd(12, 18):4, gcd(17, 5):4, gcd(1071, 462):4, gcd(0, 7):4)
end.
