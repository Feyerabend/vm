#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "vm2.h"


/*  -------------------------------------
	FIBONACCI

	0 + 1 = 1
	1 + 1 = 2
	1 + 2 = 3
	2 + 3 = 5
	3 + 5 = 8
	5 + 8 = 13
	8 + 13 = ...

	TWODUP
	ADD
	ROT
	DROP

	F(0) = 0
	F(1) = 1
	F(n) = F(n − 1) + F(n − 2), n > 1
*/


// native

int fibonacci(n) {
	if (n == 0)
		return 0;
	if (n < 3)
		return 1;
	else
		return fibonacci(n - 1) + fibonacci(n - 2);
}

void native() {
	clock_t t;
	t = clock();
	printf("native: %d\n", fibonacci(20));
	t = clock() - t;
	double time_taken = ((double)t)/CLOCKS_PER_SEC;
  	printf("%f seconds\n", time_taken);
};



// compressed
int compressed_program[] = {
	SET, 18, // print 20, but starting with 2 (3) constants
	STORE, 0,

	SETZ,
	PRINT,

	SET, 1,
	DUP,
	PRINT,

	SET, 1,
	DUP,
	PRINT,

// 14:
	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	LOAD, 0,
	DEC,
	DUP,
	STORE, 0,

	JPNZ, 14,
	HALT
};

void compressed() {
	VM* vm = newVM(compressed_program, 0, 5);
	if (vm != NULL) {
		clock_t t;
		t = clock();
		run(vm);
		t = clock() - t;
		double duration = ((double) t) / CLOCKS_PER_SEC;
		printf("%f seconds\n", duration);
		freeVM(vm);
	}
};



// expanded
// 0
// 1
// 1
// 2
// 3
// 5
// 8
// 13
// 21
// 34
// 55
// 89
// 144
// 233
// 377
// 610
// 987
// 1597
// 2584
// 4181
// 6765

int expanded_program[] = {
	SET, 0,
	PRINT,

	SET, 1,
	DUP,
	PRINT,

	SET, 1,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	TWODUP,
	ADD,
	ROT,
	DROP,
	DUP,
	PRINT,

	HALT
};

void expanded() {
	VM* vm = newVM(expanded_program, 0, 5);
	if (vm != NULL) {
		clock_t t;
		t = clock();
		run(vm);
		t = clock() - t;
		double duration = ((double) t) / CLOCKS_PER_SEC;
		printf("%f seconds\n", duration);
		freeVM(vm);
	}
}

// test all
int main() {
	native();
	compressed();
	expanded();
	return 0;
}

/* EOF */
