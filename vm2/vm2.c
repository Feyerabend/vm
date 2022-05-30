#include <stdio.h>
#include <stdlib.h>
#include "vm2.h"


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

	// init
	vm->code = code;
	vm->pc = pc;
	vm->fp = 0;
	vm->sp = -1;

	return vm;
}

void freeVM(VM* vm){
	if (vm != NULL) {
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

void run(VM* vm) {
	int v, addr, offset, a, b, c, argc, rval;

	do {
		// fetch next code ..
		int opcode = nextcode(vm);

		// .. execute
		switch (opcode) {

			case NA:
			case NOP:
				break;				

			case HALT:
				return;		

			case SET:
				v = nextcode(vm);
				push(vm, v);
				break;

			case SETZ:
				push(vm, 0);
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

			case INC:
				a = pop(vm);
				push(vm, a + 1);
				break;

			case DEC:
				a = pop(vm);
				push(vm, a - 1);
				break;

			case LT:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a < b) ? TRUE : FALSE);
				break;

			case EQ:
				b = pop(vm);
				a = pop(vm);
				push(vm, (a == b) ? TRUE : FALSE);
				break;

			case EQZ:
				a = pop(vm);
				push(vm, (a == 0) ? TRUE : FALSE);
				break;

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

			case LDARG:
				offset = nextcode(vm);
				offset = offset - 4;
				v = vm->stack[vm->fp + offset];
				push(vm, v);
				break;

			case LD:
				offset = nextcode(vm);
				v = vm->vars[vm->fp + offset];
				push(vm, v);
				break;

			case ST:
				v = pop(vm);
				offset = nextcode(vm);
				vm->vars[vm->fp + offset] = v;
				break;

			case LOAD:
				addr = nextcode(vm);
				v = vm->vars[addr];
				push(vm, v);
				break;

			case STORE:
				v = pop(vm);
				addr = nextcode(vm);
				vm->vars[addr] = v;
				break;

			case CALL:
				addr = nextcode(vm);
				argc = nextcode(vm);
				push(vm, argc);
				push(vm, vm->fp);
				push(vm, vm->pc);
				vm->fp = vm->sp;
				vm->pc = addr;
				break;

			case RET:
				rval = pop(vm);
				vm->sp = vm->fp;
				vm->pc = pop(vm);
				vm->fp = pop(vm);
				argc = pop(vm);
				vm->sp -= argc; // ignore rest of stack
				push(vm, rval);
				break;

			case DROP:
				pop(vm);
				break;

			case SWAP:
				b = pop(vm);
				a = pop(vm); 
				push(vm, b);
				push(vm, a);
				break;

			case TWODUP:
				b = pop(vm);
				a = pop(vm); 
				push(vm, a);
				push(vm, b);
				push(vm, a);
				push(vm, b);
				break;

			case ROT:
				c = pop(vm);
				b = pop(vm);
				a = pop(vm); 
				push(vm, b);
				push(vm, c);
				push(vm, a);
				break;

			case DUP:
				a = pop(vm);
				push(vm, a);
				push(vm, a);
				break;

			case OVER:
				b = pop(vm);
				a = pop(vm);
				push(vm, b);
				push(vm, a);
				push(vm, b);
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


/* EOF */
