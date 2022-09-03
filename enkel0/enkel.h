
#define FALSE 0
#define TRUE 1

#define DEFAULT_PROGNAME "compiler"
#define USAGE "%s [-v] [-f hexflag] [-i inputfile] [-o outputfile] [-h]"
#define ERR_FOPEN_INPUT "fopen(input, r)"
#define ERR_FOPEN_OUTPUT "fopen(output, w)"
#define ERR_COMPILER "compiling error"
#define OPTSTR "vi:o:f:h"

// ---------------------------
// *internal* parse tree ('AST'),
// enum, constr, init, helpers ..

typedef enum {
    ADD,
    AND,
    ARRAY,
    ASSIGN,
    BLANK,
    CALLPROC,
    DIVIDE,
    DO,
    EMIT,
    EQUAL,
    FETCH,
    GREATEEQUAL,
    GREATER,
    IF,
    IFELSE,
    INIT,
    INUMBER,
    LARRAY,
    LESS,
    LESSEQUAL,
    LOCALASSIGN,
    LOCALFETCH,
    MOD,
    MULTIPLY,
    NOT,
    NOTEQUAL,
    OR,
    PARAMASSIGN,
    PARAMSTORE,
    PRINT,
    PROCEDURE,
    PROG,
    RETURN,
    RVAL,
    SARRAY,
    SEQ,
    START,
    STARTW,
    STARTWC,
    SUB,
    UMINUS,
    WHILE,
    XOR
} Nodelabels;

// parse tree
typedef struct node {
    int type;
    int value;
    struct node *node1, *node2, *node3;
} node;

// file handling
typedef struct options_t {
    int verbose;
    uint32_t flags;
    FILE *input, *output;
} options_t;

// used in scan
extern void setinput(FILE* inputfile);

extern int errno;
extern char* optarg;
extern int opterr, optind;
