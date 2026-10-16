/*
 * Chapter 14: garbage collection.
 *
 * The machine of chapter 13, which never freed anything, now
 * reclaims every block that can no longer be reached. It has two
 * ways of doing it, chosen when it starts:
 *
 *   mark and sweep    Find every reachable block and mark it. Then go
 *                     through the whole heap, and give every unmarked
 *                     block back to a list of free space.
 *
 *   copying           Keep two heaps, and use one at a time. When it
 *                     is full, copy every reachable block into the
 *                     other, and carry on there. What was not copied
 *                     is simply left behind.
 *
 * Neither changes anything a program can see. Block numbers stay the
 * same even when blocks move, so a trace is the same line for line,
 * whichever collector runs.
 *
 *     vm [options] program.vm
 *
 *     -t          trace every step on stderr
 *     -d          run under the debugger
 *     -g mark     collect by mark and sweep (the default)
 *     -g copy     collect by copying
 *     -S          stress: collect before every NEW, to flush out bugs
 *     -s          print statistics about the heap at the end
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

enum {
    HALT, PUSH, ADD, SUB, MUL, PRINT,
    JMP, JZ, DUP, DROP, SWAP, OVER, ROT, LT, EQ,
    LOAD, STORE, CALL, RET,
    DIV, MOD,
    AND, OR, XOR, LOADM, STOREM, EMIT,
    NEW, GETF, SETF, LEN,
    NOPS
};

/* What each instruction is called, and how many operands follow it. */
static const char *names[NOPS] = {
    "HALT", "PUSH", "ADD", "SUB", "MUL", "PRINT",
    "JMP", "JZ", "DUP", "DROP", "SWAP", "OVER", "ROT", "LT", "EQ",
    "LOAD", "STORE", "CALL", "RET",
    "DIV", "MOD",
    "AND", "OR", "XOR", "LOADM", "STOREM", "EMIT",
    "NEW", "GETF", "SETF", "LEN"
};

static const int noperands[NOPS] = {
    [PUSH] = 1, [JMP] = 1, [JZ] = 1, [LOAD] = 1, [STORE] = 1, [CALL] = 2
};

/*
 * A value: an integer, or a reference to a block on the heap. For a
 * reference, n is where the block starts in the heap array.
 */
struct value {
    int is_ref;
    int n;
};

#define STACK_SIZE 256
#define FRAMES 256
#define MEMORY_SIZE 4096

/*
 * The heap is an array of values. A block of n values takes n + 2
 * places: a header of two, then the values.
 *
 *     heap[b]         length n, and in its tag field: the block's state
 *     heap[b + 1]     the block's number
 *     heap[b + 2]     value 0
 *     ...
 *
 * The first header word is never a value, so its tag field is free
 * for the collectors to use: it says whether a block is marked, or is
 * free space, or has been copied elsewhere.
 *
 * Free space, under mark and sweep, is kept in chunks that look much
 * like blocks:
 *
 *     heap[c]         FREE, and the size of the chunk in places
 *     heap[c + 1]     where the next free chunk starts, or -1
 *
 * Every block takes at least two places, so every gap left behind by
 * a block is big enough to be a chunk.
 */
#define HEAP_SIZE 65536
#define HEADER 2

enum { UNMARKED, MARKED, FREE, FORWARDED };
enum { MARK_SWEEP, COPYING };

/* Two spaces, for the copying collector. Mark and sweep uses one. */
static struct value space_a[HEAP_SIZE];
static struct value space_b[HEAP_SIZE];
static struct value *heap = space_a;
static int blocks_made = 0;

static int collector = MARK_SWEEP;
static int stress = 0;
static int statistics = 0;

static int free_list = -1;      /* mark and sweep: the first free chunk */
static int top = 0;             /* copying: the next free place */

static long collections = 0;
static long words_allocated = 0;
static long words_freed = 0;    /* mark and sweep */
static long words_copied = 0;   /* copying */
static long most_live = 0;
static clock_t gc_time = 0;

static struct value stack[STACK_SIZE];
static struct value memory[MEMORY_SIZE];
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

static struct value integer(int n) {
    struct value v = { 0, n };
    return v;
}

static void push(struct value v) {
    if (sp == STACK_SIZE)
        trap("stack overflow");
    stack[sp++] = v;
}

static void push_int(int n) {
    push(integer(n));
}

