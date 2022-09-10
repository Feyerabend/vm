#include <stdlib.h> 
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h> 
#include <libgen.h>

#include "enkel.h"
#include "scan.h"
#include "symbol.h"
#include "error.h"


// error
void buffer() {
    fprintf(stderr, " buffer='%s'", buf);
}

// file handling
FILE* file = NULL;
options_t options = { 0, 0x0, NULL, NULL };

// send file pointer to scan
void setinputfile(FILE* inputfile) {
    setinput(inputfile);
}


// ---------------------------
// for parsing
Symbol sym;

void nextsym() {
    sym = scan();

    if (options.verbose != 0) {
        printf("> ");
        printsymbol(sym);
    }
}

int recognize(Symbol s) {
    if (sym == s)
        return TRUE;
    return FALSE;
}

int accept(Symbol s) {
    if (sym == s) {
        nextsym();
        return TRUE;
    }
    return FALSE;
}

int expect(Symbol s) {
    if (recognize(s)) {
        nextsym();
        return TRUE;
    }
    errnum(ERROR_UNRECOGNIZED_SYMBOL);
    printsymbol(s);
    return FALSE;
}

void init() {
    initrval();
}

// ---------------------------
// internal parse tree ('AST')

// new node in parse tree
node* nnode(int type) {
    node* n = (node*) (malloc(sizeof(node)));
    if (n == NULL)
        return NULL;
    n->type = type;
    return n;
}

// free tree
void dnode(node* n) {
    if (n == NULL)
        return;
  
    // branches
    dnode(n->node1);
    dnode(n->node2);
    dnode(n->node3);
    
    // leaf
    free(n);
}


// --------------------------
// helpers AST

// fetch the address of the corresponding variable (identifier)
node* load() {
    node *n;
    n = NULL;

    if (peekcurrent() != NULL) {
        if (localexist(buf, peekcurrent())) {
            n = nnode(LOCALFETCH);
            n->value = getlocal(buf, peekcurrent());
            return n;
        }
    }

    if (globalexist(buf)) {
        n = nnode(FETCH);
        n->value = getglobal(buf);
        return n;
    }

    return n;
}

// get the address (of the array in vm) for storing (some value) at the variable
node* store() {
    node* n;
    n = NULL;

    if (peekcurrent() != NULL) {
        if (localexist(buf, peekcurrent())) {
            n = nnode(LOCALASSIGN); // ST
            n->value = getlocal(buf, peekcurrent());
            return n;
        }
    }

    if (globalexist(buf)) {
        n = nnode(ASSIGN); // STORE
        n->value = getglobal(buf);
        return n;
    }

    return n;
}

node* arrindex() {
    node *n;

    nextsym();
    if (recognize(IDENT)) {
        n = load();
    }
    else if (recognize(NUMBER)) {
        n = nnode(INUMBER);
        n->value = atoi(buf);
    }
    else {
        n = NULL;
        errnum(ERROR_ARRINDEX_UNKNOWN_INDEX_TYPE);
    }

    return n;
}


// PARSING AND AST BUILD
// --------------------------
// forward decl.
node* program();
node* block();
node* procedure();
node* statement();
node* condition();
node* expression();
node* term();
node* factor();


// <factor> = <ident>["." <index>] | <number> | "(" <expression> ")"
node* factor() {
    node *n;

    if (recognize(IDENT)) {
        n = load();
        nextsym();
        if (recognize(PERIOD)) {
            n->type = LARRAY;
            n->node1 = arrindex();
            nextsym();
        }

    } else if (recognize(NUMBER)) {
        n = nnode(INUMBER);
        n->value = atoi(buf);
        nextsym();

    } else if (accept(LPAREN)) {
        n = expression();
        expect(RPAREN);

    } else {
        n = NULL;
        errnum(ERROR_SYNTAX_ERROR);
        nextsym();
    }

    return n;
}

// <term> = <factor> { ("*"|"/"|"and"|"%") <factor> }
node* term() {
    node *m, *n;
    n = factor();
    int h = BLANK;

    while (sym == TIMES || sym == SLASH || sym == PERCENT || sym == ANDSYM) {
        m = n;

        if (sym == TIMES)
            h = MULTIPLY;
        else if (sym == SLASH)
            h = DIVIDE;
        else if (sym == PERCENT)
            h = MOD;
        else if (sym == ANDSYM)
            h = AND;
        else {
            errnum(ERROR_TERM_INVALID_OPERATOR);
            nextsym();
        }

        n = nnode(h);
        nextsym();
        n->node1 = m;
        n->node2 = factor();
    }

    return n;
}

