procedure factorial[n];
	var m, o;
	begin
		if n = 1 then return 1;
		o is n - 1;
		call factorial[o];
		return (n * rval)
	end;

begin
	call factorial[10];
	print rval
end.