#include <stdlib.h> 
#include <stdio.h>
#include <ctype.h>
#include <string.h>

#include "cmp4.h"
#include "scan.h"
#include "error.h"


// some simple error handling

void error(char* msg) {
    printf("error: %s\n", msg);
}

void error2(char* msg, char* msg2) {
    printf("error: %s %s\n", msg, msg2);
}

