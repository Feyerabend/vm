#include <stdio.h>
#include <stdlib.h>

#define MAX_OBJECTS 10

typedef struct Object {
    int marked;  // mark flag
    struct Object* next;  // a simple linked list ..
} Object;

Object* heap[MAX_OBJECTS];  // heap
int num_objects = 0;  // number of objects on heap

// root
Object* root = NULL;

// fwd decl.
void mark_and_sweep();

// allocate a new object, trigger gc
Object* new_object() {
    if (num_objects >= MAX_OBJECTS) {
        printf("Heap full, running garbage collection...\n");
        mark_and_sweep();
        if (num_objects >= MAX_OBJECTS) {
            printf("Out of memory!\n");
            exit(1);
        }
    }

    Object* obj = (Object*)malloc(sizeof(Object));
    obj->marked = 0;
    obj->next = NULL;
    heap[num_objects++] = obj;
    return obj;
}

// mark all reachable objects
void mark(Object* obj) {
    if (obj == NULL || obj->marked) return;

    obj->marked = 1;  // mark as live!
    printf("Marking object at %p\n", (void*)obj);

    // mark connected objects
    if (obj->next) {
        mark(obj->next);
    }
}

// mark all roots
void mark_all() {
    mark(root);
}

// sweep the heap and free unmarked objects
void sweep() {
    for (int i = 0; i < num_objects; i++) {
        if (heap[i]->marked) {
            heap[i]->marked = 0;  // unmark for next GC cycle
        } else {
            printf("Sweeping object at %p\n", (void*)heap[i]);
            free(heap[i]);
            heap[i] = heap[--num_objects];  // replace with the last object in the heap
            i--;  // .. index
        }
    }
}

// run garbage collection
void mark_and_sweep() {
    mark_all();
    sweep();
}

// show objects
void list_objects() {
    printf("List:\n");
    for (int i = 0; i < num_objects; i++) {
        printf("Object: %p\n", (void*)heap[i]);
    }
    printf("Number of objects: %d\n", num_objects);
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

// remove the root reference (simulate losing reference)
void lose_root_reference() {
    printf("Lost root\n");
    root = NULL;
}

int main() {
    printf("Start\n");

    create_object_chain(3);  // chain of 3 objects
    lose_root_reference();  // lose root
    list_objects(); // some objects listed
    mark_and_sweep(); // objects should be collected
    printf("\n");

    create_object_chain(9);  // chain of 9 objects
    create_object_chain(1);  // "chain" of 1 objects
    list_objects();
    printf("\n");

    printf("One more ..\n");
    new_object();  // can not take it, trigger GC
    list_objects();
    printf("End\n");

    return 0;
}