{ The sieve of Eratosthenes: the primes below 200.

  Every number starts out unmarked. Each prime p, found in turn,
  marks its multiples p*p, p*p + p, ... as not prime. What is still
  unmarked at the end is prime. }

const size = 200;
array marked:200;
var p, m, count;

begin
    p is 2;
    while p * p < size do
    begin
        if marked.p = 0 then
        begin
            m is p * p;
            while m < size do
            begin
                marked.m is 1;
                m is m + p
            end
        end;
        p is p + 1
    end;

    count is 0;
    p is 2;
    while p < size do
    begin
        if marked.p = 0 then
        begin
            print p;
            count is count + 1
        end;
        p is p + 1
    end;
    print count
end.
