/*
 * The instructions of the machine, each written once. This file is
 * included twice into vm.c, by loop.h: once into the run loop that
 * checks everything, and once into the one for verified programs,
 * where pop(), operand(), address() and local() check nothing, and
 * CHECK(condition, message) is empty. A CHECK is a check that the
 * verifier has already made, for the whole program, before it ran.
 *
 * Every instruction is a block of its own, so that it can have its
 * own variables, and ends with NEXT.
 */

OP(HALT) {
    return;
}
OP(PUSH) {
    push_int(operand());
    NEXT;
}
OP(ADD) {
    struct value w = pop(), v = pop();
    push_int(wrap_add(number(v), number(w)));
    NEXT;
}
OP(SUB) {
    struct value w = pop(), v = pop();
    push_int(wrap_sub(number(v), number(w)));
    NEXT;
}
OP(MUL) {
    struct value w = pop(), v = pop();
    push_int(wrap_mul(number(v), number(w)));
    NEXT;
}
OP(DIV) {
    struct value w = pop(), v = pop();
    int a = number(v), b = number(w);
    if (b == 0)
        trap("division by zero");
    push_int(wrap_div(a, b));
    NEXT;
}
OP(MOD) {
    struct value w = pop(), v = pop();
    int a = number(v), b = number(w);
    if (b == 0)
        trap("division by zero");
    push_int(wrap_mod(a, b));
    NEXT;
}
OP(AND) {
    struct value w = pop(), v = pop();
    push_int(number(v) & number(w));
    NEXT;
}
OP(OR) {
    struct value w = pop(), v = pop();
    push_int(number(v) | number(w));
    NEXT;
}
OP(XOR) {
    struct value w = pop(), v = pop();
    push_int(number(v) ^ number(w));
    NEXT;
}
OP(LT) {
    struct value w = pop(), v = pop();
    push_int(number(v) < number(w));
    NEXT;
}
OP(EQ) {
    struct value w = pop(), v = pop();
    push_int(same(v, w));
    NEXT;
}
OP(PRINT) {
    printf("%d\n", number(pop()));
    NEXT;
}
OP(JMP) {
    pc = address();
    NEXT;
}
OP(JZ) {
    int t = address();
    struct value v = pop();
    if (!v.is_ref && v.n == 0)
        pc = t;
    NEXT;
}
OP(DUP) {
    struct value v = pop();
    push(v);
    push(v);
    NEXT;
}
OP(DROP) {
    pop();
    NEXT;
}
OP(SWAP) {
    struct value w = pop(), v = pop();
    push(w);
    push(v);
    NEXT;
}
OP(OVER) {
    struct value w = pop(), v = pop();
    push(v);
    push(w);
    push(v);
    NEXT;
}
OP(ROT) {
    struct value u = pop(), w = pop(), v = pop();
    push(w);
    push(u);
    push(v);
    NEXT;
}
OP(LOAD) {
    push(stack[local()]);
    NEXT;
}
OP(STORE) {
    int k = operand();
    struct value v = pop();
    CHECK(k < 0 || fp + k >= sp, "no such local");
    stack[fp + k] = v;
    NEXT;
}
OP(CALL) {
    int t = address();
    int nargs = operand();
    CHECK(nargs < 0 || nargs > sp - fp, "not enough arguments");
    if (fsp == FRAMES)
        trap("too many nested calls");
    frames[fsp].ret = pc;
    frames[fsp].fp = fp;
    fsp++;
    fp = sp - nargs;
    pc = t;
    NEXT;
}
OP(CALLI) {
    int nargs = operand();
    int t = number(pop());
    if (t < 0 || t >= code_len)
        trap("jump out of program");
    if (nargs < 0 || nargs > sp - fp)
        trap("not enough arguments");
    if (fsp == FRAMES)
        trap("too many nested calls");
    frames[fsp].ret = pc;
    frames[fsp].fp = fp;
    fsp++;
    fp = sp - nargs;
    pc = t;
    NEXT;
}
OP(RET) {
    struct value v;
    CHECK(fsp == 0, "return without call");
    v = pop();
    sp = fp;
    fsp--;
    pc = frames[fsp].ret;
    fp = frames[fsp].fp;
    push(v);
    NEXT;
}
OP(LOADM) {
    int a = number(pop());
    if (a < 0 || a >= MEMORY_SIZE)
        trap("no such memory address");
    push(memory[a]);
    NEXT;
}
OP(STOREM) {
    struct value w = pop();
    int a = number(pop());
    if (a < 0 || a >= MEMORY_SIZE)
        trap("no such memory address");
    memory[a] = w;
    NEXT;
}
OP(EMIT) {
    int a = number(pop());
    if (a < 0 || a > 255)
        trap("not a character");
    putchar(a);
    NEXT;
}
OP(NEW) {
    push(allocate(number(pop())));
    NEXT;
}
OP(GETF) {
    struct value w = pop(), v = pop();
    int b = block(v);
    push(heap[field(b, number(w))]);
    NEXT;
}
OP(SETF) {
    struct value u = pop(), w = pop(), v = pop();
    int b = block(v);
    heap[field(b, number(w))] = u;
    NEXT;
}
OP(LEN) {
    push_int(heap[block(pop())].n);
    NEXT;
}
UNKNOWN {
    trap("unknown instruction");
}
