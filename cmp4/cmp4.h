
#define FALSE 0
#define TRUE 1

typedef enum {
    ADD,
    BLANK,
    DIVIDE,
    INUMBER,
    MULTIPLY,
    PRINT,
    PROG,
    SEQ,
    START,
    SUB
} Instr;

typedef struct node {
    int type;
    int value;
    struct node *node1, *node2, *node3;
} node;

// used in scan
extern void setinput(FILE* inputfile);
