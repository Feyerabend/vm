{ The program of samples/nested.p and nested.p4: down is declared
  inside outer, finds outer's k one level out, and calls itself. }
program nested(output);
var total: integer;

    procedure outer;
    var k: integer;

        procedure down;
        begin
            if k > 0 then begin
                writeln(k:1);
                total := total + k;
                k := k - 1;
                down
            end
        end;

    begin
        k := 5;
        down
    end;

begin
    total := 0;
    outer;
    writeln(total:1)
end.
