#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "scan.h"
#include "error.h"

#define TRUE 1
#define FALSE 0

char buf[MAXSYMB];
FILE *input;

void maxbuf() {
    fprintf(stderr, " maximum length for token=%d", MAXSYMB);
}

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
                errnum(ERROR_EXCEEDED_BUFFER_LENGTH);
                maxbuf();
                exit(EXIT_FAILURE);
            }
            c = advance();
        } while (isalpha(c) || isdigit(c) || c == '_');
        buf[i] = '\0'; // terminate

        // now, check for reserved words
        if (!strcmp(buf, "procedure"))
            return PROCSYM;

        else if (!strcmp(buf, "var"))
            return VARSYM;

        else if (!strcmp(buf, "is"))
            return BECOMES;

        else if (!strcmp(buf, "const"))
            return CONSTSYM;

        else if (!strcmp(buf, "array"))
            return ARRAYSYM;

        else if (!strcmp(buf, "do"))
            return DOSYM;

        else if (!strcmp(buf, "while"))
            return WHILESYM;

        else if (!strcmp(buf, "if"))
            return IFSYM;

        else if (!strcmp(buf, "then"))
            return THENSYM;

        else if (!strcmp(buf, "else"))
            return ELSESYM;

        else if (!strcmp(buf, "end"))
            return ENDSYM;

        else if (!strcmp(buf, "begin"))
            return BEGINSYM;

        else if (!strcmp(buf, "call"))
            return CALLSYM;

        else if (!strcmp(buf, "return"))
            return RETURNSYM;

        else if (!strcmp(buf, "print"))
            return PRINTSYM;

        else if (!strcmp(buf, "emit"))
            return EMITSYM;

        else if (!strcmp(buf, "and"))
            return ANDSYM;

        else if (!strcmp(buf, "or"))
            return ORSYM;

        else if (!strcmp(buf, "xor"))
            return XORSYM;

        // by default IDENTifier
        else {
            return IDENT;
        }
    }
    else if (isdigit(c)) {

        // make a number (integer)
        do {
            buf[i++] = c;
            if (i >= MAXSYMB) {
                errnum(ERROR_EXCEEDED_BUFFER_LENGTH);
                maxbuf();
                exit(EXIT_FAILURE);
            }
            c = advance();
        } while (isdigit(c));
        buf[i] = '\0';

        return NUMBER;
    }

    // ("<"|"<="|">"|">=")
    else if (c == '<' || c == '>') {

        if (c == '<') {
            c = advance();
            if (c == '=') {
                c = advance();
                return LEQ;
            }
            else
                return LSS;
        }
        else if (c == '>') {
            c = advance();
            if (c == '=') {
                c = advance();
                return GEQ;
            }
            else
                return GTR;
        }
        else {
            errnum(ERROR_COMPARATION_OR_SHIFT_SYMBOL);
            return 0;
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

        // mod
        case '%':
            c = advance();
            return PERCENT;

        // equal
        case '=':
            c = advance();
            return EQL;

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

        // lbracket
        case '[':
            c = advance();
            return LBRACKET;

        // rbracket
        case ']':
            c = advance();
            return RBRACKET;

        // lbracket
        case '{':
            c = advance();
            return LCURLY;

        // rbracket
        case '}':
            c = advance();
            return RCURLY;

        // exclamation
        case '!':
            c = advance();
            return EXCLAMATION;

        // colon
        case ':':
            c = advance();
            return COLON;

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
            errnum(ERROR_TOKEN_NOT_IDENTIFIED);
            return 0;
    }
}

/* EOF */
