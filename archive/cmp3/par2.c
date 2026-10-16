/* parser before merging with rest of compiler */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "scan.h"

#define TRUE 1
#define FALSE 0

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


void program();
void expression();
void term();
void factor();


// <factor> = <ident> | <number> | "(" <expression> ")"
void factor() {
    if (accept(IDENT)) {
        ;
    } else if (accept(NUMBER)) {
        printf("CONSTANT=");
        printf("%s\n", buf);
        ;
    } else if (accept(LPAREN)) {
        expression();
        expect(RPAREN);
    } else {
        error("factor: syntax error");
        nextsym();
    }
}

// <term> = <factor> {("*"|"/") <factor>}
void term() {
    factor();
    while (sym == TIMES || sym == SLASH) {
        if (sym == TIMES)
            printf("*\n");
        if (sym == SLASH)
            printf("/\n");
        nextsym();
        // children
        factor();
    }
}

// <expression> = [ "+"|"-"] <term> { ("+"|"-") <term>}
void expression() {
    if (sym == PLUS || sym == MINUS)
        nextsym();
    term();
    while (sym == PLUS || sym == MINUS) {
        if (sym == PLUS)
            printf("+\n");
        if (sym == MINUS)
            printf("-\n");
        nextsym();
        // children
        term();
    }
}

// <program> = <expression> "."
void program() {
    // node *x = nnode(PROG);
    nextsym();
    // x->node1 = expression();
    expression();
    expect(PERIOD);
    // return x;
}

int main() {
    program();
    return 0;
}

/* EOF */
