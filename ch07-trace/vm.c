/*
 * Chapter 7: watching the machine run.
 *
 * The machine is the machine of chapter 6. What is new is that it can
 * show what it is doing:
 *
 *     vm program.vm           run, as before
 *     vm -t program.vm        run, and trace every step on stderr
 *     vm -d program.vm        run under the debugger, one command at a time
 *
 * To do that the machine needs to know the names of its own
 * instructions, and its main loop is split in two: step() runs one
 * instruction, and the trace, the debugger, and plain running are
 * three different ways of calling it.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum {
    HALT, PUSH, ADD, SUB, MUL, PRINT,
    JMP, JZ, DUP, DROP, SWAP, OVER, ROT, LT, EQ,
    LOAD, STORE, CALL, RET,
    DIV, MOD,
    NOPS
};

/* What each instruction is called, and how many operands follow it. */
static const char *names[NOPS] = {
    "HALT", "PUSH", "ADD", "SUB", "MUL", "PRINT",
    "JMP", "JZ", "DUP", "DROP", "SWAP", "OVER", "ROT", "LT", "EQ",
    "LOAD", "STORE", "CALL", "RET",
    "DIV", "MOD"
};

static const int noperands[NOPS] = {
    [PUSH] = 1, [JMP] = 1, [JZ] = 1, [LOAD] = 1, [STORE] = 1, [CALL] = 2
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
static int pc = 0;
static int start;
static int halted = 0;
static int debugging = 0;

static void show_stack(FILE *out);

static void trap(const char *why) {
    fflush(stdout);
    fprintf(stderr, "trap: %s at %d\n", why, start);
    if (debugging) {
        fprintf(stderr, "stack: ");
        show_stack(stderr);
        fprintf(stderr, "\n");
    }
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

/*
 * Write the instruction at address at, with its operands, as text:
 * "CALL 17 2". Returns the number of characters written, so that
 * callers can line things up.
 */
static int show_instruction(FILE *out, int at) {
    int op, i, n;

    if (at < 0 || at >= code_len)
        return fprintf(out, "(outside the program)");
    op = code[at];
    if (op < 0 || op >= NOPS)
        return fprintf(out, ".word %d", op);
    n = fprintf(out, "%s", names[op]);
    for (i = 1; i <= noperands[op] && at + i < code_len; i++)
        n += fprintf(out, " %d", code[at + i]);
    return n;
}

/*
 * Write the stack, bottom first, with a bar where each frame begins:
 *
 *     1071 462 | 462 147 | 147 21
 *
 * Here main has pushed 1071 and 462, and two calls are active.
 */
static void show_stack(FILE *out) {
    int i, f = 1;
    const char *sep = "";

    for (i = 0; i <= sp; i++) {
        while (f <= fsp && (f < fsp ? frames[f].fp : fp) == i) {
            fprintf(out, "%s|", sep);
            sep = " ";
            f++;
        }
        if (i < sp) {
            fprintf(out, "%s%d", sep, stack[i]);
            sep = " ";
        }
    }
}

/* Run one instruction. Returns 0 once the machine has halted. */
static int step(void) {
    int op, a, b;

    if (halted)
        return 0;
    start = pc;
    if (pc < 0 || pc >= code_len)
        trap("ran off the end of the program");
    op = code[pc++];

        switch (op) {
        case HALT:
            halted = 1;
            return 0;
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
    return 1;
}

static void run(void) {
    while (step())
        ;
}

/*
 * Tracing: after every instruction, write a line to stderr with the
 * step number, the address, the instruction, and the stack after it.
 * The lines can be saved in a file and explored with replay.py.
 */
static void trace(void) {
    long n = 0;
    int at, going, width;

    do {
        at = pc;
        going = step();
        fflush(stdout);
        fprintf(stderr, "%6ld %5d  ", ++n, at);
        width = show_instruction(stderr, at);
        if (sp > 0 || fsp > 0) {
            fprintf(stderr, "%*s  ", width < 14 ? 14 - width : 0, "");
            show_stack(stderr);
        }
        fprintf(stderr, "\n");
    } while (going);
}

/*
 * The debugger. It reads commands from standard input, one per line:
 *
 *     s [n]       step one instruction, or n
 *     c           continue until a breakpoint or the end
 *     b addr      set a breakpoint at addr
 *     d addr      delete the breakpoint at addr
 *     p           print the stack and the frames
 *     l [n]       list the next instruction, or the next n
 *     q           quit
 *
 * Everything it says goes to standard output, as does what the
 * program prints, so the two appear in the order they happen.
 */

static char breakpoint[65536];

static void where(void) {
    if (halted) {
        printf("halted\n");
        return;
    }
    printf("%5d  ", pc);
    show_instruction(stdout, pc);
    printf("\n");
}

static void list(int n) {
    int at = pc;

    while (n-- > 0 && at >= 0 && at < code_len) {
        printf("%5d %c ", at, breakpoint[at] ? '*' : ' ');
        show_instruction(stdout, at);
        printf("\n");
        if (code[at] >= 0 && code[at] < NOPS)
            at += 1 + noperands[code[at]];
        else
            at += 1;
    }
}

static void print_state(void) {
    int f;

    printf("stack: ");
    show_stack(stdout);
    printf("\n");
    for (f = fsp; f > 0; f--)
        printf("frame %d: returns to %d, locals start at %d\n",
               f, frames[f - 1].ret, f == fsp ? fp : frames[f].fp);
}

static void debug(void) {
    char line[256], cmd[16];
    int n, arg;

    debugging = 1;
    where();
    for (;;) {
        printf("(vm) ");
        fflush(stdout);
        if (fgets(line, sizeof line, stdin) == NULL)
            break;
        n = sscanf(line, "%15s %d", cmd, &arg);
        if (n < 1)
            continue;
        if (strcmp(cmd, "q") == 0) {
            break;
        } else if (strcmp(cmd, "s") == 0) {
            int count = n == 2 ? arg : 1;
            while (count-- > 0 && step())
                ;
            where();
        } else if (strcmp(cmd, "c") == 0) {
            if (step())
                while (!breakpoint[pc] && step())
                    ;
            where();
        } else if ((strcmp(cmd, "b") == 0 || strcmp(cmd, "d") == 0) && n == 2) {
            if (arg < 0 || arg >= code_len)
                printf("no address %d in the program\n", arg);
            else
                breakpoint[arg] = cmd[0] == 'b';
        } else if (strcmp(cmd, "p") == 0) {
            print_state();
        } else if (strcmp(cmd, "l") == 0) {
            list(n == 2 ? arg : 1);
        } else {
            printf("commands: s [n], c, b addr, d addr, p, l [n], q\n");
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
    const char *usage = "usage: vm [-t | -d] program.vm\n";

    if (argc == 2) {
        load(argv[1]);
        run();
    } else if (argc == 3 && strcmp(argv[1], "-t") == 0) {
        load(argv[2]);
        trace();
    } else if (argc == 3 && strcmp(argv[1], "-d") == 0) {
        load(argv[2]);
        debug();
    } else {
        fprintf(stderr, "%s", usage);
        return 2;
    }
    return 0;
}
