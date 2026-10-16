procedure nl[];
  begin
    emit 13; emit 10
  end;

procedure prnt[d, t];
  var a, b, c, f1, f2;
  begin

    f1 is 0; f2 is 0;
    a is (d % 10);

    if t = 1 then
      f1 is 1;
    if t = 2 then
      begin
        f1 is 1;
        f2 is 1
      end;

    if f1 = 1 then
      begin
        d is (d / 10);
        b is (d % 10)
      end;        

    if f2 = 1 then
      begin
        d is (d / 10);
        c is (d % 10)
      end;

    a is (a or 48);
    if f1 = 1 then
      b is (b or 48);
    if f2 = 1 then
      c is (c or 48);

    if f2 = 1 then
      emit c;
    if f1 = 1 then
      emit b;
    emit a

  end;

procedure alpha[];
  var i;
  begin

    i is 0;
    while i < 26 do
      begin
        call prnt[i, 2];
        emit 32;
        i is i + 1
      end;
    call nl[];

    i is 0;
    while i < 26 do
      begin
        emit 32;
        emit 32;
        emit (i + 97);
        emit 32;
        i is i + 1
      end;
    call nl[];

    i is 0;
    while i < 26 do
      begin
        emit 32;
        emit 32;
        emit (i + 65);
        emit 32;
        i is i + 1
      end

  end;

begin
  call alpha[];
  call nl[]
end.
