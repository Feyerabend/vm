/*
 * Chapter 6: the machine is exactly the machine of chapter 5.
 *
 * What is new in this chapter are the tools around it: asm.py, which
 * turns assembly language with labels into .vm files, and disasm.py,
 * which turns .vm files back into assembly language.
 *
 *     usage: vm program.vm
 */

#include <stdio.h>
#include <stdlib.h>

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

static const int *code;     /* the program, once loaded */
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
 * Read a whole file into memory, check that it is a program, and
 * point code at its instructions. Nothing in the file is trusted:
 * every check that a file could fail is made here, before anything
 * runs. Problems with the file are not traps, since no instruction
 * has run; they are reported differently and exit with status 2.
 */

#define MAX_CODE 65536

static int words[MAX_CODE];

static void bad_file(const char *path, const char *why) {
    fprintf(stderr, "%s: %s\n", path, why);
    exit(2);
}

/* A 32-bit little-endian word, whatever the byte order of this computer. */
static long word32(const unsigned char *b) {
    unsigned long u = (unsigned long) b[0]
                    | (unsigned long) b[1] << 8
                    | (unsigned long) b[2] << 16
                    | (unsigned long) b[3] << 24;
    if (u >= 0x80000000UL)
        return (long) (u - 0x80000000UL) - 0x7fffffffL - 1;
    return (long) u;
}

static void load(const char *path) {
    unsigned char header[8], b[4];
    long n, i;
    FILE *f = fopen(path, "rb");

    if (f == NULL)
        bad_file(path, "cannot open");
    if (fread(header, 1, 8, f) != 8)
        bad_file(path, "too short to be a program");
    if (header[0] != 'S' || header[1] != 'V' || header[2] != 'M')
        bad_file(path, "not a program (wrong magic number)");
    if (header[3] != 1)
        bad_file(path, "unknown format version");
    n = word32(header + 4);
    if (n < 1 || n > MAX_CODE)
        bad_file(path, "bad code length");
    for (i = 0; i < n; i++) {
        if (fread(b, 1, 4, f) != 4)
            bad_file(path, "code ends early");
        words[i] = (int) word32(b);
    }
    if (fgetc(f) != EOF)
        bad_file(path, "extra bytes after the code");
    fclose(f);

    code = words;
    code_len = (int) n;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: vm program.vm\n");
        return 2;
    }
    load(argv[1]);
    run();
    return 0;
}