static struct value pop(void) {
    if (sp == fp)
        trap("stack underflow");
    return stack[--sp];
}

/* The number in a value that must be a number. */
static int number(struct value v) {
    if (v.is_ref)
        trap("not a number");
    return v.n;
}

/* The start of the block a value refers to, if it is a reference. */
static int block(struct value v) {
    if (!v.is_ref)
        trap("not a reference");
    return v.n;
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

static void heap_init(void) {
    if (collector == MARK_SWEEP) {
        heap[0].is_ref = FREE;
        heap[0].n = HEAP_SIZE;
        heap[1] = integer(-1);
        free_list = 0;
    } else {
        top = 0;
    }
}

/* Mark and sweep. */

/* Blocks marked but whose fields are not yet looked at. Each block
 * is pushed at most once, so this can never overflow. */
static int mark_stack[HEAP_SIZE / HEADER];
static int mark_depth;

static void mark_value(struct value v) {
    if (v.is_ref && heap[v.n].is_ref == UNMARKED) {
        heap[v.n].is_ref = MARKED;
        mark_stack[mark_depth++] = v.n;
    }
}

/*
 * Mark everything reachable. The roots are the stack and memory: the
 * only places a reference can be, apart from inside blocks.
 */
static void mark(void) {
    int i, b;

    mark_depth = 0;
    for (i = 0; i < sp; i++)
        mark_value(stack[i]);
    for (i = 0; i < MEMORY_SIZE; i++)
        mark_value(memory[i]);
    while (mark_depth > 0) {
        b = mark_stack[--mark_depth];
        for (i = 0; i < heap[b].n; i++)
            mark_value(heap[b + HEADER + i]);
    }
}

/*
 * Go through the heap from one end to the other. Marked blocks are
 * kept, and unmarked; everything else becomes free space. Free space
 * next to free space is merged into one chunk, so that the heap does
 * not end up as many small gaps where no big block fits.
 */
static void sweep(void) {
    int at = 0, last = -1;
    long live = 0;

    free_list = -1;
    while (at < HEAP_SIZE) {
        int state = heap[at].is_ref;
        int size = state == FREE ? heap[at].n : heap[at].n + HEADER;

        if (state == MARKED) {
            heap[at].is_ref = UNMARKED;
            live += size;
        } else {
            if (state == UNMARKED)
                words_freed += size;
            if (last >= 0 && last + heap[last].n == at) {
                heap[last].n += size;
            } else {
                heap[at].is_ref = FREE;
                heap[at].n = size;
                heap[at + 1] = integer(-1);
                if (last >= 0)
                    heap[last + 1].n = at;
                else
                    free_list = at;
                last = at;
            }
        }
        at += size;
    }
    if (live > most_live)
        most_live = live;
}

/*
 * First fit: take the first chunk that is big enough. A chunk that is
 * a little bigger is split, and the block taken from its end, so the
 * chunk stays where it is in the list. A chunk exactly one place too
 * big is passed over, since one place cannot be a chunk on its own.
 */
static int find_free(int words) {
    int prev = -1, c = free_list;

    while (c >= 0) {
        int size = heap[c].n;
        int next = heap[c + 1].n;

        if (size == words) {
            if (prev >= 0)
                heap[prev + 1].n = next;
            else
                free_list = next;
            return c;
        }
        if (size >= words + HEADER) {
            heap[c].n = size - words;
            return c + size - words;
        }
        prev = c;
        c = next;
    }
    return -1;
}

/* Copying. */

static struct value *to_space;
static int to_top;

/*
 * Copy the block a reference refers to into to-space, unless it has
 * been copied already, and return the reference to the copy. The old
 * block is left with a forwarding address: where its copy is now.
 */
static struct value forward(struct value v) {
    int b, words;

    if (!v.is_ref)
        return v;
    b = v.n;
    if (heap[b].is_ref != FORWARDED) {
        words = heap[b].n + HEADER;
        memcpy(&to_space[to_top], &heap[b], words * sizeof (struct value));
        words_copied += words;
        heap[b].is_ref = FORWARDED;
        heap[b].n = to_top;
        to_top += words;
    }
    v.n = heap[b].n;
    return v;
}

/*
 * Cheney's algorithm, 1970. Copy what the roots refer to. Then go
 * through to-space from the start, copying what each copied block
 * refers to and fixing its fields, until the scan catches up with
 * the end of what has been copied. To-space then holds exactly the
 * reachable blocks, packed together, and is the heap from now on.
 */
static void copy(void) {
    int i, scan = 0;

    to_space = heap == space_a ? space_b : space_a;
    to_top = 0;
    for (i = 0; i < sp; i++)
        stack[i] = forward(stack[i]);
    for (i = 0; i < MEMORY_SIZE; i++)
        memory[i] = forward(memory[i]);
    while (scan < to_top) {
        int n = to_space[scan].n;
        for (i = 0; i < n; i++)
            to_space[scan + HEADER + i] = forward(to_space[scan + HEADER + i]);
        scan += n + HEADER;
    }
    heap = to_space;
    top = to_top;
    if (top > most_live)
        most_live = top;
}

static void collect(void) {
    clock_t began = clock();

    collections++;
    if (collector == MARK_SWEEP) {
        mark();
        sweep();
    } else {
        copy();
    }
    gc_time += clock() - began;
}

static int find_room(int words) {
    int b;

    if (collector == MARK_SWEEP)
        return find_free(words);
    if (words > HEAP_SIZE - top)
        return -1;
    b = top;
    top += words;
    return b;
}

static struct value allocate(int n) {
    struct value r;
    int i, b, words;

    if (n < 0)
        trap("bad size");
    if (n > HEAP_SIZE - HEADER)
        trap("out of memory");
    words = n + HEADER;
    if (stress)
        collect();
    b = find_room(words);
    if (b < 0) {
        collect();
        b = find_room(words);
        if (b < 0)
            trap("out of memory");
    }
    heap[b].is_ref = UNMARKED;
    heap[b].n = n;
    heap[b + 1] = integer(++blocks_made);
    for (i = 0; i < n; i++)
        heap[b + HEADER + i] = integer(0);
    words_allocated += words;
    r.is_ref = 1;
    r.n = b;
    return r;
}

static void report(void) {
    if (!statistics)
        return;
    fflush(stdout);
    fprintf(stderr, "gc: %s%s, heap of %d places\n",
            collector == MARK_SWEEP ? "mark and sweep" : "copying",
            stress ? " (stress)" : "", HEAP_SIZE);
    fprintf(stderr, "gc: %d blocks made, %ld places in all\n", blocks_made, words_allocated);
    fprintf(stderr, "gc: %ld collections, most live after one: %ld places\n",
            collections, most_live);
    if (collector == MARK_SWEEP)
        fprintf(stderr, "gc: %ld places freed\n", words_freed);
    else
        fprintf(stderr, "gc: %ld places copied\n", words_copied);
    fprintf(stderr, "gc: %.3f seconds collecting\n", (double) gc_time / CLOCKS_PER_SEC);
}

/* Where field i of the block at b is, checking that there is one. */
static int field(int b, int i) {
    if (i < 0 || i >= heap[b].n)
        trap("index out of bounds");
    return b + HEADER + i;
}

static int same(struct value a, struct value b) {
    return a.is_ref == b.is_ref && a.n == b.n;
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

/* A value as text: 42 for an integer, @7 for a reference to block 7. */
static void show_value(FILE *out, const char *sep, struct value v) {
    if (v.is_ref)
        fprintf(out, "%s@%d", sep, heap[v.n + 1].n);
    else
        fprintf(out, "%s%d", sep, v.n);
}

/*
 * Write the stack, bottom first, with a bar where each frame begins.
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
            show_value(out, sep, stack[i]);
            sep = " ";
        }
    }
}

/*
 * 32-bit wrapping arithmetic, without undefined behaviour. Unsigned
 * arithmetic in C wraps by definition; to_int turns the unsigned
 * result back into a signed one by hand, because a plain cast of a
 * value above INT32_MAX is left to the compiler to decide.
 */
static int to_int(uint32_t u) {
    if (u <= INT32_MAX)
        return (int) u;
    return -(int) (UINT32_MAX - u) - 1;
}

static int wrap_add(int a, int b) {
    return to_int((uint32_t) a + (uint32_t) b);
}

static int wrap_sub(int a, int b) {
    return to_int((uint32_t) a - (uint32_t) b);
}

static int wrap_mul(int a, int b) {
    return to_int((uint32_t) a * (uint32_t) b);
}

/* INT32_MIN / -1 is the one quotient too big for 32 bits. It wraps. */
static int wrap_div(int a, int b) {
    if (b == -1)
        return wrap_sub(0, a);
    return a / b;
}

static int wrap_mod(int a, int b) {
    if (b == -1)
        return 0;
    return a % b;
}

/* Run one instruction. Returns 0 once the machine has halted. */
static int step(void) {
    struct value v, w;
    int op, a, b, k;

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
        push_int(operand());
        break;
    case ADD:
    case SUB:
    case MUL:
    case DIV:
    case MOD:
    case AND:
    case OR:
    case XOR:
    case LT:
        w = pop();
        v = pop();
        a = number(v);
        b = number(w);
        switch (op) {
        case ADD: push_int(wrap_add(a, b)); break;
        case SUB: push_int(wrap_sub(a, b)); break;
        case MUL: push_int(wrap_mul(a, b)); break;
        case AND: push_int(a & b); break;
        case OR:  push_int(a | b); break;
        case XOR: push_int(a ^ b); break;
        case LT:  push_int(a < b); break;
        default:
            if (b == 0)
                trap("division by zero");
            push_int(op == DIV ? wrap_div(a, b) : wrap_mod(a, b));
        }
        break;
    case EQ:
        w = pop();
        v = pop();
        push_int(same(v, w));
        break;
    case PRINT:
        printf("%d\n", number(pop()));
        break;
    case JMP:
        pc = address();
        break;
    case JZ:
        b = address();
        v = pop();
        if (!v.is_ref && v.n == 0)
            pc = b;
        break;
    case DUP:
        v = pop();
        push(v);
        push(v);
        break;
    case DROP:
        pop();
        break;
    case SWAP:
        w = pop();
        v = pop();
        push(w);
        push(v);
        break;
    case OVER:
        w = pop();
        v = pop();
        push(v);
        push(w);
        push(v);
        break;
    case ROT: {
        struct value u = pop();
        w = pop();
        v = pop();
        push(w);
        push(u);
        push(v);
        break;
    }
    case LOAD:
        push(stack[local()]);
        break;
    case STORE:
        k = operand();
        v = pop();
        if (k < 0 || fp + k >= sp)
            trap("no such local");
        stack[fp + k] = v;
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
        v = pop();
        sp = fp;
        fsp--;
        pc = frames[fsp].ret;
        fp = frames[fsp].fp;
        push(v);
        break;
    case LOADM:
        a = number(pop());
        if (a < 0 || a >= MEMORY_SIZE)
            trap("no such memory address");
        push(memory[a]);
        break;
    case STOREM:
        w = pop();
        a = number(pop());
        if (a < 0 || a >= MEMORY_SIZE)
            trap("no such memory address");
        memory[a] = w;
        break;
    case EMIT:
        a = number(pop());
        if (a < 0 || a > 255)
            trap("not a character");
        putchar(a);
        break;
    case NEW:
        push(allocate(number(pop())));
        break;
    case GETF:
        w = pop();
        v = pop();
        b = block(v);
        push(heap[field(b, number(w))]);
        break;
    case SETF: {
        struct value u = pop();
        w = pop();
        v = pop();
        b = block(v);
        heap[field(b, number(w))] = u;
        break;
    }
    case LEN:
        push_int(heap[block(pop())].n);
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
    const char *usage = "usage: vm [-t | -d] [-g mark | -g copy] [-S] [-s] program.vm\n";
    int mode = 0, i;

    for (i = 1; i < argc - 1; i++) {
        if (strcmp(argv[i], "-t") == 0 || strcmp(argv[i], "-d") == 0) {
            mode = argv[i][1];
        } else if (strcmp(argv[i], "-g") == 0 && i + 1 < argc - 1) {
            i++;
            if (strcmp(argv[i], "mark") == 0) {
                collector = MARK_SWEEP;
            } else if (strcmp(argv[i], "copy") == 0) {
                collector = COPYING;
            } else {
                fprintf(stderr, "%s", usage);
                return 2;
            }
        } else if (strcmp(argv[i], "-S") == 0) {
            stress = 1;
        } else if (strcmp(argv[i], "-s") == 0) {
            statistics = 1;
        } else {
            fprintf(stderr, "%s", usage);
            return 2;
        }
    }
    if (argc < 2 || argv[argc - 1][0] == '-') {
        fprintf(stderr, "%s", usage);
        return 2;
    }
    load(argv[argc - 1]);
    heap_init();
    atexit(report);
    if (mode == 't')
        trace();
    else if (mode == 'd')
        debug();
    else
        run();
    return 0;
}
