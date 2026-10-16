/*
 * Chapter 20: the run-time support for compiled programs.
 *
 * A program compiled by vm2c.py is C code that does what the machine's
 * instructions would have done, in the same order, on the same stack,
 * frames, memory and heap. Everything here is the interpreter's own
 * code from chapter 19, unchanged: values and their tags, the stack and
 * its checks, both garbage collectors, the arithmetic, and trap(). So a
 * compiled program fails exactly as the interpreted one does, with the
 * same message at the same address.
 *
 * What the compiled program does not need is the run loop: there is no
 * instruction to fetch, since each one has become a few lines of C.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

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
static long steps = 0;          /* instructions run, for -c */
static int counting = 0;

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

/*
 * trap() never returns, and the C compiler is told so: then it knows
 * that the code after a failed check is never reached, and need not
 * prepare for it.
 */
#if defined __GNUC__
__attribute__((noreturn))
#endif
static void trap(const char *why) {
    fflush(stdout);
    fprintf(stderr, "trap: %s at %d\n", why, start);
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
    if (counting) {
        fflush(stdout);
        fprintf(stderr, "steps: %ld\n", steps);
    }
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


/* A check on a local, for LOAD and STORE: the interpreter's local(),
 * with the operand already known. */
static int local_at(int k) {
    if (k < 0 || fp + k >= sp)
        trap("no such local");
    return fp + k;
}

static int run_options(int argc, char *argv[]) {
    int i;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-g") == 0 && i + 1 < argc) {
            i++;
            if (strcmp(argv[i], "copy") == 0)
                collector = COPYING;
            else if (strcmp(argv[i], "mark") == 0)
                collector = MARK_SWEEP;
            else
                return 0;
        } else if (strcmp(argv[i], "-S") == 0) {
            stress = 1;
        } else if (strcmp(argv[i], "-s") == 0) {
            statistics = 1;
        } else {
            return 0;
        }
    }
    return 1;
}
