procedure gcd[a, b];
  begin
    while a # b do
      begin
        if b < a
          then a is a - b
          else b is b - a
      end;
      return a
  end;

begin
    call gcd[15, 6];
    print rval
end.
