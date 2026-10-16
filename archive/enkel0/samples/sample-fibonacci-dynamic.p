array A:15;

procedure nl[];
	begin
		emit 13; emit 10
	end;

procedure write[n];
	var j;
	begin
		j is 0;
		do
			begin
				print A.j;
				j is j + 1
			end
		while j < n
	end;

procedure fib[n];
	var i, j, k;
	begin
		A.0 is 0;
		A.1 is 1;

		i is 2;
		while i <= n do
		begin
			j is (i - 1);
			k is (i - 2);
			A.i is A.j + A.k;
			i is i + 1
		end
	end;


begin
	call nl[];
	call fib[15];
	call write[15]
end.
