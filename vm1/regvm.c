#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PROGRAM_SIZE 100
#define MAX_REGISTERS 4

typedef struct {
    int pc;
    int registers[MAX_REGISTERS]; // A, B, C, D
    int flags[2]; // Z, N
    char *memory[MAX_PROGRAM_SIZE];
} REGVM;

// fwd decl
void init_vm(REGVM *vm);
void load_program(REGVM *vm, char *program[], int size);
void fetch(REGVM *vm, char **instruction);
int decode_and_execute(REGVM *vm, char *instruction);
void update_flags(REGVM *vm, int value);
void run(REGVM *vm);
int get_value(REGVM *vm, char *arg);


void init_vm(REGVM *vm) {
    vm->pc = 0;
    memset(vm->registers, 0, sizeof(vm->registers));
    memset(vm->flags, 0, sizeof(vm->flags));
    memset(vm->memory, 0, sizeof(vm->memory));
}

void load_program(REGVM *vm, char *program[], int size) {
    for (int i = 0; i < size; i++) {
        vm->memory[i] = program[i];
    }
}

void fetch(REGVM *vm, char **instruction) {
    if (vm->pc < MAX_PROGRAM_SIZE && vm->memory[vm->pc] != NULL) {
        *instruction = vm->memory[vm->pc];
        vm->pc++;
    } else {
        *instruction = NULL;
    }
}

int get_value(REGVM *vm, char *arg) {
    if (arg[0] >= 'A' && arg[0] <= 'D') {
        return vm->registers[arg[0] - 'A'];
    } else {
        return atoi(arg);
    }
}

int decode_and_execute(REGVM *vm, char *instruction) {
    if (!instruction)
        return 0;

    char opcode[4];
    char arg1[2];
    char arg2[10];
    // careful ..
    sscanf(instruction, "%s %s %s", opcode, arg1, arg2);

    int val1, val2;

    if (strcmp(opcode, "MOV") == 0) {
        val1 = (arg1[0] - 'A');
        vm->registers[val1] = get_value(vm, arg2);

    } else if (strcmp(opcode, "ADD") == 0) {
        val1 = (arg1[0] - 'A');
        vm->registers[val1] += get_value(vm, arg2);
        update_flags(vm, vm->registers[val1]);

    } else if (strcmp(opcode, "SUB") == 0) {
        val1 = (arg1[0] - 'A');
        vm->registers[val1] -= get_value(vm, arg2);
        update_flags(vm, vm->registers[val1]);

    } else if (strcmp(opcode, "MUL") == 0) {
        val1 = (arg1[0] - 'A');
        vm->registers[val1] *= get_value(vm, arg2);
        update_flags(vm, vm->registers[val1]);

    } else if (strcmp(opcode, "CMP") == 0) {
        val1 = get_value(vm, arg1);
        val2 = get_value(vm, arg2);
        vm->flags[0] = (val1 == val2) ? 1 : 0;

    } else if (strcmp(opcode, "JMP") == 0) {
        vm->pc = atoi(arg1);

    } else if (strcmp(opcode, "JZ") == 0) {
        if (vm->flags[0]) {
            vm->pc = atoi(arg1);
        }

    } else if (strcmp(opcode, "PRINT") == 0) {
        val1 = (arg1[0] - 'A');
        printf("Register %c: %d\n", arg1[0], vm->registers[val1]);

    } else {
        fprintf(stderr, "Unknown opcode: %s\n", opcode);
        return 0;
    }

    return 1;
}

void update_flags(REGVM *vm, int value) {
    vm->flags[0] = (value == 0) ? 1 : 0;  // Zero
    vm->flags[1] = (value < 0) ? 1 : 0;   // Negative
}

void run(REGVM *vm) {
    char *instruction;
    while (1) {
        fetch(vm, &instruction);
        if (!instruction || !decode_and_execute(vm, instruction)) {
            break;
        }
    }
}

int main() {
    REGVM vm;
    init_vm(&vm);

    char *factorial[] = {
        "MOV A 1",
        "MOV B 5",
        "CMP B 0",
        "JZ 7",
        "MUL A B",
        "SUB B 1",
        "JMP 3",
        "PRINT A"
    };

    load_program(&vm, factorial, sizeof(factorial) / sizeof(factorial[0]));
    run(&vm);

    return 0;
}
