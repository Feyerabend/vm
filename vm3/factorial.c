#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "vm3.h"


/* -------------------------------------
	FACTORIAL

	5! = 1 × 2 × 3 × 4 × 5 = 120
		same as
	5! = 5 x 4 x 3 x 2 x 1 = 120
*/

int standard_factorial(int n) {
	if (n == 1)
		return 1;
	else
		return n * standard_factorial(n - 1);
}

//  switch replacing if-then-else
int switch_factorial(int n) {
	switch(n) {
		case 1:
			return 1;
		default:
			return n * switch_factorial(n - 1);
	}
}

//  iterative -- non-recursive
int nrec_factorial(int n) {
	int fact = 1;
 	for (int i = 1; i <= n; i++) {
		fact = fact * i;
	}
	return fact;
}

//  non-recursive -- but looping backwards
int nrecb_factorial(int n) {
	int fact = 1;
 	for (int i = n; i > 1; i--) {
		fact = fact * i;
	}
	return fact;
}

//  non-recursive
int nrecw_factorial(int n) {
	int fact = 1;
	int i = n;
	do {
		fact = fact * i;
		i--;
	} while (i > 0);
	return fact;
}

// yet another non-recursive
int ya_factorial(int n) {
    int f = 1;
    for (int i = 2; i <= n; i++) {
        f *= i;
    }
    return f;
}


int factorial_program[] = {
	27, 15, 5, 31, 0, 27, 1, 31, 1, 15, 0, 15, 1, 19, 31, 1, 15, 0, 3, 5, 31, 0, 11, 9, 15, 1, 23, 8
};

/*{
	SET, 15,	// n = 15
	DUP,
	STORE, 0,	// i = 15
	SET, 1,
	STORE, 1,	// fact = 1

// 9:
	LOAD, 0,	// i
	LOAD, 1,	// fact
	MUL,		// i * fact ->
	STORE, 1,	// -> fact
	LOAD, 0,	// i
	DEC,		// --i
	DUP,
	STORE, 0,	// -> i
	JPNZ, 9,	// i ≠ 0 ?

	LOAD, 1,	// fact
	PRINT,
	HALT

};*/

void factorial() {
	VM* vm = newVM(factorial_program, 0, 5);
	if (vm != NULL) {
		run(vm);
		freeVM(vm);
	}
};



int main() {
	printf("standard: %d\n", standard_factorial(15));
	printf("switch: %d\n", switch_factorial(15));
	printf("non-recursive: %d\n", nrec_factorial(15));
	printf("non-recursive backwards: %d\n", nrecb_factorial(15));
	printf("non-recursive while-loop: %d\n", nrecw_factorial(15));
	printf("vm factorial: ");
	factorial();
	printf("\n");

	return 0;
}
