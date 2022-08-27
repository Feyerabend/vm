#include <stdio.h>
#include <stdlib.h>

#include "vmenkel.h"


VM* newVM(int* code, int pc, int vars, int args, int arrs) {

	// allocate
	VM* vm = (VM*) malloc(sizeof(VM));
	if (vm == NULL)
		return NULL;
	vm->stack = (int*) malloc(sizeof(int) * STACK_SIZE);
	if (vm->stack == NULL)
		return NULL;
	vm->vars = (int*) malloc(sizeof(int) * vars);
	if (vm->vars == NULL)
		return NULL;
	vm->args = (int*) malloc(sizeof(int) * args);
	if (vm->args == NULL)
		return NULL;
	vm->arrs = (int*) malloc(sizeof(int) * arrs);
	if (vm->arrs == NULL)
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
		free(vm->arrs);
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
	int v, addr, offset, a, b;

	do {
		int opcode = nextcode(vm);

		switch (opcode) {

			case ADD:
				b = pop(vm);
				a = pop(vm);
				push(vm, a + b);
				break;

			case AND:
				b = pop(vm);
				a = pop(vm);
				push(vm, a & b);
				break;

			case CALL:
				addr = nextcode(vm);
				push(vm, vm->fp);
				push(vm, vm->pc);
				vm->fp = vm->sp;
				vm->pc = addr;
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

			case EMIT:
				v = pop(vm);
				printf("%c", (char)v);
				break;

			case EQ:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a == b) ? TRUE : FALSE);
				break;

			case GT:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a > b) ? TRUE : FALSE);
				break;

			case GQ:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a >= b) ? TRUE : FALSE);
				break;

			case HALT:
				return;

			case JP:
				vm->pc = nextcode(vm);
				break;

			case JPNZ:
				addr = nextcode(vm);
				v = pop(vm);
				if (v != 0) {
					vm->pc = addr;
				}
				break;

			case JPZ:
				addr = nextcode(vm);
				v = pop(vm);
				if (v == 0) {
					vm->pc = addr;
				}
				break;

			case LD:
				offset = nextcode(vm);
				v = vm->vars[vm->fp + offset];
				push(vm, v);
				break;

			case LDARG:
				addr = nextcode(vm);
				v = vm->args[addr];
				push(vm, v);
				break;

			case LOAD:
				addr = nextcode(vm);
				v = vm->vars[addr];
				push(vm, v);
				break;

			case LT:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a < b) ? TRUE : FALSE);
				break;

			case LQ:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a <= b) ? TRUE : FALSE);
				break;

			case MOD:
				b = pop(vm);
				a = pop(vm);
				push(vm, a % b);
				break;

			case MUL:
				b = pop(vm);
				a = pop(vm);
				push(vm, a * b);
				break;

			case NEQ:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a != b) ? TRUE : FALSE);
				break;

			case NOT: // skip?
				a = pop(vm);
				push(vm, !a);
				break;

			case NOP:
				break;				

			case OR:
				b = pop(vm);
				a = pop(vm);
				push(vm, a | b);
				break;

			case PRINT:
				v = pop(vm);
				printf("%d\n", v);
				break;

			case PRNT:
				v = pop(vm);
				printf("%d", v);
				break;

			case RET:
				vm->sp = vm->fp;
				vm->pc = pop(vm);
				vm->fp = pop(vm);
				break;

			case RLOAD:
				a = pop(vm);
				v = vm->arrs[a];
				push(vm, v);
				break;

			case RSTORE:
				a = pop(vm);
				b = pop(vm);
				vm->arrs[a] = b;
				break;

			case SET:
				v = nextcode(vm);
				push(vm, v);
				break;

			case ST:
				v = pop(vm);
				offset = nextcode(vm);
				vm->vars[vm->fp + offset] = v;
				break;

			case STARG:
				v = pop(vm);
				addr = nextcode(vm);
				vm->args[addr] = v;
				break;

			case STORE:
				v = pop(vm);
				addr = nextcode(vm);
				vm->vars[addr] = v;
				break;

			case SUB:
				b = pop(vm);
				a = pop(vm); 
				push(vm, a - b);
				break;

			case UMIN:
				a = pop(vm);
				push(vm, -a);
				break;

			case XOR:
				b = pop(vm);
				a = pop(vm);
				push(vm, a ^ b);
				break;

			default:
				break;

		}

	} while (TRUE);
}



/* EOF */
