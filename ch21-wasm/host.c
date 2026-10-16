/*
 * The host for core.c, as an ordinary C program: the machine as a
 * command, like the machines of earlier chapters.
 *
 *     vm [-g mark | -g copy] [-S] program.vm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void host_write(int c) {
    putchar(c);
}

void host_trap(const char *why, int at) {
    fflush(stdout);
    fprintf(stderr, "trap: %s at %d\n", why, at);
    exit(1);
}

unsigned char *vm_input(void);
int vm_input_size(void);
const char *vm_load(int size);
void vm_reset(void);
void vm_set_collector(int copying, int stressed);
void vm_run(void);

int main(int argc, char *argv[]) {
    int i, copying = 0, stressed = 0, size;
    const char *path, *why;
    FILE *f;

    for (i = 1; i < argc - 1; i++) {
        if (strcmp(argv[i], "-g") == 0 && i + 1 < argc - 1)
            copying = strcmp(argv[++i], "copy") == 0;
        else if (strcmp(argv[i], "-S") == 0)
            stressed = 1;
        else
            break;
    }
    if (argc < 2 || i != argc - 1) {
        fprintf(stderr, "usage: vm [-g mark | -g copy] [-S] program.vm\n");
        return 2;
    }
    path = argv[argc - 1];
    f = fopen(path, "rb");
    if (f == NULL) {
        fprintf(stderr, "%s: cannot open\n", path);
        return 2;
    }
    size = (int) fread(vm_input(), 1, vm_input_size(), f);
    fclose(f);
    why = vm_load(size);
    if (why != NULL) {
        fprintf(stderr, "%s: %s\n", path, why);
        return 2;
    }
    vm_set_collector(copying, stressed);
    vm_reset();
    vm_run();
    return 0;
}
