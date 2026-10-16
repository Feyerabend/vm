/*
 * Chapter 3: calls and frames.
 *
 * A function needs three things the machine does not yet have: a
 * way to come back to where it was called from, a place for its own
 * values that the caller's values are safe from, and a way to hand
 * a result back. New since chapter 2: LOAD, STORE, CALL, RET.
 *
 * Each call gets a frame: a record of where to return to and where
 * its arguments begin on the stack. Frames live on a stack of their
 * own, so a function can call itself and every call still finds its
 * own values.
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
    EQ,         /* a b     -> (a == b) as 1 or 0               */
    LOAD,       /* LOAD k: push local k of the current frame   */
    STORE,      /* STORE k: pop into local k                   */
    CALL,       /* CALL addr n: call addr with n arguments     */
    RET         /* pop result, drop the frame, push result     */
};

#define STACK_SIZE 256

#define FRAMES 256

static int stack[STACK_SIZE];
static int sp = 0;

/*
 * A frame remembers where to go back to (ret), and where on the data
 * stack this call's locals begin (fp). The arguments a caller pushed
 * become locals 0, 1, ... of the called function.
 */
struct frame {
    int ret;
    int fp;
};

static struct frame frames[FRAMES];
static int fsp = 0;             /* number of frames in use */
static int fp = 0;              /* locals of the current call start here */

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
        case LOAD:
            push(stack[fp + code[pc++]]);
            break;
        case STORE:
            stack[fp + code[pc++]] = pop();
            break;
        case CALL: {
            int addr = code[pc++];
            int nargs = code[pc++];
            frames[fsp].ret = pc;
            frames[fsp].fp = fp;
            fsp++;
            fp = sp - nargs;
            pc = addr;
            break;
        }
        case RET:
            a = pop();
            sp = fp;
            fsp--;
            pc = frames[fsp].ret;
            fp = frames[fsp].fp;
            push(a);
            break;
        }
    }
}

/*
 * Factorial, recursively:
 *
 *     fact(n) = 1                  if n < 2
 *     fact(n) = n * fact(n - 1)    otherwise
 *
 * Every call to fact has its own frame, so each finds its own n as
 * local 0, however deep the recursion goes.
 */
static const int program[] = {
    /* main: */
    /*  0 */ PUSH, 5,
    /*  2 */ CALL, 13, 1,       /* fact(5)               */
    /*  5 */ PRINT,
    /*  6 */ PUSH, 10,
    /*  8 */ CALL, 13, 1,       /* fact(10)              */
    /* 11 */ PRINT,
    /* 12 */ HALT,

    /* fact: */
    /* 13 */ LOAD, 0,
    /* 15 */ PUSH, 2,
    /* 17 */ LT,
    /* 18 */ JZ, 23,            /* n >= 2: go recurse    */
    /* 20 */ PUSH, 1,
    /* 22 */ RET,               /* return 1              */
    /* recurse: */
    /* 23 */ LOAD, 0,           /* n                     */
    /* 25 */ LOAD, 0,
    /* 27 */ PUSH, 1,
    /* 29 */ SUB,               /* n - 1                 */
    /* 30 */ CALL, 13, 1,       /* fact(n - 1)           */
    /* 33 */ MUL,               /* n * fact(n - 1)       */
    /* 34 */ RET
};

int main(void) {
    run(program);
    return 0;
}
