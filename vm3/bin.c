#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "vm3.h"


int power(int x, int n) {
	int p;
	if (n == 0) {
		p = 1;
	} else {
		for (p = 1; n > 0; --n) {
			p = p * x;
		}
	}
	return p;
}

int powerD(int x, int y) {
	int r = 1; 
	while (y > 0) {
		if (y & 1) {
			r = r * x;
		}
		y = y >> 1;
		x = x * x;
	}
	return r;
}

void bin1(int in) {
	int loop;
	loop = 32;
	while (loop > 0) {
		if (in & powerD(2, loop - 1)) {
			printf("1");
		} else {
			printf("0");
		}
		--loop;
	}
	printf("\n");
}

void bin2(int n) {
	int c, t;
	c = 32;
	do {
		t = (n >> (c - 1)) & 1;
		if (t) {
			printf("1");
		} else {
			printf("0");
		}
		c--;
	} while (c > 0);
	printf("\n");
}


int program[] = {
	26, 16, 30, 0, 26, 51966, 14, 0, 3, 25, 26, 1, 1, 23, 14, 0, 3, 4, 30, 0, 10, 4, 7
};

/*{
	SET, 16,	// number of bits
	STORE, 0,

// 4:
	SET, 51966,	// decimal input
	LOAD, 0,
	DEC,
	RSH,
	SET, 1,
	AND,
	PRNT,

	LOAD, 0,
	DEC,
	DUP,
	STORE, 0,

	JPNZ, 4,
	HALT
};*/

void bin() {
	VM* vm = newVM(program, 0, 10);
	if (vm != NULL) {
		run(vm);
		freeVM(vm);
	}
}

int main() {
	bin();
	return 0;
}


/* EOF */