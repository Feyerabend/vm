program hanoi(output);

    procedure move(n: integer; source, target, spare: char);
    begin
        if n > 0 then begin
            move(n - 1, source, spare, target);
            writeln('disc ', n:1, ' from ', source, ' to ', target);
            move(n - 1, spare, target, source)
        end
    end;

begin
    move(3, 'A', 'C', 'B')
end.
