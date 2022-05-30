#include <stdio.h>
#include <stdlib.h>

#define STACK_SIZE 200
#define TRUE 1
#define FALSE 0

typedef struct {
	int* vars;
	int* code;
	int* stack;
	int pc;
	int sp;
	int fp;
} VM;

enum {
	NA,
	NOP,
	RET,
	ADD,
	SUB,
	MUL,
	LT,
	EQ,
	JP,
	JPNZ,
	JPZ,
	SET,
	LD,
	LOAD,
	ST,
	STORE,
	PRINT,
	HALT,
	CALL,
	EQZ,
	SETZ,
	LDARG,
	INC,
	DEC,

// "forthified"
	DROP,
	SWAP,
	DUP,
	TWODUP,
	ROT,
	OVER
};

VM* newVM(int* code, int pc, int datasize);
void freeVM(VM* vm);
void run(VM* vm);


/* EOF */
