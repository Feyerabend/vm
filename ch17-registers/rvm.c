/*
 * Chapter 17: a register machine.
 *
 * It runs programs translated from the stack machine by translate.py.
 * Where a stack machine says ADD, and finds its operands on top of the
 * stack, a register machine says ADD r1, r1, r3: where its operands
 * are, and where its result goes. Instructions are bigger, but there
 * are fewer of them: no LOAD to fetch a value before using it, and no
 * STORE to put it back.
 *
 * Registers are numbered within a window: the registers of the current
 * call. A call's window starts where its arguments are in the caller's
 * window, so passing arguments copies nothing, and the result comes
 * back in the first register of the window. Lua's virtual machine
 * works the same way.
 *
 * Each instruction is five numbers: the opcode, three operands, and
 * the address of the stack-machine instruction it was translated
 * from. Traps report that address, so they say the same as the stack
 * machine would.
 *
 * The heap is chapter 13's: blocks are made, and never freed.
 *
 *     rvm [-c] program.rvm
 *
 * -c prints the number of instructions run, on stderr.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum {
    HALT, MOVI, MOV, SWAPR, ROTR,
    ADD, SUB, MUL, DIV, MOD, AND, OR, XOR, LT, EQ,
    ADDI, SUBI, MULI, DIVI, MODI, ANDI, ORI, XORI, LTI, EQI,
    PRINT, EMIT, JMP, JZ, CALL, RET,
    LOADM, STOREM, NEW, GETF, SETF, LEN, TRAP,
    NOPS
};

/*
 * TRAP x stops the machine with message x. The translator puts it
 * where it can see, before running, that the stack machine would
 * trap: an ADD with one value in the frame, a jump to 9999.
 */
static const char *messages[] = {
    "unknown instruction", "missing operand", "ran off the end of the program",
    "jump out of program", "stack underflow", "no such local",
    "not enough arguments", "return without call", "stack overflow"
};

#define WIDTH 5                 /* words per instruction */
#define REGISTERS 256
#define FRAMES 256
#define MEMORY_SIZE 4096
#define HEAP_SIZE 65536
#define HEADER 2

struct value {
    int is_ref;
    int n;
};

static struct value regs[REGISTERS];
static int base = 0;            /* where the current window starts */

struct frame {
    int ret;
    int base;
};

static struct frame frames[FRAMES];
static int fsp = 0;

static struct value memory[MEMORY_SIZE];
static struct value heap[HEAP_SIZE];
static int heap_used = 0;
static int blocks_made = 0;

static int *code;
static int code_len;            /* in instructions */
static int start;
static long steps = 0;

static void trap(const char *why) {
    fflush(stdout);
    fprintf(stderr, "trap: %s at %d\n", why, start);
    exit(1);
}

static struct value integer(int n) {
    struct value v = { 0, n };
    return v;
}

static int number(struct value v) {
    if (v.is_ref)
        trap("not a number");
    return v.n;
}

static int block(struct value v) {
    if (!v.is_ref)
        trap("not a reference");
    return v.n;
}

static struct value allocate(int n) {
    struct value r;
    int i;

    if (n < 0)
        trap("bad size");
    if (n > HEAP_SIZE - HEADER - heap_used)
        trap("out of memory");
    heap[heap_used] = integer(n);
    heap[heap_used + 1] = integer(++blocks_made);
    for (i = 0; i < n; i++)
        heap[heap_used + HEADER + i] = integer(0);
    r.is_ref = 1;
    r.n = heap_used;
    heap_used += HEADER + n;
    return r;
}

static int field(int b, int i) {
    if (i < 0 || i >= heap[b].n)
        trap("index out of bounds");
    return b + HEADER + i;
}

static int to_int(uint32_t u) {
    if (u <= INT32_MAX)
        return (int) u;
    return -(int) (UINT32_MAX - u) - 1;
}

/* The ten operations with two operands, as in the stack machine. */
static int arith(int op, int a, int b) {
    switch (op) {
    case ADD: return to_int((uint32_t) a + (uint32_t) b);
    case SUB: return to_int((uint32_t) a - (uint32_t) b);
    case MUL: return to_int((uint32_t) a * (uint32_t) b);
    case AND: return a & b;
    case OR:  return a | b;
    case XOR: return a ^ b;
    case LT:  return a < b;
    case EQ:  return a == b;
    }
    if (b == 0)
        trap("division by zero");
    if (op == DIV)
        return b == -1 ? to_int(0u - (uint32_t) a) : a / b;
    return b == -1 ? 0 : a % b;
}

#define R(x) regs[base + (x)]

