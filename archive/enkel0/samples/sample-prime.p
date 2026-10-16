procedure prime[n];
	var i, j, k, c;
	begin
		i is 2;
		do
			begin
				c is 0;
				j is 1;
				do
					begin
						k is i % j;
						if k = 0 then c is c + 1;
						j is j + 1;
					end
				while j <= i;
				if c = 2 then print i;
				i is i + 1
			end
		while i <= n
	end;

begin
	call prime[1000]
end.
