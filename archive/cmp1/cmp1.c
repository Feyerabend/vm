#include <stdlib.h> 
#include <stdio.h>
#include <ctype.h>
#include <string.h>

enum {
    ADD,
    CONSTANT,
    MULTIPLY,
};

typedef struct node {
    int type;
    int value;
    struct node *node1, *node2;
} node;

node* nnode(int type) {
    node* n = (node*) (malloc(sizeof(node)));
    n->type = type;
    return n;
}

node* sample() {
    node *x, *y, *z;

    y = nnode(CONSTANT);
    y->value = 32;
    z = nnode(CONSTANT);
    z->value = 53;
    x = nnode(ADD);
    x->node1 = y;
    x->node2 = z;

    node *p, *q;

    p = nnode(CONSTANT);
    p->value = 90;
    q = nnode(MULTIPLY);
    q->node1 = x;
    q->node2 = p;

    return q;
}

void compile(node *n) {
    switch (n->type) {

        case CONSTANT:
            printf("SET %d\n", n->value);
            break;

        case ADD:
            compile(n->node1);
            compile(n->node2);
            printf("ADD\n"); 
            break;

        case MULTIPLY:
            compile(n->node1);
            compile(n->node2);
            printf("MUL\n"); 
            break;
    }
}

int main() {
    compile(sample());
    return 0;
}
