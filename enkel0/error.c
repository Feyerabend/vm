#include <stdlib.h> 
#include <stdio.h>
#include <ctype.h>
#include <string.h>

#include "scan.h"
#include "error.h"

// some simple error handling
// warnings or errors

char* errorstring(int ERROR) {
    switch (ERROR) {
        case ERR_TEST:
            return "*** testing errors ***";
// enkel.c
        case ERROR_UNRECOGNIZED_SYMBOL:
            return "unrecognized symbol";
        case ERROR_ARRINDEX_UNKNOWN_INDEX_TYPE:
            return "unknown index type for array";
        case ERROR_SYNTAX_ERROR:
            return "syntax error";
        case ERROR_TERM_INVALID_OPERATOR:
            return "invalid operator in term";
        case ERROR_EXPRESSION_INVALID_OPERATOR:
            return "invalid operator in expression";
        case ERROR_CONDITION_RELATIONAL_INVALID_OPERATOR:
            return "invalid relational operator in condition";
// scan.c
        case ERROR_EXCEEDED_BUFFER_LENGTH:
            return "buffer length for storage of token exceeded";
        case ERROR_TOKEN_NOT_IDENTIFIED:
            return "could not identify token";
        case ERROR_COMPARATION_OR_SHIFT_SYMBOL:
            return "comparation of shift error in syntax";

        case ERROR_PREVIOUS_DECLARATION_PARAMETER:
            return "previous declaration of parameter exist";
        case ERROR_PREVIOUS_DECLARATION_CONSTANT:
            return "previous declaration of constant exist";
        case ERROR_PREVIOUS_DECLARATION_ARRAY:
            return "previous declaration of array exist";
        case ERROR_PREVIOUS_DECLARATION_GLOBAL_VARIABLE:
            return "previous declaration of global variable exist";
        case ERROR_PREVIOUS_DECLARATION_LOCAL_VARIABLE:
            return "previous declaration of local variable exist";
// symbol.c
        case ERROR_NO_PREVIOUS_DECLARATION_GLOBAL_IDENT:
            return "no previous declaration of global identifier exist";
        case ERROR_PREVIOUS_DECLARATION_GLOBAL_IDENT:
            return "previous declaration of global identifier exist";
        case ERROR_NO_PREVIOUS_DECLARATION_LOCAL_IDENT_LEVEL:
            return "no previous declaration of local identifier at level";
        case ERROR_PREVIOUS_DECLARATION_LOCAL_IDENT_LEVEL:
            return "previous declaration of local identifier at level";

        default:
            return "unknown error";
    }
}

void errnum(int error) {
    fprintf(stderr, "error:%d:%s\n", error, errorstring(error));
}


void printsymb(Symbol s) {
    switch (s) {
        case IDENT:         printf("IDENT \"%s\"\n", buf); break;
        case NUMBER:        printf("NUMBER \"%s\"\n", buf); break;

        case ANDSYM:        printf("ANDSYM \"and\"\n"); break;
        case ARRAYSYM:      printf("ARRAYSYM \"array\"\n"); break;
        case BECOMES:       printf("BECOMES \"is\"\n"); break;
        case BEGINSYM:      printf("BEGINSYM \"begin\"\n"); break;
        case CALLSYM:       printf("CALLSYM \"call\"\n"); break;
        case COLON:         printf("COLON \":\"\n"); break;
        case COMMA:         printf("COMMA \",\"\n"); break;
        case CONSTSYM:      printf("CONSTSYM \"const\"\n"); break;
        case DOSYM:         printf("DOSYM \"do\"\n"); break;
        case ELSESYM:       printf("ELSESYM \"else\"\n"); break;
        case EMITSYM:       printf("EMITSYM \"emit\"\n"); break;
        case ENDSYM:        printf("ENDSYM \"end\"\n"); break;
        case EQL:           printf("EQL \"=\"\n"); break;
        case EXCLAMATION:   printf("EXCLAMATION \"!\"\n"); break;
        case GEQ:           printf("GEQ \">=\"\n"); break;
        case GTR:           printf("GTR \">\"\n"); break;
        case IFSYM:         printf("IFSYM \"if\"\n"); break;
        case LBRACKET:      printf("LBRACKET \"[\"\n"); break;
        case LCURLY:        printf("LCURLY \"{\"\n"); break;
        case LEQ:           printf("LEQ \"<=\"\n"); break;
        case LPAREN:        printf("LPAREN \"(\"\n"); break;
        case LSS:           printf("LSS \"<\"\n"); break;
        case MINUS:         printf("MINUS \"-\"\n"); break;
        case NEQ:           printf("NEQ \"#\"\n"); break;
        case ORSYM:         printf("ORSYM \"or\"\n"); break;
        case PERCENT:       printf("PERCENT \"%%\"\n"); break;
        case PERIOD:        printf("PERIOD \".\"\n"); break;
        case PLUS:          printf("PLUS \"+\"\n"); break;
        case PRINTSYM:      printf("PRINTSYM \"print\"\n"); break;
        case PROCSYM:       printf("PROCSYMP \"procedure\"\n"); break;
        case RBRACKET:      printf("RBRACKET \"]\"\n"); break;
        case RCURLY:        printf("RCURLY \"}\"\n"); break;
        case RETURNSYM:     printf("RETURNSYM \"return\"\n"); break;
        case RPAREN:        printf("RPAREN \")\"\n"); break;
        case SEMICOLON:     printf("SEMICOLON \";\"\n"); break;
        case SLASH:         printf("SLASH \"/\"\n"); break;
        case THENSYM:       printf("THENSYM \"then\"\n"); break;
        case TIMES:         printf("TIMES \"*\"\n"); break;
        case VARSYM:        printf("VARSYM \"var\"\n"); break;
        case WHILESYM:      printf("WHILESYM \"while\"\n"); break;
        case XORSYM:        printf("WHILESYM \"xor\"\n"); break;

        case ENDOFFILE: printf("ENDOFFILE\n"); break;
        default: printf("Unrecognized symbol\n"); break;
    }
}

// scan.c
int printsymbol(int s) {
    printsymb((Symbol) s);
    return 0;
}

