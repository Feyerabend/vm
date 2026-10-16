#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "error.h"
#include "symbol.h"


// errors
void printerr(char *str1, char *str2) {
    fprintf(stderr, " %s='%s'", str1, str2);
}

// packing numbers in short

int16_t unpacka(int32_t x) {
   return (int16_t) (((uint32_t) x) >> 16);
}

int16_t unpackb(int32_t x) {
   return (int16_t) (((uint32_t) x) & 0xffff);
}

int32_t pack(int16_t a, int16_t b) {
   return (int32_t) ((((uint32_t) a) << 16) + (uint32_t) b);
}

// extern: returns a packed 32-bit int with two 16-bit ints
int packint(int a, int b) {
    return (int) pack((int16_t) a, (int16_t) b);
}


// label creation
// for calls (C0001) and jumps (L0001)
// sets, checks a label at destination and source

#define LABEL_MAX 6
char labelarr[LABEL_MAX];
int labelcount = 1;

int labelincrease() {
    labelcount++;
    return labelcount;
} 

int labelnumber() {
    return labelcount;
}

char* label1(){
    return labelarr;
}

int createconnect(int labelnumber) {
    return snprintf(labelarr, LABEL_MAX, "C%04d", labelnumber);    
}

char* connects(int value) {
    createconnect(value);
    return labelarr;
}

int createlabel(int labelnumber) {
    return snprintf(labelarr, LABEL_MAX, "L%04d", labelnumber);
}

char* label(int value) {
    createlabel(value);
    return labelarr;
}

int newlabel() {
    int count = createlabel(labelnumber());
    if (count >= 0 && count < LABEL_MAX) {
        labelincrease();
        return TRUE;
    }
    return FALSE;
}


// unpacking labels
// because limit of only one integer, we pack
// sometimes two labels in one integer

char* labela(int value) {
    int a = (int) unpacka((int32_t) value);
    createlabel(a);
    return label1();
}

char* labelb(int value) {
    int b = (int) unpackb((int32_t) value);
    createlabel(b);
    return label1();
}


// the counter that controls offsets for arrays
// contained in one larger array container in vm
int arraycount = 0;

int nextoffset(int length) {
    int offset = arraycount;
    arraycount = arraycount + length;
    return offset;
}


// general functions

// new node for list
snode* allocatesnode() {
    snode* n = (snode *) (malloc(sizeof(snode)));
    if (n == NULL)
        return NULL;
    return n;
}

// push a fresh node on list
void push(snode** head_ref, Type type, char* str1, char* str2, int value) {

    // new head
    snode* n = allocatesnode();

    // if str1, copy to new snode
    if (strcmp(str1, "")) {
        n->str1 = malloc(strlen(str1) + 1);
        strcpy(n->str1, str1);
    }

    // if str2, copy to new snode
    if (strcmp(str2, "")) {
        n->str2 = malloc(strlen(str2) + 1);
        strcpy(n->str2, str2);
    }

    // type, see symboltable.h, value is type dependent
    n->type = type;
    n->value = value;

    // at new head, attach the rest
    n->next = (* head_ref);
    (* head_ref) = n;
}

// pop = delete first snode in list
void pop(snode* n) {
    if (n->next == NULL) {
        // free(n);
        return;
    }
    snode* t = n->next;
    n->type = t->type;
    n->str1 = t->str1;
    n->str2 = t->str2;
    n->value = t->value;
    n->next = t->next;
    free(t);
}

