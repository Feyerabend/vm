#include <stdio.h>
#include <stdlib.h>

#define STACK_SIZE 200
#define OFF 10
#define TRUE 1
#define FALSE 0

typedef struct {
	int* vars;
	int* args;
    int* locals;
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
	DROP,	// 4
	DUP,	// 5
	EQ,	// 6
	EQZ,	// 7
	HALT,	// 8
	INC,	// 9
	JP,	// 10
	JPNZ,	// 11
	JPZ,	// 12
	LD,	// 13
	LDARG,	// 14
	LOAD,	// 15
	LSH,	// 16
	LT,	// 17
	MOD,	// 18
	MUL,	// 19
	NA,	// 20
	NOP,	// 21
	OR,	// 22
	PRINT,	// 23
	PRNT,	// 24
	RET,	// 25
	RSH,	// 26
	SET,	// 27
	SETZ,	// 28
	ST,	// 29
	STARG,	// 30
	STORE,	// 31
	SUB	// 32
};

VM* newVM(int* code, int pc, int datasize);
void freeVM(VM* vm);
void run(VM* vm);

/* EOF */
