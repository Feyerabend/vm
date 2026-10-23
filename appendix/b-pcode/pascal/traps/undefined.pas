{ Pascal does not set a variable to anything until it is given a
  value. The original P4 machine would print whatever was left in that
  word; ours stops. }
program undefined(output);
var x, y: integer;
begin
    x := 1;
    writeln(x + y)
end.
