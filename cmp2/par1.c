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
void block();
void statement();
void condition();
void expression();
void term();
void factor();


// <factor> = <ident> | <number> | "(" <expression> ")";
void factor() {
    if (accept(IDENT)) {
        ;
    } else if (accept(NUMBER)) {
        ;
    } else if (accept(LPAREN)) {
        expression();
        expect(RPAREN);
    } else {
        error("factor: syntax error");
        nextsym();
    }
}

// <term> = <factor> {("*"|"/") <factor>};
void term() {
    factor();
    while (sym == TIMES || sym == SLASH) {
        nextsym();
        factor();
    }
}

// <expression> = [ "+"|"-"] <term> { ("+"|"-") <term>};
void expression() {
    if (sym == PLUS || sym == MINUS)
        nextsym();
    term();
    while (sym == PLUS || sym == MINUS) {
        nextsym();
        term();
    }
}

// <condition> = "odd" <expression>
//              | <expression> ("="|"#"|"<"|"<="|">"|">=") <expression> ;
void condition() {
    if (accept(ODDSYM)) {
        expression();
    } else {
        expression();
        if (sym == EQL || sym == NEQ || sym == LSS || sym == LEQ || sym == GTR || sym == GEQ) {
            nextsym();
            expression();
        } else {
            error("condition: invalid operator");
            nextsym();
        }
    }
}


// <statement> = [ <ident> ":=" <expression>
//               | "call" <ident> 
//               | "read" <ident> // NOT IMPL!
//               | "write" <expression> // NOT IMPL!
//               | "begin" <statement> {";" <statement> } "end" 
//               | "if" <condition> "then" <statement> 
//               | "while" <condition> "do" <statement> ];
void statement() {
    if (accept(IDENT)) {
        expect(BECOMES);
        expression();
    } else if (accept(CALLSYM)) {
        expect(IDENT);
    } else if (accept(BEGINSYM)) {
        do {
            statement();
        } while (accept(SEMICOLON));
        expect(ENDSYM);
    } else if (accept(IFSYM)) {
        condition();
        expect(THENSYM);
        statement();
    } else if (accept(WHILESYM)) {
        condition();
        expect(DOSYM);
        statement();
    } else {
        error("statement: syntax error");
        nextsym();
    }
}


// <block> = [ "const" <ident> "=" <number> {"," <ident> "=" <number>} ";"]
//           [ "var" <ident> {"," <ident>} ";"]
//           { "procedure" <ident> ";" <block> ";" } <statement> ;
void block() {
    if (accept(CONSTSYM)) {
        do {
            expect(IDENT);
            expect(EQL);
            expect(NUMBER);
        } while (accept(COMMA));
        expect(SEMICOLON);
    }
    if (accept(VARSYM)) {
        do {
            expect(IDENT);
        } while (accept(COMMA));
        expect(SEMICOLON);
    }
    while (accept(PROCSYM)) {
        expect(IDENT);
        expect(SEMICOLON);
        block();
        expect(SEMICOLON);
    }
    statement();
}

// <program> = <block> "." ;
void program() {
    nextsym();
    block();
    expect(PERIOD);
}

int main() {
    program();
    return 0;
}


/* EOF */
