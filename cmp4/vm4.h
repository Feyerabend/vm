#include <stdio.h>
#include <stdlib.h>

#define STACK_SIZE 32768
#define TRUE 1
#define FALSE 0

typedef struct {
	int* vars;
	int* args;
	int* code;
	int* stack;
	int pc;
	int sp;
	int fp;
} VM;

// must be in sync with asm.py
enum {
	ADD,	// 0
	DIV,	// 4
	HALT,	// 9
	MUL,	// 20
	PRINT,	// 24
	SET,	// 28
	SUB		// 33
};

VM* newVM(int* code, int pc, int datasize);
void freeVM(VM* vm);
void run(VM* vm);

/* EOF */
