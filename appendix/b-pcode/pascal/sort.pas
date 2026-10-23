{ var parameters: swap changes its caller's variables, and sort its
  caller's array. }
program sort(output);
type list = array [1..8] of integer;
var a: list;
    i: integer;

    procedure swap(var x, y: integer);
    var t: integer;
    begin
        t := x; x := y; y := t
    end;

    procedure sort(var a: list);
    var i, j: integer;
    begin
        for i := 1 to 7 do
            for j := 8 downto i + 1 do
                if a[j] < a[j - 1] then swap(a[j], a[j - 1])
    end;

    procedure show(var a: list);
    var i: integer;
    begin
        for i := 1 to 8 do write(a[i]:4);
        writeln
    end;

begin
    a[1] := 31; a[2] := 4; a[3] := 15; a[4] := -9;
    a[5] := 26; a[6] := 5; a[7] := 3; a[8] := 0;
    show(a);
    sort(a);
    show(a)
end.
