
procedure max[a, b];
	begin
		if a > b then return a;
		return b
	end;

procedure gcd[a, b];
	var c;
	begin
		c is -a;
		call max[a, c];
		a is rval;
		if b = 0 then return a;
		c is a % b;
		call gcd[b, c]
	end;

begin
	call gcd[1071, 462];
	print rval
end.