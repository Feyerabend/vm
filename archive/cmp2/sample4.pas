

var x, squ, answer;

procedure square;
begin
   squ := x * x
end;

begin
   x := 1;
   while x <= 10 do
   begin
      call square;
      answer := squ;
      x := x + 1
   end
end.