// <expression> = {"-"} <term> { ("+"|"-"|"or"|"xor") <term> }
node* expression() {
    node *m, *n;

    if (recognize(MINUS)) {
        n = nnode(UMINUS);
        nextsym();
        n->node1 = term();

    } else {
        n = term();
    }

    int h = BLANK;

    while (sym == PLUS || sym == MINUS || sym == ORSYM || sym == XORSYM) {
        m = n;

        if (sym == PLUS)
            h = ADD;
        else if (sym == MINUS)
            h = SUB;
        else if (sym == ORSYM)
            h = OR;
        else if (sym == XORSYM)
            h = XOR;
        else {
            errnum(ERROR_EXPRESSION_INVALID_OPERATOR);
            nextsym();
        }

        n = nnode(h);
        nextsym();
        n->node1 = m;
        n->node2 = term();
    }

    return n;
}

// condition = expression ("="|"#"|"<"|">"|"<="|">=") expression
node* condition() {
    node *m, *n;
    n = expression();
    m = n;
    int h = BLANK;

    if (sym == EQL)
        h = EQUAL;          // =
    else if (sym == NEQ)
        h = NOTEQUAL;       // #
    else if (sym == LSS)
        h = LESS;           // <
    else if (sym == GTR)
        h = GREATER;        // >
    else if (sym == LEQ)
        h = LESSEQUAL;      // <= ≤
    else if (sym == GEQ)
        h = GREATEEQUAL;    // >= ≥
    else {
        errnum(ERROR_CONDITION_RELATIONAL_INVALID_OPERATOR);
        nextsym();
    }

    n = nnode(h);
    nextsym();
    n->node1 = m;
    n->node2 = expression();

    return n;
}

// statement = [ ident["." index] "is" expression
//             | "call" ident "[" {"," factor } "]" ";"
//             | "begin" statement {";" statement } "end" 
//             | "if" condition "then" statement { "else" statement }
//             | "do" statement "while" condition
//             | "while" condition "do" statement
//             | "return" [ factor ]
//             | "print" factor
//             | "emit" factor
//             ];
node* statement() {
    node *k, *l, *m, *n;
    n = NULL;

    if (recognize(IDENT)) {
        n = store();
        nextsym();
        if (recognize(PERIOD)) {
            n->type = SARRAY;
            n->node2 = arrindex();
            nextsym();
        }
        expect(BECOMES);
        n->node1 = expression();

    } else if (accept(PRINTSYM)) {
        n = nnode(PRINT);
        n->node1 = factor();

    } else if (accept(EMITSYM)) {
        n = nnode(EMIT);
        n->node1 = factor();

    } else if (accept(RETURNSYM)) {
        n = nnode(RVAL);
        n->node1 = factor();

    } else if (accept(CALLSYM)) {
        expect(IDENT);

        n = nnode(CALLPROC);
        n->value = getconnectnumber(buf);

        int address = 0;
        l = nnode(BLANK);

        expect(LBRACKET);
        if (!recognize(RBRACKET)) {
            do {
                k = l;

                m = nnode(PARAMASSIGN);
                m->value = address;
                m->node1 = factor();

                l = nnode(SEQ);
                l->node1 = k;
                l->node2 = m;

                ++address;

            } while (accept(COMMA));
        }
        expect(RBRACKET);
        n->node1 = l;

    } else if (accept(BEGINSYM)) {
        n = nnode(BLANK);
        do {
            m = n;
            n = nnode(SEQ);
            n->node1 = m;
            n->node2 = statement();
        } while (accept(SEMICOLON));
        expect(ENDSYM);

    } else if (accept(IFSYM)) {
        n = nnode(IF);
        int a = labelincrease();
        int b = labelincrease();
        n->value = packint(a, b);
        n->node1 = condition();
        expect(THENSYM);
        n->node2 = statement();
        if (accept(ELSESYM)) {
            n->type = IFELSE;
            n->node3 = statement();
        }

    } else if (accept(WHILESYM)) {
        n = nnode(WHILE);
        int a = labelincrease();
        int b = labelincrease();
        n->value = packint(a, b);
        n->node1 = condition();
        expect(DOSYM);
        n->node2 = statement();

    } else if (accept(DOSYM)) {
        n = nnode(DO);
        n->value = labelincrease();
        n->node1 = statement();
        expect(WHILESYM);
        n->node2 = condition();

    } else {
        errnum(ERROR_SYNTAX_ERROR);
        nextsym();
    }

    return n;
}

