/*
 * Superinstructions: each one is two instructions of ops.h, one after
 * the other, with a single dispatch. Between the two, start moves on
 * to the second instruction, so that a trap there names the right
 * address, and pc steps over the second one's opcode.
 *
 * Where the first instruction leaves a value that the second at once
 * takes, the value need not go through the stack at all, but then the
 * superinstruction must still trap where the pair would: a PUSH onto
 * a full stack must still say "stack overflow".
 */

L_LOAD_PUSH: {
    push(stack[local()]);               /* LOAD k */
    start = pc++;                       /* PUSH n */
    push_int(operand());
    NEXT;
}
L_LOAD_LOAD: {
    push(stack[local()]);               /* LOAD j */
    start = pc++;                       /* LOAD k */
    push(stack[local()]);
    NEXT;
}
L_LOAD_ADD: {
    struct value v, w;
    push(stack[local()]);               /* LOAD k */
    start = pc++;                       /* ADD */
    w = pop();
    v = pop();
    push_int(wrap_add(number(v), number(w)));
    NEXT;
}
L_LT_JZ: {
    struct value w = pop(), v = pop();  /* LT */
    int less = number(v) < number(w);
    int t;
    start = pc++;                       /* JZ t: jumps when LT gave 0 */
    t = address();
    if (!less)
        pc = t;
    NEXT;
}
L_PUSH_SUB: {
    int n = operand();                  /* PUSH n */
    struct value v;
    if (sp == STACK_SIZE)
        trap("stack overflow");
    start = pc++;                       /* SUB: v - n */
    v = pop();
    push_int(wrap_sub(number(v), n));
    NEXT;
}
L_PUSH_ADD: {
    int n = operand();                  /* PUSH n */
    struct value v;
    if (sp == STACK_SIZE)
        trap("stack overflow");
    start = pc++;                       /* ADD: v + n */
    v = pop();
    push_int(wrap_add(number(v), n));
    NEXT;
}
L_PUSH_LOADM: {
    int n = operand();                  /* PUSH n */
    if (sp == STACK_SIZE)
        trap("stack overflow");
    start = pc++;                       /* LOADM: memory[n] */
    if (n < 0 || n >= MEMORY_SIZE)
        trap("no such memory address");
    push(memory[n]);
    NEXT;
}
L_ADD_STORE: {
    struct value w = pop(), v = pop();  /* ADD */
    int k;
    push_int(wrap_add(number(v), number(w)));
    start = pc++;                       /* STORE k */
    k = operand();
    v = pop();
    if (k < 0 || fp + k >= sp)
        trap("no such local");
    stack[fp + k] = v;
    NEXT;
}
