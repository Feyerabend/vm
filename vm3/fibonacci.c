#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "vm3.h"


int fibonacci_program[] = {
	27, 15, 30, 1, 2, 8, 23, 8,
	14, 1, 5, 7, 12, 15, 25, 5,
	27, 1, 6, 12, 22, 25, 27, 1,
	32, 5, 29, 1, 30, 1, 2, 8,
	29, 0, 13, 1, 27, 1, 32, 30,
	1, 2, 8, 13, 0, 0, 25
};

void fibonacci() {
	VM* vm = newVM(fibonacci_program, 0, 200);
	if (vm != NULL) {
		run(vm);
		freeVM(vm);
	}
};


int main() {
	fibonacci();
	return 0;
}
