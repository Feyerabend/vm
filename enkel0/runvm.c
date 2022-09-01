#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "vmenkel.h"


// enough for the samples?
int VARS = 2048;
int ARGS = 2048;
int ARRAYS = 2048;
int MAXPROGLEN = 32768;
int* program;

// 
void allocateprogram() {
	program = (int*) malloc(MAXPROGLEN * sizeof(int));
	if (program == NULL) {
		fprintf(stderr, "Runtime: unable to allocate memory for loading program.");
	    exit(EXIT_FAILURE);
	}
}

// 
long fsize(FILE* file) {
    fseek(file, 0L, SEEK_END);
    long size = ftell(file);
    rewind(file);
    return size;
}

// 
char* read(char *path) {
    FILE* file;
    file = fopen(path, "rb");
    long size = fsize(file);
    char* buf = (char*) calloc(1, size + 1);
    fread(buf, size, 1, file);
    fclose(file);
    return buf;
}

// 
void exec(int* code, int start) {
	VM* vm = newVM(code, start, VARS, ARGS, ARRAYS);
	if (vm != NULL) {
		run(vm);
		freeVM(vm);
	}
}

// 
int main(int argc, char *argv[]) {
	printf("loading ..\n");

	// get the "binary" file
	char* source = read(argv[1]);
	allocateprogram();

	// parse numbers separated by comma
	const char s[2] = ",";
	char *token;
  	token = strtok(source, s);

  	// header
	int start = atoi(token);

	// body
	int i = 0;
	token = strtok(NULL, s);
	while (token != NULL) {
		program[i] = atoi(token);
		token = strtok(NULL, s);
		i++;
	}

	// print loaded prog (change \r to \n)
	printf("%d:\r", start);
	int j = 0;
	do {
		printf("%d\r", program[j]);
		j++;
	}
	while (j < i);

	// 
	printf("running ..\n");
	printf("- - - - - - - - - - - -\n");
	clock_t t;
	t = clock();
	exec(program, start);
	t = clock() - t;
	printf("- - - - - - - - - - - -\n");
	double duration = ((double) t) / CLOCKS_PER_SEC;
	printf("duration %f seconds\n", duration);
	printf("done running.\n");

	return 0;
}

/* EOF */
