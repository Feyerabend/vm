#include <stdio.h>
#include <stdlib.h>

#define STACK_SIZE 200
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

enum {
	ADD,	// 0
	AND,	// 1
	CALL,	// 2
	DEC,	// 3
	DUP,	// 4
	EQ,		// 5
	EQZ,	// 6
	HALT,	// 7
	INC,	// 8
	JP,		// 9
	JPNZ,	// 10
	JPZ,	// 11
	LD,		// 12
	LDARG,	// 13
	LOAD,	// 14
	LSH,	// 15
	LT,		// 16
	MOD,	// 17
	MUL,	// 18
	NA,		// 19
	NOP,	// 20
	OR,		// 21
	PRINT,	// 22
	PRNT,	// 23
	RET,	// 24
	RSH,	// 25
	SET,	// 26
	SETZ,	// 27
	ST,		// 28
	STARG,	// 29
	STORE,	// 30
	SUB		// 31
};

VM* newVM(int* code, int pc, int datasize);
void freeVM(VM* vm);
void run(VM* vm);

/* EOF */
