#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "scan.h"

char buf[MAXSYMB];
FILE *input;

void setinput(FILE* inputfile) {
    input = inputfile;
}

int advance() {
    return fgetc(input);
}

Symbol scan() {

    static int c = ' ';
    int i = 0; // buf counter

    while (isspace(c)) {
        c = advance();
    }

    if (c == EOF)
        return ENDOFFILE;

    if (isalpha(c)) {

        // make a "word"
        do {
            buf[i++] = c;
            if (i >= MAXSYMB) {
                printf("scan: max buf length: %d\n", MAXSYMB);
                exit(1);
            }
            c = advance();
        } while (isalpha(c) || isdigit(c) || c == '_');
        buf[i] = '\0'; // terminate

        // check for reserved words
        if (!strcmp(buf, "print"))
            return PRINTSYM;

        // if not reserved, this is by default IDENTifier
        else {
            return IDENT;
        }
    }
    else if (isdigit(c)) {

        // make a number (integer)
        do {
            buf[i++] = c;
            if (i >= MAXSYMB) {
                printf("scan: max buf length: %d\n", MAXSYMB);
                exit(1);
            }
            c = advance();
        } while (isdigit(c));
        buf[i] = '\0';

        return NUMBER;
    }
    else
        switch (c) {

        // add
        case '+':
            c = advance();
            return PLUS;

        // subtract
        case '-':
            c = advance();
            return MINUS;

        // multiply
        case '*':
            c = advance();
            return TIMES;

        // divide
        case '/':
            c = advance();
            return SLASH;

        // lparen
        case '(':
            c = advance();
            return LPAREN;

        // rparen
        case ')':
            c = advance();
            return RPAREN;

        // semicolon
        case ';':
            c = advance();
            return SEMICOLON;

        // period
        case '.':
            c = advance();
            return PERIOD;

        default:
            printf("scan: default error\n");
            exit(1);
    }
}


void printsymb(Symbol s) {

    switch (s) {

        case IDENT:
            printf("IDENT \"%s\"\n", buf); break;

        case NUMBER:
            printf("NUMBER \"%s\"\n", buf); break;

        case LPAREN:
            printf("LPAREN \"(\"\n"); break;

        case RPAREN:
            printf("RPAREN \")\"\n"); break;

        case TIMES:
            printf("TIMES \"*\"\n"); break;

        case SLASH:
            printf("SLASH \"/\"\n"); break;

        case PLUS:
            printf("PLUS \"+\"\n"); break;

        case MINUS:
            printf("MINUS \"-\"\n"); break;

        case SEMICOLON:
            printf("SEMICOLON \";\"\n"); break;

        case PRINTSYM:
            printf("PRINTSYM \"print\"\n"); break;

        case PERIOD:
            printf("PERIOD \".\"\n"); break;

        case ENDOFFILE:
            printf("ENDOFFILE\n"); break;

        default:
            printf("Unrecognized symbol\n"); break;
    }
}

/* EOF */