// flags for setting START
int startflag = FALSE;
int startflagset = FALSE;

// procedure = { "procedure" ident "[" {"," ident} "]" ";" block ";" }
node* procedure() {
    node *k, *l, *m, *n, *p, *q, *r, *s;
    n = NULL;

    while (accept(PROCSYM)) {
        expect(IDENT);
        pushcurrent(buf);

        p = nnode(PROCEDURE);
        p->value = getconnectnumber(buf);

        resetlocal();
        int address = 0;
        k = nnode(BLANK);

        expect(LBRACKET);
        if (recognize(IDENT)) {
            do {
                expect(IDENT);

                if (localexist(buf, peekcurrent())) {
                    errnum(ERROR_PREVIOUS_DECLARATION_PARAMETER);
                    buffer();
                } else {
                    setlocal(buf, peekcurrent(), address);
                }

                m = nnode(PARAMSTORE);
                m->value = address;

                l = k;
                k = nnode(SEQ);
                k->node1 = l;
                k->node2 = m;

                address = newlocal();

            } while (accept(COMMA));
        }
        expect(RBRACKET);

        expect(SEMICOLON);
        r = block();
        expect(SEMICOLON);

        s = nnode(SEQ);
        s->node1 = k; // parameters
        s->node2 = r; // block

        p->node1 = s;

        popcurrent();

        if (n == NULL)
            n = nnode(BLANK);
        q = n;
        n = nnode(SEQ);
        n->node1 = q;
        n->node2 = p;
    }

    return n;
}


// block = [ "const" ident "=" number {"," ident "=" number} ";"]
//         [ "array" ident ":" number {"," ident ":" number} ";"]
//         [ "var" ident {"," ident} ";"]
//         { procedure }
//           statement

int initflag = FALSE;
int initflagset = FALSE;

node* block() {
    node *k, *l, *m, *n;
    n = nnode(BLANK);
    int address;

    if (accept(CONSTSYM)) {
        do {
            expect(IDENT);

            if (globalexist(buf)) {
                errnum(ERROR_PREVIOUS_DECLARATION_CONSTANT);
                buffer();
            } else {
                address = newglobal();
                setglobal(buf, address, CONSTANT_TYPE);
            }
            expect(EQL);
            expect(NUMBER);

            k = nnode(INUMBER);
            k->value = atoi(buf);

            m = nnode(ASSIGN);
            m->value = address;
            m->node1 = k;

            l = n;
            n = nnode(SEQ);
            n->node1 = l;
            n->node2 = m;

        } while (accept(COMMA));
        expect(SEMICOLON);

        initflag = TRUE;
    }

    if (accept(ARRAYSYM)) {
        do {
            expect(IDENT);

            if (globalexist(buf)) {
                errnum(ERROR_PREVIOUS_DECLARATION_ARRAY);
                buffer();
            } else {
                address = newglobal();
                setglobal(buf, address, ARRAY_TYPE);
            }
            expect(COLON);
            expect(NUMBER);

            int length = atoi(buf);
            int offset = nextoffset(length);

            k = nnode(INUMBER);
            k->value = offset;

            m = nnode(ASSIGN);
            m->value = address;
            m->node1 = k;

            l = n;
            n = nnode(SEQ);
            n->node1 = l;
            n->node2 = m;

        } while (accept(COMMA));
        expect(SEMICOLON);

        initflag = TRUE;
    }

    if (accept(VARSYM)) {
        do {
            expect(IDENT);

            if (peekcurrent() ==  NULL) {
                if (globalexist(buf)) {
                    errnum(ERROR_PREVIOUS_DECLARATION_GLOBAL_VARIABLE);
                    buffer();
                }
                else {
                    address = newglobal();
                    setglobal(buf, address, VARGLOBAL_TYPE);
                }
            }
            else {
                if (localexist(buf, peekcurrent())) {
                    errnum(ERROR_PREVIOUS_DECLARATION_LOCAL_VARIABLE);
                    buffer();
                }
                else {
                    address = newlocal();
                    setlocal(buf, peekcurrent(), address);
                }
            }
        } while (accept(COMMA));
        expect(SEMICOLON);
    }

    if (initflag == TRUE) {
        l = n;
        n = nnode(INIT);
        n->node1 = l;

        initflag = FALSE;
        initflagset = TRUE;
    }

    if (recognize(PROCSYM)) {
        m = procedure();

        if (m == NULL)
            m = nnode(BLANK);
        l = n;
        n = nnode(SEQ);
        n->node1 = l;
        n->node2 = m;

        startflag = TRUE;
    }

    if (startflag == TRUE) {
        l = n;
        n = nnode(SEQ);
        n->node1 = l;
        if (initflagset == TRUE)
            n->node2 = nnode(STARTW);
        else
            n->node2 = nnode(START);

        // only once
        startflagset = TRUE;
        startflag = FALSE;
    }

    m = n;
    n = nnode(SEQ);
    n->node1 = m;
    n->node2 = statement();

    return n;
}

