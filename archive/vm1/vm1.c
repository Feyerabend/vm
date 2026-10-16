#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "vm1.h"


VM* newVM(int* code, int pc) {

	// allocate
	VM* vm = (VM*) malloc(sizeof(VM));
	if (vm == NULL)
		return NULL;
	vm->stack = (int*) malloc(sizeof(int) * STACK_SIZE);
	if (vm->stack == NULL)
		return NULL;

	// init
	vm->code = code;
	vm->pc = pc;
	vm->sp = -1;

	return vm;
}

void freeVM(VM* vm){
	if (vm != NULL) {
		free(vm->stack);
		free(vm);
	}
}

int pop(VM* vm) {
	int sp = (vm->sp)--;
	return vm->stack[sp];
}

void push(VM* vm, int v) {
	int sp = ++(vm->sp);
	vm->stack[sp] = v;
}

int nextcode(VM* vm) {
	int pc = (vm->pc)++;
	return vm->code[pc];
}

void run(VM* vm){
	int v, a, b;

	do {
		int opcode = nextcode(vm);
		switch (opcode) {

			case HALT:
				return;

			case SET:
				v = nextcode(vm);
				push(vm, v);
				break;

			case ADD:
				b = pop(vm);
				a = pop(vm);
				push(vm, a + b);
				break;
      
			case SUB:
				b = pop(vm);
				a = pop(vm); 
				push(vm, a - b);
				break;

			case MUL:
				b = pop(vm);
				a = pop(vm);
				push(vm, a * b);
				break;

			case PRINT:
				v = pop(vm);
				printf("%d\n", v);
				break;

			default:
				break;
		} // switch

	} while (TRUE);
}

int program[] = {
        SET, 33,
        SET, 44,
        ADD,
        PRINT,
        HALT
};

int main() {
        VM* vm = newVM(program, 0);
        if (vm != NULL) {
		clock_t t;
		t = clock();

		run(vm);

		t = clock() - t;
		double duration = ((double) t) / CLOCKS_PER_SEC;
		printf("%f seconds\n", duration);
		freeVM(vm);
        }
        return 0;
};

/* EOF */
