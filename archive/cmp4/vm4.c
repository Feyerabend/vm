#include <stdio.h>
#include <stdlib.h>

#include "vm4.h"


VM* newVM(int* code, int pc, int datasize) {

	// allocate
	VM* vm = (VM*) malloc(sizeof(VM));
	if (vm == NULL)
		return NULL;
	vm->stack = (int*) malloc(sizeof(int) * STACK_SIZE);
	if (vm->stack == NULL)
		return NULL;
	vm->vars = (int*) malloc(sizeof(int) * datasize);
	if (vm->vars == NULL)
		return NULL;
	vm->args = (int*) malloc(sizeof(int) * datasize);
	if (vm->args == NULL)
		return NULL;

	// init
	vm->code = code;
	vm->pc = pc;
	vm->fp = 0;
	vm->sp = -1;

	return vm;
}

void freeVM(VM* vm){
	if (vm != NULL) {
		free(vm->args);
		free(vm->vars);
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

			case DIV:
				b = pop(vm);
				a = pop(vm);
				if (b == 0) {
					fprintf(stderr, "Runtime error: division by zero.\n");
					exit(EXIT_FAILURE);
				}
				push(vm, a / b);
				break;


			case PRINT:
				v = pop(vm);
				printf("%d\n", v);
				break;

			default:
				break;
		}

	} while (TRUE);
}



/* EOF */
