array A:10;

procedure nl[];
	begin
		emit 13; emit 10
	end;

procedure swap[a, b];
	var u;
	begin
		u is A.a;
		A.a is A.b;
		A.b is u
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
		while j < n;
		call nl[]
	end;

procedure insert[n];
	var i, j, m, t;
	begin
		i is 0;
		do
			begin
				j is i;
				m is i;
				do
					begin
						if A.j < A.m then m is j;
						j is j + 1
					end
				while j < n;
				call swap[i, m];
				i is i + 1
			end
		while i < n
	end;

begin
	A.0 is 90;
	A.1 is 45;
	A.2 is 4;
	A.3 is 56;
	A.4 is 1;
	A.5 is 99;
	A.6 is 8;
	A.7 is 50;
	A.8 is 32;
	A.9 is 10;

	call write[10];
	call insert[10];
	call write[10]
end.