static void run(void) {
    int pc = 0;

    for (;;) {
        int *i = &code[pc * WIDTH];
        int op = i[0], x = i[1], y = i[2], z = i[3];

        start = i[4];
        steps++;
        pc++;
        switch (op) {
        case HALT:
            return;
        case MOVI:
            R(x) = integer(y);
            break;
        case MOV:
            R(x) = R(y);
            break;
        case SWAPR: {
            struct value t = R(x);
            R(x) = R(y);
            R(y) = t;
            break;
        }
        case ROTR: {
            struct value t = R(x);
            R(x) = R(y);
            R(y) = R(z);
            R(z) = t;
            break;
        }
        case ADD: case SUB: case MUL: case DIV: case MOD:
        case AND: case OR: case XOR: case LT: {
            int a = number(R(y)), b = number(R(z));
            R(x) = integer(arith(op, a, b));
            break;
        }
        case EQ:
            R(x) = integer(R(y).is_ref == R(z).is_ref && R(y).n == R(z).n);
            break;
        case ADDI: case SUBI: case MULI: case DIVI: case MODI:
        case ANDI: case ORI: case XORI: case LTI:
            R(x) = integer(arith(op - ADDI + ADD, number(R(y)), z));
            break;
        case EQI:
            R(x) = integer(!R(y).is_ref && R(y).n == z);
            break;
        case PRINT:
            printf("%d\n", number(R(x)));
            break;
        case EMIT: {
            int c = number(R(x));
            if (c < 0 || c > 255)
                trap("not a character");
            putchar(c);
            break;
        }
        case JMP:
            pc = x;
            break;
        case JZ:
            if (!R(x).is_ref && R(x).n == 0)
                pc = y;
            break;
        case CALL:
            if (fsp == FRAMES)
                trap("too many nested calls");
            if (base + y + z > REGISTERS)
                trap("stack overflow");
            frames[fsp].ret = pc;
            frames[fsp].base = base;
            fsp++;
            base += y;
            pc = x;
            break;
        case RET:
            regs[base] = R(x);
            fsp--;
            pc = frames[fsp].ret;
            base = frames[fsp].base;
            break;
        case LOADM: {
            int a = number(R(y));
            if (a < 0 || a >= MEMORY_SIZE)
                trap("no such memory address");
            R(x) = memory[a];
            break;
        }
        case STOREM: {
            int a = number(R(x));
            if (a < 0 || a >= MEMORY_SIZE)
                trap("no such memory address");
            memory[a] = R(y);
            break;
        }
        case NEW:
            R(x) = allocate(number(R(y)));
            break;
        case GETF: {
            int b = block(R(y));
            R(x) = heap[field(b, number(R(z)))];
            break;
        }
        case SETF: {
            int b = block(R(x));
            heap[field(b, number(R(y)))] = R(z);
            break;
        }
        case LEN:
            R(x) = integer(heap[block(R(y))].n);
            break;
        case TRAP:
            trap(messages[x]);
            break;
        default:
            trap("unknown instruction");
        }
    }
}

static long word32(const unsigned char *b) {
    unsigned long u = (unsigned long) b[0]
                    | (unsigned long) b[1] << 8
                    | (unsigned long) b[2] << 16
                    | (unsigned long) b[3] << 24;
    if (u >= 0x80000000UL)
        return (long) (u - 0x80000000UL) - 0x7fffffffL - 1;
    return (long) u;
}

/* The file is like a .vm file, with RVM for its magic number. The
 * translator has checked the program; the loader checks the file. */
static void load(const char *path) {
    unsigned char header[8], b[4];
    long n, k;
    FILE *f = fopen(path, "rb");

    if (f == NULL || fread(header, 1, 8, f) != 8 || memcmp(header, "RVM\1", 4) != 0) {
        fprintf(stderr, "%s: not a register machine program\n", path);
        exit(2);
    }
    n = word32(header + 4);
    if (n < WIDTH || n % WIDTH != 0) {
        fprintf(stderr, "%s: bad code length\n", path);
        exit(2);
    }
    code = malloc(n * sizeof (int));
    for (k = 0; k < n; k++) {
        if (fread(b, 1, 4, f) != 4) {
            fprintf(stderr, "%s: code ends early\n", path);
            exit(2);
        }
        code[k] = (int) word32(b);
    }
    fclose(f);
    code_len = (int) (n / WIDTH);
}

static int counting = 0;

static void report(void) {
    if (counting) {
        fflush(stdout);
        fprintf(stderr, "steps: %ld\n", steps);
    }
}

int main(int argc, char *argv[]) {
    if (argc == 3 && strcmp(argv[1], "-c") == 0) {
        counting = 1;
        load(argv[2]);
    } else if (argc == 2) {
        load(argv[1]);
    } else {
        fprintf(stderr, "usage: rvm [-c] program.rvm\n");
        return 2;
    }
    atexit(report);
    run();
    return 0;
}