// program = block "."
node* program() {
    node *m, *n;
    n = nnode(PROG);
    nextsym();
    n->node1 = block();
    if (startflagset == FALSE) { // no procedures
        m = n;
        n = nnode(SEQ);
        if (initflagset == TRUE)
            n->node1 = nnode(STARTWC);
        else
            n->node1 = nnode(START); // no inits
        n->node2 = m;
    }
    expect(PERIOD);
    return n;
}


// CODE GENERATION
// ---------------------------
// generate instructions for assembler
// from parse tree
void compile(node *n) {

    if (n == NULL)
        return;

    switch (n->type) {

        case ADD:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tADD\n");
            break;

        case AND:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tAND\n");
            break;

        case ASSIGN:
            compile(n->node1);
            fprintf(file, "\tSTORE %d\n", n->value);
            break;

        case BLANK:
            break;

        case CALLPROC:
            compile(n->node1);
            fprintf(file, "\tCALL :%s\n", connects(n->value));
            break;

        case DIVIDE:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tDIV\n");
            break;

        case DO:
            fprintf(file, "%s:\n", label(n->value));
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tJPNZ ");
            fprintf(file, ":%s\n", label(n->value));
            break;

        case EMIT:
            compile(n->node1);
            fprintf(file, "\tEMIT\n");
            break;

        case EQUAL:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tEQ\n");
            break;

        case FETCH:
            fprintf(file, "\tLOAD %d\n", n->value);
            break;

        case GREATER:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tGT\n");            
            break;

        case GREATEEQUAL:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tGQ\n");            
            break;

        case IF:
            compile(n->node1);
            fprintf(file, "\tJPZ ");
            fprintf(file, ":%s\n", labela(n->value));
            compile(n->node2);
            fprintf(file, "%s:\n", labela(n->value));
            break;

        case IFELSE:
            compile(n->node1);
            fprintf(file, "\tJPZ ");
            fprintf(file, ":%s\n", labela(n->value));
            compile(n->node2);
            fprintf(file, "\tJP ");
            fprintf(file, ":%s\n", labelb(n->value));
            fprintf(file, "%s:\n", labela(n->value));
            compile(n->node3);
            fprintf(file, "%s:\n", labelb(n->value));
            break;

        case INIT:
            fprintf(file, "INIT:\n");
            compile(n->node1);
            fprintf(file, "\tRET\n");
            fprintf(file, "CONT:\n");
            break;

        case INUMBER:
            fprintf(file, "\tSET %d\n", n->value);
            break;

        case LARRAY:
            compile(n->node1);
            fprintf(file, "\tLOAD %d\n", n->value);
            fprintf(file, "\tADD\n");
            fprintf(file, "\tRLOAD\n");
            break;

        case LESS:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tLT\n");            
            break;

        case LESSEQUAL:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tLQ\n");            
            break;

        case LOCALASSIGN:
            compile(n->node1);
            fprintf(file, "\tST %d\n", n->value);
            break;

        case LOCALFETCH:
            fprintf(file, "\tLD %d\n", n->value);
            break;

        case MOD:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tMOD\n");
            break;

        case MULTIPLY:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tMUL\n");
            break;

        case NOTEQUAL:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tNEQ\n");
            break;

        case OR:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tOR\n");
            break;

        case PARAMASSIGN:
            compile(n->node1);
            fprintf(file, "\tSTARG %d\n", n->value);
            break;

        case PARAMSTORE:
            fprintf(file, "\tLDARG %d\n", n->value);
            fprintf(file, "\tST %d\n", n->value);
            break;

        case PRINT:
            compile(n->node1);
            fprintf(file, "\tPRINT\n");
            break;

        case PROCEDURE:
            fprintf(file, "\n%s:\t\n", connects(n->value));
            compile(n->node1);
            fprintf(file, "\tRET\n");
            break;

        case PROG:
            compile(n->node1);
            fprintf(file, "\tHALT\n");
            break;

        case RETURN:
            fprintf(file, "\tRET\n");
            break;

        case RVAL:
            compile(n->node1);
            fprintf(file, "\tSTORE 0\n");
            fprintf(file, "\tRET\n");
            break;

        case SARRAY:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tLOAD %d\n", n->value);
            fprintf(file, "\tADD\n");
            fprintf(file, "\tRSTORE\n");

        case SEQ:
            compile(n->node1);
            compile(n->node2);
            break;

        case START:
            fprintf(file, "START:\n");
            break;

        case STARTW:
            fprintf(file, "START:\n");
            fprintf(file, "\tCALL :INIT\n");
            break;

        case STARTWC:
            fprintf(file, "START:\n");
            fprintf(file, "\tCALL :INIT\n");
            fprintf(file, "\tJP :CONT\n");
            break;

        case SUB:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tSUB\n");
            break;

        case UMINUS:
            compile(n->node1);
            fprintf(file, "\tUMIN\n");
            break;

        case WHILE:
            fprintf(file, "%s:\n", labela(n->value));
            compile(n->node1);
            fprintf(file, "\tJPZ ");
            fprintf(file, ":%s\n", labelb(n->value));
            compile(n->node2);
            fprintf(file, "\tJP ");
            fprintf(file, ":%s\n", labela(n->value));
            fprintf(file, "%s:\n", labelb(n->value));
            break;

        case XOR:
            compile(n->node1);
            compile(n->node2);
            fprintf(file, "\tXOR\n");
            break;

        default:
            // errnum(compile: unknown node identifier);
            break;
    }
}

