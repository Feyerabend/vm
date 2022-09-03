#define TRUE 1
#define FALSE 0

typedef enum {
    CONSTANT_TYPE = 0x10,   // const x = 1, y = 10, z = 100;            --> str1 = (root or ident), str2 = x, value = 1 ..
    ARRAY_TYPE,
    VARGLOBAL_TYPE,         // var x, y, z;                             --> str1 = (root), str2 = x ..
    VARLOCAL_TYPE,          // var x, y, z;                             --> str1 = a (ident), str2 = x ..
                            // procedure a[x, y, z];                    --> str1 = a (ident), str2 = x ..
    CONNECT,                // call a (:label) -- (label:) procedure a  --> str1 = a (ident), str2 = label ..
    CURRLEVEL               // procedure a                              --> str1 = a
} Type;

typedef struct snode {
    Type type;
    char* str1;
    char* str2;
    int value;
    struct snode* next;
} snode;


// extern(al) functions

// label
extern int labelincrease();
extern int packint(int a, int b);
extern char* label(int value);
extern char* labela(int value);
extern char* labelb(int value);

// current
extern void pushcurrent(char* identifier);
extern void popcurrent();
extern char* peekcurrent();

// connect
extern void setconnectnumber(char* identifier, char* label, int number);
extern int connectexistnumber(char* identifier);
extern int getconnectnumber(char* identifier);
extern char* connects(int value);

// global and constant and array
extern void initrval();
extern int newglobal();
extern int globalexist(char* identifier);
extern int getglobal(char* identifier);
extern void setglobal(char* identifier, int address, int Type);

// local and parameter
extern int newlocal();
extern void resetlocal();
extern int localexist(char* identifier, char* level);
extern int getlocal(char* identifier, char* level);
extern void setlocal(char* identifier, char* level, int address);

// array
extern int nextoffset(int length);

// print (debug)
extern void printglobal();
extern void printlocal();

// when we leave ...
extern void destroysymbols();

