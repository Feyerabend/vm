/*
 * Chapter 2: jumps.
 *
 * A machine that can only go forward computes one fixed expression.
 * Let it set pc to somewhere else, and let that depend on a value,
 * and it can repeat and decide. New since chapter 1: JMP, JZ, DUP,
 * DROP, SWAP, OVER, ROT, LT, EQ.
 */

#include <stdio.h>

enum {
    HALT,
    PUSH,
    ADD,
    SUB,
    MUL,
    PRINT,
    JMP,        /* JMP addr: continue at addr                  */
    JZ,         /* JZ addr: pop a, continue at addr if a == 0  */
    DUP,        /* a       -> a a                              */
    DROP,       /* a       ->                                  */
    SWAP,       /* a b     -> b a                              */
    OVER,       /* a b     -> a b a                            */
    ROT,        /* a b c   -> b c a                            */
    LT,         /* a b     -> (a < b)  as 1 or 0               */
    EQ          /* a b     -> (a == b) as 1 or 0               */
};

#define STACK_SIZE 256

static int stack[STACK_SIZE];
static int sp = 0;

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
        case JMP:
            pc = code[pc];
            break;
        case JZ:
            a = pop();
            if (a == 0)
                pc = code[pc];
            else
                pc++;
            break;
        case DUP:
            a = pop();
            push(a);
            push(a);
            break;
        case DROP:
            pop();
            break;
        case SWAP:
            b = pop();
            a = pop();
            push(b);
            push(a);
            break;
        case OVER:
            b = pop();
            a = pop();
            push(a);
            push(b);
            push(a);
            break;
        case ROT: {
            int c = pop();
            b = pop();
            a = pop();
            push(b);
            push(c);
            push(a);
            break;
        }
        case LT:
            b = pop();
            a = pop();
            push(a < b);
            break;
        case EQ:
            b = pop();
            a = pop();
            push(a == b);
            break;
        }
    }
}

/*
 * The first ten Fibonacci numbers.
 *
 * The stack holds: a b n, where n counts down to zero.
 * Each round prints a, then replaces a b with b (a + b).
 *
 * The numbers on the left are addresses: where each instruction
 * starts in the array. Jumps refer to them, which is why they are
 * worth writing down. Counting them by hand is error-prone, and is
 * exactly the job the assembler in chapter 6 takes over.
 */
static const int program[] = {
    /*  0 */ PUSH, 0,           /* a                     */
    /*  2 */ PUSH, 1,           /* b                     */
    /*  4 */ PUSH, 10,          /* n                     */
    /* loop: */
    /*  6 */ DUP, JZ, 22,       /* a b n, leave if n = 0 */
    /*  9 */ PUSH, 1, SUB,      /* a b n-1               */
    /* 12 */ ROT, ROT,          /* n a b                 */
    /* 14 */ OVER, PRINT,       /* print a               */
    /* 16 */ SWAP, OVER, ADD,   /* n b (a + b)           */
    /* 19 */ ROT,               /* b (a + b) n           */
    /* 20 */ JMP, 6,
    /* end: */
    /* 22 */ HALT
};

int main(void) {
    run(program);
    return 0;
}
