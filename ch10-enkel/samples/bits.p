{ Bitwise operators: count the 1 bits in some numbers, and print
  numbers in binary. "and 1" keeps the lowest bit; dividing by 2
  shifts the rest down. }

procedure ones[n];
var count;
begin
    count is 0;
    while n do                  { a condition can be any value: 0 is false }
    begin
        count is count + (n and 1);
        n is n / 2
    end;
    return count
end;

procedure binary[n];
begin
    if n > 1 then call binary[n / 2];
    emit (n and 1) + 48
end;

begin
    call ones[255]; print rval;          { 8 }
    call ones[1023 xor 15]; print rval;  { 6 }
    call binary[10]; emit 10;
    call binary[(12 or 3) and 13]; emit 10
end.
