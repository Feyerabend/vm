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

procedure bubble[n];
	var k, kk, l;
	begin
		l is n - 1;
		do
			begin
				k is 0;
				do
					begin
						kk is k + 1;
						if A.k > A.kk then call swap[k, kk];
						k is k + 1
					end
				while k < l;
				l is l - 1
			end
		while l > 0
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
	call bubble[10];
	call write[10]
end.
