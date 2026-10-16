#include <stdio.h>
#include <stdlib.h>
#include "vm3.h"

void prime() {
	int i, j, n;
 	n = 100;

	for (i = 2; i <= n; i++) {

		int c = 0;
		j = 1;

		do {
			if (i % j == 0) {
				c++;
			}
			j++;

		} while (j <= i);

		if (c == 2) {
			printf("%d ",i);
		}
	}
}

const int START = 51;
int program[] = {
	28, 29, 0, 27, 1, 29, 1, 14, 1,
	13, 1, 18, 7, 12, 20, 13, 0, 9,
	29, 0, 13, 1, 9, 29, 1, 13, 1,
	14, 1, 17, 11, 7, 13, 1, 14, 1,
	6, 11, 7, 13, 0, 27, 2, 6, 12,
	49, 14, 1, 23, 4, 25, 27, 99,
	31, 0, 27, 1, 31, 1, 15, 1, 9,
	5, 31, 1, 30, 1, 2, 0, 15, 1,
	15, 0, 17, 11, 59, 15, 0, 15, 1,
	6, 11, 59, 8
};

void primevm() {
        VM* vm = newVM(program, START, 200);
        if (vm != NULL) {
                run(vm);
                freeVM(vm);
        }
}

int main() {
	prime();
	primevm();
	return 0;
}

/* EOF */