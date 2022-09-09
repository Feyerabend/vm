
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "scan.h"


char buf[MAXSYMB];

int advance() { return getchar(); }

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
                printf("max buf length: %d\n", MAXSYMB);
                exit(1);
            }
            c = advance();
        } while (isalpha(c) || isdigit(c) || c == '_');
        buf[i] = '\0'; // terminate

        // check for reserved words
        if (!strcmp(buf, "procedure"))
            return PROCSYM;

        else if (!strcmp(buf, "var"))
            return VARSYM;

        else if (!strcmp(buf, "const"))
            return CONSTSYM;

        else if (!strcmp(buf, "do"))
            return DOSYM;

        else if (!strcmp(buf, "while"))
            return WHILESYM;

        else if (!strcmp(buf, "if"))
            return IFSYM;

        else if (!strcmp(buf, "then"))
            return THENSYM;

        else if (!strcmp(buf, "end"))
            return ENDSYM;

        else if (!strcmp(buf, "begin"))
            return BEGINSYM;

        else if (!strcmp(buf, "call"))
            return CALLSYM;

        else if (!strcmp(buf, "odd"))
            return ODDSYM;

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
                printf("max buf length: %d\n", MAXSYMB);
                exit(1);
            }
            c = advance();
        } while (isdigit(c));
        buf[i] = '\0';

        return NUMBER;
    }
    else if (c == '=' || c == ':' || c == '<' || c == '>') {

        int b = c;
        c = advance();

        // less <
        if (c != '=' && b == '<')
            return LSS;

        // greater >
        else if (c != '=' && b == '>')
            return GTR;

        // equal =
        else if (b == '=')
            return EQL;

        int a = c;
        c = advance();

        // greater or equal >=
        if (a == '=' && b == '>')
            return GEQ;

        // less or equal <=
        else if (a == '=' && b == '<')
            return LEQ;

        // assign :=
        else if (a == '=' && b == ':')
            return BECOMES;

        else {
            printf("comparation error");
            printsymb(c);
            exit(1);
        }
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

        case '#':
            c = advance();
            return NEQ;

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

        // comma
        case ',':
            c = advance();
            return COMMA;

        // period
        case '.':
            c = advance();
            return PERIOD;

        default:
            printf("default error\n");
            exit(1);
    }
}


void printsymb(Symbol s) {

    switch (s) {

        case NOP:
            printf("NOP\n"); break;

        case IDENT:
            printf("IDENT \"%s\"\n", buf); break;

        case NUMBER:
            printf("NUMBER \"%s\"\n", buf); break;

        case LPAREN:
            printf("LPAREN \"(\"\n"); break;

        case RPAREN:
            printf("RPAREN \")\"\n"); break;

        case TIMES:
            printf("RPAREN \"*\"\n"); break;

        case SLASH:
            printf("RPAREN \"/\"\n"); break;

        case PLUS:
            printf("PLUS \"+\"\n"); break;

        case MINUS:
            printf("MINUS \"-\"\n"); break;

        case EQL:
            printf("EQL \"=\"\n"); break;

        case NEQ:
            printf("NEQ \"#\"\n"); break;

        case LSS:
            printf("LSS \"<\"\n"); break;

        case LEQ:
            printf("LEQ \"<=\"\n"); break;

        case GTR:
            printf("GTR \">\"\n"); break;

        case GEQ:
            printf("GEQ \">=\"\n"); break;

        case CALLSYM:
            printf("CALLSYM \"call\"\n"); break;

        case BEGINSYM:
            printf("BEGINSYM \"begin\"\n"); break;

        case SEMICOLON:
            printf("SEMICOLON \";\"\n"); break;

        case ENDSYM:
            printf("ENDSYM \"end\"\n"); break;

        case IFSYM:
            printf("IFSYM \"if\"\n"); break;

        case WHILESYM:
            printf("WHILESYM \"while\"\n"); break;

        case BECOMES:
            printf("BECOMES \":=\"\n"); break;

        case THENSYM:
            printf("THENSYM \"then\"\n"); break;

        case DOSYM:
            printf("DOSYM \"do\"\n"); break;

        case CONSTSYM:
            printf("CONSTSYM \"const\"\n"); break;

        case COMMA:
            printf("COMMA \",\"\n"); break;

        case VARSYM:
            printf("VARSYMP \"var\"\n"); break;

        case PROCSYM:
            printf("PROCSYMP \"procedure\"\n"); break;

        case PERIOD:
            printf("PERIOD \".\"\n"); break;

        case ODDSYM:
            printf("ODDSYM \"odd\"\n"); break;

        case ENDOFFILE:
            printf("ENDOFFILE\n"); break;
    }
}

/* EOF */
