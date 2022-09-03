
typedef enum {
    IDENT,
    NUMBER,

    ANDSYM,     // and
    ARRAYSYM,   // array
    BECOMES,    // is
    BEGINSYM,   // begin
    CALLSYM,    // call
    COLON,      // :
    COMMA,      // ,
    CONSTSYM,   // const
    DOSYM,      // do
    ELSESYM,    // else
    EMITSYM,    // emit
    ENDSYM,     // end
    EQL,        // =
    EXCLAMATION,// !
    GEQ,        // >=
    GTR,        // >
    IFSYM,      // if
    LBRACKET,   // [
    LCURLY,     // {
    LEQ,        // <=
    LPAREN,     // (
    LSS,        // <
    MINUS,      // -
    NEQ,        // #
    ORSYM,      // or
    PERCENT,    // %
    PERIOD,     // .
    PLUS,       // +
    PRINTSYM,   // print
    PROCSYM,    // proc
    RBRACKET,   // ]
    RCURLY,     // }
    RETURNSYM,  // return
    RPAREN,     // )
    SEMICOLON,  // ;
    SLASH,      // /
    THENSYM,    // then
    TIMES,      // *
    VARSYM,     // var
    WHILESYM,   // while
    XORSYM,     // xor

    ENDOFFILE
} Symbol;


#define MAXSYMB 4096
extern char buf[MAXSYMB];

extern Symbol scan();
extern void printsymb(Symbol s);