void usage(char *progname, int opt) {
    fprintf(stderr, USAGE, progname ? progname : DEFAULT_PROGNAME);
    exit(EXIT_FAILURE);
}

int compiling(options_t *options) {

    if (!options) {
        //errno = EINVAL;
        return EXIT_FAILURE;
    }

    if (!options->input || !options->output) {
        //errno = ENOENT;
        return EXIT_FAILURE;
    }

    file = options->output;
    setinputfile(options->input);
    init(); // rval init

    if (options->verbose)
        printf("parsing ..\n");
    node* n = program();
    if (options->verbose)
        printf("done parsing.\n");    

    if (options->verbose)
        printf("compiling ..\n");
    compile(n);
    if (options->verbose)
        printf("done compiling.\n");

    if (options->flags == 0x01)
        printglobal();
    if (options->flags == 0x02)
        printlocal();

    destroysymbols();
    dnode(n);

    return EXIT_SUCCESS;
}

int main(int argc, char *argv[]) {
    int opt;
    opterr = 0;
    options.input = stdin;
    options.output = stdout;

    while ((opt = getopt(argc, argv, OPTSTR)) != EOF) {
        switch(opt) {
            case 'i':
                if (! (options.input = fopen(optarg, "r")) ) {
                    perror(ERR_FOPEN_INPUT);
                    exit(EXIT_FAILURE);
                }
                break;

            case 'o':
                if (! (options.output = fopen(optarg, "w")) ) {
                    perror(ERR_FOPEN_OUTPUT);
                    exit(EXIT_FAILURE);
                }
                break;

            case 'f': // limit error messages?
                options.flags = (uint32_t) strtoul(optarg, NULL, 16);
                break;

            case 'v':
                options.verbose += 1;
                break;

            case 'h':
            default:
                usage(basename(argv[0]), opt);
                break;
        }
    }

    // pointer for starting at input file at 0
    if (options.input)
        fseek(options.input, 0, SEEK_SET);

    if (compiling(&options) != EXIT_SUCCESS) {
        perror(ERR_COMPILER);
        exit(EXIT_FAILURE);
    }

    fclose(options.input);
    fclose(options.output);

    return EXIT_SUCCESS;
}

