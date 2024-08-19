#include <stdio.h>
#include <stdlib.h>

#define INITIAL_HEAP_SIZE 10
#define HEAP_INCREMENT 10

typedef struct Object {
    int marked;  // mark flag
    struct Object* next;  // linked list for references
} Object;

typedef struct Heap {
    Object** objects;  // dynamically allocated array of pointers
    int size;  // current size of the heap array
    int capacity;  // current capacity of the heap array
} Heap;

Heap heap;  // global heap

// root
Object* root = NULL;

// initialize the heap
void initialize_heap() {
    heap.capacity = INITIAL_HEAP_SIZE;
    heap.size = 0;
    heap.objects = (Object**)malloc(heap.capacity * sizeof(Object*));
    if (heap.objects == NULL) {
        perror("Failed to initialize heap");
        exit(1);
    }
}

// extend heap capacity
void extend_heap() {
    heap.capacity += HEAP_INCREMENT;
    heap.objects = (Object**)realloc(heap.objects, heap.capacity * sizeof(Object*));
    if (heap.objects == NULL) {
        perror("Failed to extend heap");
        exit(1);
    }
}

// fwd decl.
void mark_and_sweep();

// allocate a new object, trigger GC if needed
Object* new_object() {
    if (heap.size >= heap.capacity) {
        printf("Heap full, running garbage collection...\n");
        mark_and_sweep();
        if (heap.size >= heap.capacity) {
            printf("Out of memory!\n");
            exit(1);
        }
    }

    Object* obj = (Object*)malloc(sizeof(Object));
    if (obj == NULL) {
        perror("Failed to allocate object");
        exit(1);
    }
    obj->marked = 0;
    obj->next = NULL;
    heap.objects[heap.size++] = obj;
    return obj;
}

// mark all reachable objects
void mark(Object* obj) {
    if (obj == NULL || obj->marked) return;

    obj->marked = 1;
    printf("Marking object at %p\n", (void*)obj);

    // mark connected objects
    if (obj->next) {
        mark(obj->next);
    }
}

void mark_all() {
    mark(root);
}

// sweep the heap and free unmarked objects
void sweep() {
    for (int i = 0; i < heap.size; i++) {
        if (heap.objects[i]->marked) {
            heap.objects[i]->marked = 0;  // unmark for next GC cycle
        } else {
            printf("Sweeping object at %p\n", (void*)heap.objects[i]);
            free(heap.objects[i]);
            heap.objects[i] = heap.objects[--heap.size];  // replace with last object
            i--;  // index after removal
        }
    }
}

// garbage collection
void mark_and_sweep() {
    mark_all();
    sweep();
}

// display/list objects
void list_objects() {
    printf("List:\n");
    for (int i = 0; i < heap.size; i++) {
        printf("Object: %p\n", (void*)heap.objects[i]);
    }
    printf("Number of objects: %d\n", heap.size);
}

// create a chain of objects
void create_object_chain(int length) {
    Object* current = new_object();
    root = current;
    printf("New object root\n");
    for (int i = 1; i < length; i++) {
        current->next = new_object();
        current = current->next;
        printf("New object linked\n");
    }
}

// remove root reference (simulate losing reference)
void lose_root_reference() {
    printf("Lost root\n");
    root = NULL;
}

int main() {
    initialize_heap();
    printf("Start\n");

    create_object_chain(3);  // chain of 3 objects
    lose_root_reference();  // lose root
    list_objects(); // some objects listed
    mark_and_sweep(); // objects should be collected
    printf("\n");

    create_object_chain(9);  // chain of 9 objects
    create_object_chain(1);  // "chain" of 1 object
    list_objects();
    printf("\n");

    printf("One more ..\n");
    new_object();  // trigger GC
    list_objects();
    printf("End\n");

    printf("Clean up all\n");
    mark_and_sweep();
    free(heap.objects);

    return 0;
}
