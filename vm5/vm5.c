#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define INITIAL_HEAP_SIZE 5
#define HEAP_INCREMENT 5

typedef struct Object {
    int marked;
    struct Object* next;
    int value;
} Object;

typedef struct Heap {
    Object** objects;
    int size;
    int capacity;
} Heap;

Heap heap;
Object* root = NULL;

// some instructions
enum {
    ADD_NUM,
    DELETE_NUM,
    PRINT_LIST,
    HALT
};

void initialize_heap() {
    heap.capacity = INITIAL_HEAP_SIZE;
    heap.size = 0;
    heap.objects = (Object**)malloc(heap.capacity * sizeof(Object*));
    if (heap.objects == NULL) {
        perror("Failed to initialize heap");
        exit(1);
    }
}

void extend_heap() {
    heap.capacity += HEAP_INCREMENT;
    heap.objects = (Object**)realloc(heap.objects, heap.capacity * sizeof(Object*));
    if (heap.objects == NULL) {
        perror("Failed to extend heap");
        exit(1);
    }
}

void mark(Object* obj) {
    if (obj == NULL || obj->marked) return;
    obj->marked = 1;
    if (obj->next) {
        mark(obj->next);
    }
}

void mark_all() {
    mark(root);
}

void sweep() {
    for (int i = 0; i < heap.size; ) {
        if (heap.objects[i]->marked) {
            heap.objects[i]->marked = 0;
            i++;
        } else {
            free(heap.objects[i]);

            // move last object to current index
            heap.objects[i] = heap.objects[--heap.size];

            // avoid processing moved object twice
            // index only increases i++ if we keep current object.
        }
    }
}

void mark_and_sweep() {
    mark_all();
    sweep();
}

Object* new_object(int value) {
    if (heap.size >= heap.capacity) {
        printf("Heap full, running garbage collection...\n");
        mark_and_sweep();
        if (heap.size >= heap.capacity) {
            extend_heap();
        }
    }

    Object* obj = (Object*)malloc(sizeof(Object));
    if (obj == NULL) {
        perror("Failed to allocate object");
        exit(1);
    }
    obj->marked = 0;
    obj->value = value;
    obj->next = NULL;
    heap.objects[heap.size++] = obj;
    return obj;
}

void add_num(int value) {
    Object* obj = new_object(value);
    if (root == NULL) {
        root = obj;
    } else {
        Object* current = root;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = obj;
    }
}

void delete_num(int index) {
    if (root == NULL) {
        printf("List is empty, nothing to delete.\n");
        return;
    }

    Object* current = root;
    Object* prev = NULL;

    for (int i = 0; i < index; i++) {
        if (current == NULL) {
            printf("Index out of bounds.\n");
            return;
        }
        prev = current;
        current = current->next;
    }

    if (prev == NULL) {
        root = current->next;
    } else {
        prev->next = current->next;
    }

    // remove object from heap list
    for (int i = 0; i < heap.size; i++) {
        if (heap.objects[i] == current) {
            free(current);
            heap.objects[i] = heap.objects[--heap.size];
            break;
        }
    }

    mark_and_sweep();
}

void print_list() {
    Object* current = root;
    if (current == NULL) {
        printf("List is empty.\n");
        return;
    }
    printf("List: ");
    while (current != NULL) {
        printf("%d ", current->value);
        current = current->next;
    }
    printf("\n");
}

// more of vm
void run_vm(int* code) {
    int pc = 0;
    bool running = true; // flag running

    while (running) {
        int instruction = code[pc++];
        int value, index;

        switch (instruction) {
            case ADD_NUM:
                value = code[pc++];
                add_num(value);
                break;

            case DELETE_NUM:
                index = code[pc++];
                delete_num(index);
                break;

            case PRINT_LIST:
                print_list();
                break;

            case HALT:
                running = false;
                break;

            default:
                printf("Unknown instruction %d\n", instruction);
                running = false;
                break;
        }
    }
}

int main() {
    initialize_heap();

    // trigger GC by adding more numbers, than initial heap size
    int program[] = {
        ADD_NUM, 10,
        ADD_NUM, 20,
        ADD_NUM, 30,
        ADD_NUM, 40,
        ADD_NUM, 50,  // heap should be full after this
        PRINT_LIST,  // GC should kick in, if we try to add another object
        ADD_NUM, 60,  // trigger GC .. extend
        PRINT_LIST,
        DELETE_NUM, 0,  // delete first element to free space
        ADD_NUM, 70,  // adding after deletion
        PRINT_LIST,
        HALT
    };

    run_vm(program);
    mark_and_sweep();  // gc before exit
    free(heap.objects);
    return 0;
}
