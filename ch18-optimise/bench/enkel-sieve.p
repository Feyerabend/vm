{ The sieve of Eratosthenes below 4000, 200 times over: a benchmark
  for code as the enkel/0 compiler of chapter 10 writes it. }

const size = 4000;
array marked:4000;
var round, p, m, count;

begin
    round is 0;
    while round < 200 do
    begin
        p is 0;
        while p < size do
        begin
            marked.p is 0;
            p is p + 1
        end;
        count is 0;
        p is 2;
        while p < size do
        begin
            if marked.p = 0 then
            begin
                count is count + 1;
                m is p * p;
                if p < size / p then
                    while m < size do
                    begin
                        marked.m is 1;
                        m is m + p
                    end
            end;
            p is p + 1
        end;
        round is round + 1
    end;
    print count
end.
