#include <stdio.h>
#include <stdlib.h>

#define STACK_SIZE 32768
#define TRUE 1
#define FALSE 0

typedef struct {
	int* vars;
	int* args;
	int* arrs;
	int* code;
	int* stack;
	int pc;
	int sp;
	int fp;
} VM;

// must be in sync with asm.py
enum {
	ADD,	// 0
	AND,	// 1
	CALL,	// 2
	DIV,	// 4
	EMIT,	// 5
	EQ,	// 6
	GT,	// 7
	GQ,	// 8
	HALT,	// 9
	JP,	// 10
	JPNZ,	// 11
	JPZ,	// 12
	LD,	// 13
	LDARG,	// 14
	LOAD,	// 15
	LT,	// 16
	LQ,	// 17
	MOD,	// 18
	MUL,	// 19
	NEQ,	// 20
	NOP,	// 21
	OR,	// 22
	PRINT,	// 23
	PRNT,	// 24
	RET,	// 25
	RLOAD,	// 26
	RSTORE,	// 27
	SET,	// 28
	ST,	// 29
	STARG,	// 30
	STORE,	// 31
	SUB,	// 32
	UMIN,	// 33
	XOR	// 34
};

VM* newVM(int* code, int pc, int vars, int args, int arrs);
void freeVM(VM* vm);
void run(VM* vm);


/* EOF */
