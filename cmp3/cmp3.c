#include <stdlib.h> 
#include <stdio.h>
#include <ctype.h>
#include <string.h>

#include "scan.h"

#define FALSE 0
#define TRUE 1

FILE* file;


// parser init decl helpers etc

Symbol sym;

void nextsym() {
    sym = scan();
    printf("> ");
    printsymb(sym);
};

void error(const char msg[]) {
    printf("error: %s\n", msg);
    printsymb(sym);
};

int accept(Symbol s) {
    if (sym == s) {
        nextsym();
        return TRUE;
    }
    return FALSE;
}

int expect(Symbol s) {
    if (accept(s)) {
        return TRUE;
    }
    error("expected symbol: ");
    printsymb(s);
    return FALSE;
}


// compiler init decl etc

typedef enum {
    ADD,
    ASSIGN,
    CONSTANT,
    DIVIDE,
    DO,
    EXPR,
    IF,
    IFELSE,
    LESS,
    MULTIPLY,
    PROG,
    SEQ,
    SUB,
    VALUE,
    WHILE
} Instr;

#define LABEL_MAX 6
char labelarr1[LABEL_MAX];
char labelarr2[LABEL_MAX];
int labelcount = 1;

typedef struct node {
    int type;
    int value;
    struct node *node1, *node2, *node3;
} node;

int nlabel() {
  int count;
  count = snprintf(labelarr1, LABEL_MAX, "L%04d", labelcount);
  if (count >= 0 && count < LABEL_MAX) {
    labelcount++;
    return TRUE;
  }
  return FALSE;
}

void copylabel() {
  int loop;
  for (loop = 0; loop < LABEL_MAX; loop++) {
    labelarr2[loop] = labelarr1[loop];
  }
}

// new node
node* nnode(int type) {
    node* n = (node*) (malloc(sizeof(node)));
    n->type = type;
    return n;
}

// sample node by hand
node* sample() {

/* CONSTANT ADD MULTIPLY */
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

// fwd decl
node* expression();


// <factor> = <ident> | <number> | "(" <expression> ")";
node* factor() {
    node *n;
    n = NULL;

    if (accept(IDENT)) {
        ;
    } else if (accept(NUMBER)) {
        n = nnode(CONSTANT);
        n->value = atoi(buf);
        ;
    } else if (accept(LPAREN)) {
        n = expression();
        expect(RPAREN);
    } else {
        error("factor: syntax error");
        nextsym();
    }
    return n;
}

// <term> = <factor> {("*"|"/") <factor>};
node* term() {
    node *m, *n;
    n = factor();
    int h;
    while (sym == TIMES || sym == SLASH) {
        m = n;
        h = (sym == TIMES ? MULTIPLY : DIVIDE);
        n = nnode(h);
        nextsym();
        n->node1 = m;
        n->node2 = factor();
    }
    return n;
}

// <expression> = [ "+"|"-"] <term> { ("+"|"-") <term>};
node* expression() {
    node *m, *n;
    n = term();
    int h;
    while (sym == PLUS || sym == MINUS) {
        m = n;
        h = (sym == PLUS ? ADD : SUB);
        n = nnode(h);
        nextsym();
        n->node1 = m;
        n->node2 = term();
    }
    return n;
}

// <program> = <expression> "." ;
node* program() {
    node *n = nnode(PROG);
    nextsym();
    n->node1 = expression();
    expect(PERIOD);
    return n;
}


// compile nodes
void compile(node *n) {
    switch (n->type) {

        case CONSTANT:
            fprintf(file, "\tSET %d\n", n->value);
            break;

        case VALUE:
            fprintf(file, "\tLOAD %d\n", n->value);
            break;

        case ASSIGN:
            compile(n->node2);
            fprintf(file, "\tSTORE %d\n", n->node1->value);
            break;

        case ADD:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tADD\n");
            break;

        case SUB:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tSUB\n");
            break;

        case MULTIPLY:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tMUL\n");
            break;

        case PROG:
            compile(n->node1);
            fprintf(file, "\tHALT\n");
            break;
    }
}

int main() {
	file = fopen("sample.a", "w");

	fprintf(file, "START:\n");
	compile(program());
	fprintf(file, "\tPRINT\n");
	fclose(file);

	return 0;
}
