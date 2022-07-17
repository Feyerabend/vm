#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "vm3.h"


int fib(int n) {
	if (n == 0) return 0;
	if (n == 1) return 1;
	else return fib(n-1) + fib(n-2);
}

int fibonacci_program[] = {
	27, 15, 30, 1, 2, 8, 23, 8, 14,
	1, 5, 7, 12, 15, 25, 5, 27, 1,
	6, 12, 22, 25, 3, 5, 29, 1, 30,
	1, 2, 8, 29, 0, 13, 1, 3, 30,
	1, 2, 8, 13, 0, 0, 25
};

void fibonacci() {
	VM* vm = newVM(fibonacci_program, 0, 100);
	if (vm != NULL) {
		run(vm);
		freeVM(vm);
	}
};

int main() {
	fibonacci();
	printf("%d\n", fib(15));
	return 0;
}
