L0:
	LDARG 0		# 013 000
	ST 0		# 028 000
	LD 0		# 012 000
	SET 1		# 027 001
	EQ		    # 005
	JPZ :L16	# 011 016
	SET 1		# 027 001
	STORE 0		# 030 000
	RET		    # 024
L16:
	LD 0		# 012 000
	SET 1		# 027 001
	SUB		    # 031
	ST 3		# 028 003
	LD 3		# 012 003
	STARG 0		# 029 000
	CALL :L0	# 002 000
	LD 0		# 012 000
	LOAD 0		# 014 000
	MUL		    # 018
	STORE 0		# 030 000
	RET		    # 024
	RET		    # 024
START:
	SET 10		# 027 010
	STARG 0		# 029 000
	CALL :L0	# 002 000
	LOAD 0		# 014 000
	PRINT		# 022
	HALT		# 008
