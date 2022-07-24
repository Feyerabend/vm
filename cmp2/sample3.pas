var x;

procedure func0;
var x0;
begin
  x0 := 456;
  call func1
end;

procedure func1;
var x1;
begin
  x1 := 789;
  call func0
end;

begin
  x := 123;
  call func0
end.