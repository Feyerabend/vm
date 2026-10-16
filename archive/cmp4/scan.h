
typedef enum {
    NOP,
    IDENT,
    NUMBER,
    LPAREN,     // (
    RPAREN,     // )
    TIMES,      // *
    SLASH,      // /
    PLUS,       // +
    MINUS,      // -
    SEMICOLON,  // ;
    PRINTSYM,   // print
    PERIOD,     // .
    ENDOFFILE
} Symbol;

#define MAXSYMB 4096
extern char buf[MAXSYMB];

extern Symbol scan();
extern void printsymb(Symbol s);
