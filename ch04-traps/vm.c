/*
 * Chapter 4: traps.
 *
 * Up to now a bad program made the machine misbehave in whatever way
 * the C underneath happened to: read garbage, write over memory, or
 * crash. This chapter makes the machine check every step and stop
 * cleanly with a message saying what went wrong and where. Such a
 * stop is called a trap.
 *
 * New since chapter 3: DIV and MOD, and checks on everything.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum {
    HALT,
    PUSH,
    ADD,
    SUB,
    MUL,
    PRINT,
    JMP,
    JZ,
    DUP,
    DROP,
    SWAP,
    OVER,
    ROT,
    LT,
    EQ,
    LOAD,
    STORE,
    CALL,
    RET,
    DIV,        /* a b -> a / b, trap if b == 0                */
    MOD         /* a b -> a % b, trap if b == 0                */
};

#define STACK_SIZE 256
#define FRAMES 256

static int stack[STACK_SIZE];
static int sp = 0;

struct frame {
    int ret;
    int fp;
};

static struct frame frames[FRAMES];
static int fsp = 0;
static int fp = 0;

static const int *code;
static int code_len;
static int pc;
static int start;               /* address of the instruction being run */

/*
 * Stop the machine. The message names the instruction that was
 * running, not wherever pc happens to point by now.
 */
static void trap(const char *why) {
    fflush(stdout);
    fprintf(stderr, "trap: %s at %d\n", why, start);
    exit(1);
}

static void push(int v) {
    if (sp == STACK_SIZE)
        trap("stack overflow");
    stack[sp++] = v;
}

static int pop(void) {
    if (sp == fp)
        trap("stack underflow");
    return stack[--sp];
}

static int operand(void) {
    if (pc >= code_len)
        trap("missing operand");
    return code[pc++];
}

static int address(void) {
    int addr = operand();
    if (addr < 0 || addr >= code_len)
        trap("jump out of program");
    return addr;
}

static int local(void) {
    int k = operand();
    if (k < 0 || fp + k >= sp)
        trap("no such local");
    return fp + k;
}

static void run(void) {
    pc = 0;

    for (;;) {
        int op, a, b;

        start = pc;
        if (pc < 0 || pc >= code_len)
            trap("ran off the end of the program");
        op = code[pc++];

        switch (op) {
        case HALT:
            return;
        case PUSH:
            push(operand());
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
            pc = address();
            break;
        case JZ:
            b = address();
            a = pop();
            if (a == 0)
                pc = b;
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
        case LOAD:
            a = local();
            push(stack[a]);
            break;
        case STORE:
            a = local();
            stack[a] = pop();
            break;
        case CALL: {
            int addr = address();
            int nargs = operand();
            if (nargs < 0 || nargs > sp - fp)
                trap("not enough arguments");
            if (fsp == FRAMES)
                trap("too many nested calls");
            frames[fsp].ret = pc;
            frames[fsp].fp = fp;
            fsp++;
            fp = sp - nargs;
            pc = addr;
            break;
        }
        case RET:
            if (fsp == 0)
                trap("return without call");
            a = pop();
            sp = fp;
            fsp--;
            pc = frames[fsp].ret;
            fp = frames[fsp].fp;
            push(a);
            break;
        case DIV:
            b = pop();
            a = pop();
            if (b == 0)
                trap("division by zero");
            push(a / b);
            break;
        case MOD:
            b = pop();
            a = pop();
            if (b == 0)
                trap("division by zero");
            push(a % b);
            break;
        default:
            trap("unknown instruction");
        }
    }
}

/*
 * gcd(a, b): gcd(a, 0) = a, otherwise gcd(b, a mod b).
 * Then the machine is made to fail on purpose: see the programs below.
 */
static const int gcd[] = {
    /* main: */
    /*  0 */ PUSH, 1071,
    /*  2 */ PUSH, 462,
    /*  4 */ CALL, 17, 2,       /* gcd(1071, 462)        */
    /*  7 */ PRINT,
    /*  8 */ PUSH, 17,
    /* 10 */ PUSH, 5,
    /* 12 */ CALL, 17, 2,       /* gcd(17, 5)            */
    /* 15 */ PRINT,
    /* 16 */ HALT,

    /* gcd: */
    /* 17 */ LOAD, 1,
    /* 19 */ JZ, 32,            /* b = 0: return a       */
    /* 21 */ LOAD, 1,           /* b                     */
    /* 23 */ LOAD, 0,
    /* 25 */ LOAD, 1,
    /* 27 */ MOD,               /* a mod b               */
    /* 28 */ CALL, 17, 2,       /* gcd(b, a mod b)       */
    /* 31 */ RET,
    /* 32 */ LOAD, 0,
    /* 34 */ RET
};

/* Each of these is broken in a different way. */

static const int divzero[] = {
    PUSH, 1, PUSH, 0, DIV, PRINT, HALT
};

static const int underflow[] = {
    PUSH, 1, ADD, PRINT, HALT
};

/* Recursion that never stops, and that fills the stack: f(n) = f(n + 1). */
static const int deep[] = {
    /* 0 */ PUSH, 0,
    /* 2 */ CALL, 5, 1,
    /* 5 */ LOAD, 0,
    /* 7 */ PUSH, 1,
    /* 9 */ ADD,
    /* 10 */ CALL, 5, 1,
    /* 13 */ RET
};

/* Recursion that never stops, with no arguments: only frames pile up. */
static const int forever[] = {
    /* 0 */ CALL, 3, 0,
    /* 3 */ CALL, 3, 0
};

static const int badop[] = {
    PUSH, 1, 99, HALT
};

static const int runoff[] = {
    PUSH, 1, PRINT
};

static const int badjump[] = {
    JMP, 1000
};

static const int badret[] = {
    PUSH, 1, RET
};

#define PROGRAM(p) { #p, p, sizeof p / sizeof p[0] }

static const struct {
    const char *name;
    const int *code;
    int len;
} programs[] = {
    PROGRAM(gcd),
    PROGRAM(divzero),
    PROGRAM(underflow),
    PROGRAM(deep),
    PROGRAM(forever),
    PROGRAM(badop),
    PROGRAM(runoff),
    PROGRAM(badjump),
    PROGRAM(badret)
};

int main(int argc, char *argv[]) {
    const char *name = argc > 1 ? argv[1] : "gcd";
    size_t i;

    for (i = 0; i < sizeof programs / sizeof programs[0]; i++) {
        if (strcmp(name, programs[i].name) == 0) {
            code = programs[i].code;
            code_len = programs[i].len;
            run();
            return 0;
        }
    }
    fprintf(stderr, "no program called %s\n", name);
    return 2;
}
