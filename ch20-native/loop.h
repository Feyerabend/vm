/*
 * The run loop: threaded dispatch, as in chapter 16. This file is
 * included twice into vm.c, with RUN set to the name of the function
 * to define, and with the checks set up as that function needs them.
 */

static void RUN(void) {
    static void *table[NOPS] = {
        &&L_HALT, &&L_PUSH, &&L_ADD, &&L_SUB, &&L_MUL, &&L_PRINT,
        &&L_JMP, &&L_JZ, &&L_DUP, &&L_DROP, &&L_SWAP, &&L_OVER, &&L_ROT, &&L_LT, &&L_EQ,
        &&L_LOAD, &&L_STORE, &&L_CALL, &&L_RET,
        &&L_DIV, &&L_MOD,
        &&L_AND, &&L_OR, &&L_XOR, &&L_LOADM, &&L_STOREM, &&L_EMIT,
        &&L_NEW, &&L_GETF, &&L_SETF, &&L_LEN,
        &&L_CALLI
    };
    /* Static, so that it lives as long as the program does. */
    static void **thread;
    int a;

    thread = malloc((code_len + 1) * sizeof (void *));

    if (thread == NULL) {
        fprintf(stderr, "out of memory for threaded code\n");
        exit(2);
    }
    for (a = 0; a < code_len; a++)
        thread[a] = code[a] >= 0 && code[a] < NOPS ? table[code[a]] : &&L_UNKNOWN;
    thread[code_len] = &&L_RUNOFF;

    NEXT;
#include "ops.h"
L_RUNOFF:
    trap("ran off the end of the program");
}
