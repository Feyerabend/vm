
procedure factorial[n];
  var m;
  begin
    if n = 1 then return 1;
    m is n - 1;
    call factorial[m];
    rval is (n * rval)
  end;

begin
  call factorial[10];
  print rval
end.
