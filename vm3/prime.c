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

const int START = 50;
int program[] = {
	27, 28, 0, 26, 1, 28, 1, 13, 1, 12, 1, 17, 6, 11, 20,
	12, 0, 8, 28, 0, 12, 1, 8, 28, 1, 12, 1, 13, 1, 16, 10,
	7, 12, 1, 13, 1, 5, 10, 7, 12, 0, 26, 2, 5, 11, 49, 13,
	1, 22, 24, 26, 99, 30, 0, 26, 1, 30, 1, 14, 1, 8, 4, 30,
	1, 29, 1, 2, 0, 14, 1, 14, 0, 16, 10, 58, 14, 0, 14, 1,
	5, 10, 58, 7
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