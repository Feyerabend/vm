#include <stdio.h>
#include <stdlib.h>

#define STACK_SIZE 200
#define TRUE 1
#define FALSE 0


typedef struct {
	int* code;
	int* stack;
	int pc;
	int sp;
	int fp;
} VM;

enum {
	NA,
	HALT,
	ADD,
	SUB,
	MUL,
	SET,
	PRINT
};

VM* newVM(int* code, int pc);
void freeVM(VM* vm);
void run(VM* vm);

/* EOF */
