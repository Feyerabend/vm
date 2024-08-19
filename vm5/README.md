# Virtual Machines

## garbage collection

So far we have ignored in principal how memory or memory management
for the VM should or could look like. In Python the build-in
garbage collector takes care of much memory concerns. But in C
we have to check for ourselves the memory required. So far
the easiest solution is to allocate memory at the start, and
crash when ther is no left. This isn't ideal in a real scenario.
One way of handling memory in C is also to use garbage collection
at suitable places, in the program.

Memory management in a VM can involve several critical aspects.
They can including allocation, deallocation, and garbage collection.
For C this poses additional challenges, as C
does not automatically reclaim unused memory, leading to
potential memory leaks and crashes if not managed correctly.

A sample of a very simple illustration of this can be seen in
`gc.c`. The provided code snippet demonstrates a basic implementation
of a mark-and-sweep garbage collector. It manages a heap (a space
for allocatable memory) of `Object` instances, performs garbage
collection when necessary, and provides utility functions to
create and list objects. This approach can be extended and
adapted for various applications in a virtual machine, ranging
from simple memory management to complex implementations.


### memory management considerations in C

a.) *Static vs. dynamic allocation*
   - *Static*. Memory is allocated at compile-time. While this
   is straightforward, it limits flexibility and can waste memory
   if the allocation size is not well-calibrated.
   - *Dynamic*. Memory is allocated at runtime using functions
   like `malloc` and `free`. This is more flexible but requires
   careful management to avoid leaks and fragmentation.

b.) *Constraints and safety*
   - *Pre-allocated heap*. Allocating a fixed-size heap and crashing
   when it is full, as in the previously provided example, is simple
   but not ideal. It does not handle scenarios where memory demands
   fluctuate or where memory can be reclaimed dynamically.
   - *Garbage Collection (GC)*. Implementing garbage collection helps
   automatically manage memory by reclaiming unused objects, but it
   introduces overhead and some complexity.


### gc.c


   ```c
   typedef struct Object {
       int marked;  // mark flag
       struct Object* next;  // a simple linked list ..
   } Object;
   ```
   - `marked`: A flag used during garbage collection to
     indicate if the object is reachable.
   - `next`: A pointer to the next object in a linked list
     (which simulates an object reference).


   ```c
   Object* heap[MAX_OBJECTS];
   int num_objects = 0;
   ```
   - `heap`: An array of pointers to `Object` structures,
      representing the managed heap.
   - `num_objects`: The count of objects currently in the heap.


   ```c
   Object* root = NULL;
   ```
   - A pointer to an `Object` that serves as the point for
   the garbage collection process. Objects reachable from
   `root` are considered *live* (in use).


#### GC functions

Allocates a new object and triggers garbage collection,
if the heap is full:

   ```c
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
   ```

Recursively marks all reachable objects,
starting from the given `obj`:

   ```c
   void mark(Object* obj) {
       if (obj == NULL || obj->marked) return;
       obj->marked = 1;
       printf("Marking object at %p\n", (void*)obj);
       if (obj->next) {
           mark(obj->next);
       }
   }
   ```

Frees objects that are not marked as reachable
and reorganizes the heap:

   ```c
   void sweep() {
       for (int i = 0; i < num_objects; i++) {
           if (heap[i]->marked) {
               heap[i]->marked = 0;
           } else {
               printf("Sweeping object at %p\n", (void*)heap[i]);
               free(heap[i]);
               heap[i] = heap[--num_objects];
               i--; // adjust index as object get lost
           }
       }
   }
   ```

Main GC, marking and then sweeping:

   ```c
   void mark_and_sweep() {
       mark_all();
       sweep();
   }
   ```


### examples of usage

In a VM context, the provided garbage collection
implementation can be adapted to manage various
types of objects.

a.) *Objects in a programming language*
   - *Data structures*: The `Object` structure could represent objects
   like strings, arrays, or user-defined types (in a VM).
   - *Memory management*: The GC can automatically reclaim memory for
   objects that are no longer reachable, reducing the risk of memory leaks.

b.) *VM internals*
   - *Stack frames*: Objects could represent stack frames or other
   internal data structures.
   - *Instruction state*: The linked list could represent a sequence
   of instructions or state information that needs to be managed.



### gc2.c

The `gc2.c`have some slight improvements over `gc.c`.
Those are in object management thriugh the *reference counting*,
and *pools*.

Besides addition to mark-and-sweep, implementing reference
counting can help manage objects (with circular references)
more effectively.
For frequently allocated and deallocated objects of the same
size (here examplified with 10), using memory pools can reduce
fragmentation and improve performance.

Some improvements of giving *errors*, improving robustness
by handling memory allocation failures gracefully and
providing mechanisms for recovery or scaling.

Implementing some "debugging" features by printing statements
to track memory usage and identify potential leaks or performance
bottlenecks.



..

Future enhancements could involve implementing memory
pools for common object sizes and adding profiling
tools to monitor memory usage.


..
