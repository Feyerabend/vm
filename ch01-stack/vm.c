/*
 * Chapter 1: a stack machine.
 *
 * The whole machine is three things: an array of code, a program
 * counter pointing into it, and a stack of integers. Each step reads
 * one instruction at pc and does what it says. That is all.
 *
 * The program is written directly into the C source below. Changing
 * the program means recompiling the machine, which we fix in chapter 5.
 */

#include <stdio.h>

enum {
    HALT,       /* stop the machine                          */
    PUSH,       /* PUSH n: push the number n                 */
    ADD,        /* pop b, pop a, push a + b                  */
    SUB,        /* pop b, pop a, push a - b                  */
    MUL,        /* pop b, pop a, push a * b                  */
    PRINT       /* pop a, print it on a line of its own      */
};

#define STACK_SIZE 256

static int stack[STACK_SIZE];
static int sp = 0;              /* number of values on the stack */

static void push(int v) {
    stack[sp++] = v;
}

static int pop(void) {
    return stack[--sp];
}

static void run(const int *code) {
    int pc = 0;

    for (;;) {
        int op = code[pc++];
        int a, b;

        switch (op) {
        case HALT:
            return;
        case PUSH:
            push(code[pc++]);
            break;
        case ADD:
            b = pop();
            a = pop();
            push(a + b);
            break;
        case SUB:
            b = pop();
            a = pop();
            push(a - b);
            break;
        case MUL:
            b = pop();
            a = pop();
            push(a * b);
            break;
        case PRINT:
            printf("%d\n", pop());
            break;
        }
    }
}

/* (2 + 3) * 7 - 5, then 6 * 7 */
static const int program[] = {
    PUSH, 2,
    PUSH, 3,
    ADD,
    PUSH, 7,
    MUL,
    PUSH, 5,
    SUB,
    PRINT,
    PUSH, 6,
    PUSH, 7,
    MUL,
    PRINT,
    HALT
};

int main(void) {
    run(program);
    return 0;
}
