#include <stdlib.h> 
#include <stdio.h>
#include <ctype.h>
#include <string.h>

#include "cmp4.h"
#include "scan.h"
#include "error.h"

Symbol sym;

FILE* file;

// send file pointer to scan
void setinputfile(FILE* inputfile) {
    setinput(inputfile);
}

void nextsym() {
    sym = scan();
    printf("> ");
    printsymb(sym);
}

int recognize(Symbol s) {
    if (sym == s)
        return TRUE;
    return FALSE;
}

int accept(Symbol s) {
    if (sym == s) {
        nextsym();
        return TRUE;
    }
    return FALSE;
}

int expect(Symbol s) {
    if (recognize(s)) {
        nextsym();
        return TRUE;
    }
    error("expected symbol");
    return FALSE;
}

// new node in parse tree
node* nnode(int type) {
    node* n = (node*) (malloc(sizeof(node)));
    if (n == NULL)
        return NULL;
    n->type = type;
    return n;
}

// free tree
void dnode(node* n) {
    if (n == NULL)
        return;
  
    // branches
    dnode(n->node1);
    dnode(n->node2);
    dnode(n->node3);
    
    // leaf
    free(n);
}


// PARSING AND AST BUILD
// --------------------------
// forward decl.
node* program();

//  ignored for the moment:
//  node* block();
//  node* procedure();
//  node* statement();
//  node* condition();

node* expression();
node* term();
node* factor();


// <factor> = <ident> | <number> | "(" <expression> ")"
node* factor() {
    node *n = NULL;

    if (recognize(IDENT)) {
        ;
        nextsym();

    } else if (recognize(NUMBER)) { // ok
        n = nnode(INUMBER);
        n->value = atoi(buf);
        nextsym();

    } else if (accept(LPAREN)) { // ok
        n = expression();
        expect(RPAREN);

    } else {
        error("factor: syntax error");
        nextsym();
    }

    return n;
}


// <term> = <factor> {("*"|"/") <factor>}
node* term() {
    node *m, *n;
    n = factor();
    int h = BLANK;

    while (sym == TIMES || sym == SLASH) {
        m = n;

        if (sym == TIMES)
            h = MULTIPLY;       // *
        else if (sym == SLASH)
            h = DIVIDE;         // /
        else {
            error("term: invalid operator");
            nextsym();
        }

        n = nnode(h);
        nextsym();
        n->node1 = m;
        n->node2 = factor();
    }

    return n;
}


// <expression> = <term> { ("+"|"-") <term> }
node* expression() {
    node *m, *n;
    n = term();
    int h = BLANK;

    while (sym == PLUS || sym == MINUS) {
        m = n;

        if (sym == PLUS)
            h = ADD;            // +
        else if (sym == MINUS)
            h = SUB;            // -
        else {
            error("expression: invalid operator");
            nextsym();
        }

        n = nnode(h);
        nextsym();
        n->node1 = m;
        n->node2 = term();
    }

    return n;
}


// ..
// skip the rest of parsing for the moment ..
// ..


// program = block "."
node* program() {
    node *n = nnode(PROG);
    nextsym();
    n->node1 = expression(); // block(); will be here later
    expect(PERIOD);
    return n;
}


// CODE GENERATION
// ---------------------------
// generate instructions for assembler
// from parse tree
void compile(node *n) {

    if (n == NULL)
        return;

    switch (n->type) {

        case ADD:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tADD\n");
            break;

        case BLANK:
            break;

        case DIVIDE:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tDIV\n");
            break;

        case INUMBER:
            fprintf(file, "\tSET %d\n", n->value);
            break;

        case MULTIPLY:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tMUL\n");
            break;

        case PRINT:
            compile(n->node1);
            fprintf(file, "\tPRINT\n");
            break;

        case PROG:
            compile(n->node1); // block
            fprintf(file, "\tPRINT\n");
            fprintf(file, "\tHALT\n");
            break;

        case START:
            fprintf(file, "START:\n");
            break;

        case SUB:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tSUB\n");
            break;

        default:
            break;
    }
}


int main(int argc, char *argv[]) {
    FILE* in = fopen(argv[1], "rb");
    setinputfile(in);
    file = fopen("sample.a", "w");

    printf("parse ..\n");
    node* n = program();
    printf("done.\n");

    printf("compiling ..\n");
    compile(n);
    printf("done.\n");

    fclose(file);

    dnode(n);

    return 0;
}
