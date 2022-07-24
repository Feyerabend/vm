var i, x, r, answer;

procedure fib;
var xx, r1, r2;
begin
  xx := x;
  if xx = 0 then r := 1;
  if xx = 1 then r := 1;
  if xx >= 2 then begin
    x := xx - 2;
    call fib;
    r1 := r;
    x := xx - 1;
    call fib;
    r2 := r;
    r := r1 + r2
  end
end;

begin
  i := 0;
  while i < 35 do begin
    x := i;
    call fib;
    answer := r;
    i := i + 1
  end
end.