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
	ADD,
	DEC,
	EQ,
	EQZ,
	HALT,
	INC,
	JP,
	JPNZ,
	JPZ,
	LD,
	LOAD,
	LT,
	MUL,
	NA,
	NOP,
	PRINT,
	SET,
	SETZ,
	ST,
	STORE,
	SUB,

// "forthified"
	DROP,
	DUP,
	OVER,
	ROT,
	SWAP,
	TWODUP
};

VM* newVM(int* code, int pc, int datasize);
void freeVM(VM* vm);
void run(VM* vm);


/* EOF */
