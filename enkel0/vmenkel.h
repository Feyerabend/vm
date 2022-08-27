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
	EQ,		// 6
	GT,		// 7
	GQ,		// 8
	HALT,	// 9
	JP,		// 10
	JPNZ,	// 11
	JPZ,	// 12
	LD,		// 13
	LDARG,	// 14
	LOAD,	// 15
	LT,		// 16
	LQ,		// 17
	MOD,	// 18
	MUL,	// 19
	NEQ,	// 20
	NOP,	// 21
	NOT,	// 22 // skip?
	OR,		// 23
	PRINT,	// 24
	PRNT,	// 25
	RET,	// 26
	RLOAD,	// 27
	RSTORE,	// 28
	SET,	// 29
	ST,		// 30
	STARG,	// 31
	STORE,	// 32
	SUB,	// 33
	UMIN,	// 34
	XOR		// 35
};

VM* newVM(int* code, int pc, int vars, int args, int arrs);
void freeVM(VM* vm);
void run(VM* vm);


/* EOF */