// search operation on snode
snode* searchid(snode* head, char* identifier) {
    snode* current = head;
    while (current != NULL) {
        if (strcmp(current->str1, identifier) == 0) {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

// search operation on snode
snode* searchidlevel(snode* head, char* identifier, char* level) {
    snode* current = head;
    while (current != NULL) {
        if (strcmp(current->str2, level) == 0) {
             if (strcmp(current->str1, identifier) == 0) {
                return current;
            }
        }
        current = current->next;
    }
    return NULL;
}


// connect between call and procedure

snode* connect = NULL;

void setconnectnumber(char* identifier, char* label, int number) {
    push(&connect, CONNECT, identifier, label, number);
}

int connectexistnumber(char* identifier) {
    snode* tmp = searchid(connect, identifier);
    if (tmp != NULL) {
        return tmp->value; // =labelno
    }
    return 0;
}

int getconnectnumber(char* identifier) {
    int num = connectexistnumber(identifier);
    if (num == 0) {
        labelincrease();
        int labelno = labelnumber();
        createlabel(labelno);
        setconnectnumber(identifier, label1(), labelno);
        return labelno;
    }
    return num;
}


// current (procedure) identifier used for/by locals
// to seperate them, as the can have the same names

snode* currentlevel = NULL;

void pushcurrent(char* identifier) {
    push(&currentlevel, CURRLEVEL, identifier, "", 0);   
}

void popcurrent() {
    if (currentlevel != NULL)
        pop(currentlevel);
}

char* peekcurrent() {
    if (currentlevel != NULL)
        return currentlevel->str1;
    return NULL;
}


// globals
// such as constants, vars, or arrays

snode* global = NULL;

int globalcount = 0;

int newglobal() {
    globalcount++;
    return globalcount;
}

int globalexist(char* identifier) {
    snode* tmp = searchid(global, identifier);
    if (tmp != NULL) {
        return TRUE;
    }
    return FALSE;
}

int getglobal(char* identifier) {
    snode* tmp = searchid(global, identifier);
    if (tmp != NULL)
        return tmp->value;
    errnum(ERROR_NO_PREVIOUS_DECLARATION_GLOBAL_IDENT);
    printerr("identifier", identifier);
    return 0;
}

void setglobal(char* identifier, int address, int Type) {
    snode* tmp = searchid(global, identifier);
    if (tmp == NULL) {
        // new node global var
        push(&global, Type, identifier, "@global", address);
        return;
    }
    errnum(ERROR_PREVIOUS_DECLARATION_GLOBAL_IDENT);
    printerr("identifier", identifier);
}

// call *once* for init RVAL
void initrval() {
    if (!globalexist("rval"))
        setglobal("rval", 0, VARGLOBAL_TYPE);
}


// locals
// all local variables and parameters
// (at each level ~ procedure identifier)

snode* local = NULL;

int localcount = 0;

int newlocal() {
    localcount++;
    return localcount;
}

void resetlocal() {
    localcount = 0;
}

int getlocal(char* identifier, char* level) {
    snode* current = local;
    while (current != NULL) {
        if (strcmp(current->str2, level) == 0) {
            if (strcmp(current->str1, identifier) == 0) {
                return current->value;
            }
        }
        current = current->next;
    }
    errnum(ERROR_NO_PREVIOUS_DECLARATION_LOCAL_IDENT_LEVEL);
    printerr("identifier", identifier);
    printerr("level", level);
    return 0;
}

void setlocal(char* identifier, char* level, int address) {
    snode* tmp = searchidlevel(local, identifier, level);
    if (tmp == NULL) {
        push(&local, VARLOCAL_TYPE, identifier, level, address);
    } else {
        errnum(ERROR_PREVIOUS_DECLARATION_LOCAL_IDENT_LEVEL);
        printerr("identifier", identifier);
        printerr("level", level);
    }
    return;
}

int localexist(char* identifier, char* level) {
    if (identifier == NULL)
        return FALSE;
    if (level == NULL)
        return FALSE;
    if (searchidlevel(local, identifier, level) == NULL)
        return FALSE;
    return TRUE;
}


// some general routines

// delete (list of) snodes
void dsnode(snode** head_ref) {
    snode *current = *head_ref;
    snode *next;
    while (current != NULL) {
       next = current->next;
       free(current->str2);
       free(current->str1);
       free(current);
       current = next;
   }
   *head_ref = NULL;
}

// delete lists used by "sym table"
void destroysymbols() {
    dsnode(&connect);
    dsnode(&currentlevel);
    dsnode(&global);
    dsnode(&local);

    free(local);
    free(global);
    free(currentlevel);
    free(connect);
}


// small debug operations on snode

// print single snode
void printsnode(snode* n) {
    printf("# str1=%s, str2=%s, type=%d, value=%d\n",
        n->str1, n->str2, n->type, n->value);
}

// print list of snodes
void psnode(snode* n) {
    while (n != NULL) {
        printsnode(n);
        n = n->next;
    }
    printf("\n");
}

void printglobal() {
    psnode(global);
}

void printlocal() {
    psnode(local);
}



/* EOF */