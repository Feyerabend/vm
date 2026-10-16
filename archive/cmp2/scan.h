
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
    EQL,        // =
    NEQ,        // #
    LSS,        // <
    LEQ,        // <=
    GTR,        // >
    GEQ,        // >=
    CALLSYM,    // call
    BEGINSYM,   // begin
    SEMICOLON,  // ;
    ENDSYM,     // end
    IFSYM,      // if
    WHILESYM,   // while
    BECOMES,    // :=
    THENSYM,    // then
    DOSYM,      // do
    CONSTSYM,   // const
    COMMA,      // ,
    VARSYM,     // var
    PROCSYM,    // proc
    PERIOD,     // .
    ODDSYM,     // odd
    ENDOFFILE
} Symbol;

#define MAXSYMB 100
extern char buf[MAXSYMB];

extern Symbol scan();
extern void printsymb(Symbol s);
