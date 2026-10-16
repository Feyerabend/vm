# F: The Java Virtual Machine

When Java appeared in 1995, the language was only half of what was
new. The other half was the machine: Java programs compiled not to the
code of any processor, but to *bytecode* for the Java Virtual Machine,
and the same `.class` file ran on any computer that had one, even
inside a web page. The p-System (study B) had made the same promise
twenty years earlier. This time it came with the web, and it took.

It is still one of the most widely used virtual machines there is,
and many other languages, such as Kotlin, Scala and Clojure, compile
to it.

## The machine

The JVM is a stack machine, and close to ours. Here is a recursive
Fibonacci in Java, as `javac` compiled it, and the same function
written for our machine:

```
fib(I)I                              fib:    LOAD 0
     0  iload_0                              PUSH 2
     1  iconst_2                             LT
     2  if_icmpge 7                          JZ more
     5  iload_0                              LOAD 0
     6  ireturn                              RET
     7  iload_0                      more:   LOAD 0
     8  iconst_1                             PUSH 1
     9  isub                                 SUB
    10  invokestatic Fib.fib:(I)I            CALL fib 1
    13  iload_0                              LOAD 0
    14  iconst_2                             PUSH 2
    15  isub                                 SUB
    16  invokestatic Fib.fib:(I)I            CALL fib 1
    19  iadd                                 ADD
    20  ireturn                              RET
```

Almost line for line, the same: arguments as numbered local
variables, arithmetic on the stack, a call that takes its arguments
from the stack and leaves the result there.

[`jvm.py`](jvm.py) reads class files and runs them: about 450 lines,
for a subset of the JVM, which is ints, arrays of ints, static methods,
string constants and printing. Three programs in [`src/`](src) were
compiled with `javac`, and their class files are in
[`classes/`](classes). `jvm.py` prints exactly what the real JVM
prints for each, including the stack trace when `Divide` divides by
zero:

```
Exception in thread "main" java.lang.ArithmeticException: / by zero
	at Divide.share(Divide.java:4)
	at Divide.main(Divide.java:10)
```

The test checks both machines against the same expected output, the
way chapter 8 checked ours.

## Compared with ours

The differences are in what the class file carries.

**The constant pool.** Our `CALL` holds an address. The JVM's
`invokestatic` holds the number of an entry in the class's *constant
pool*, which names the class, the method and its type:
`Fib.fib:(I)I`. Nothing is an address until the program runs. A class
can then be loaded when it is first used, from a file or from the
network, and replaced by a newer version without recompiling those
that use it. The price is a lookup, which a real JVM does once, and
then remembers.

**Typed instructions.** Our `ADD` adds whatever is on the stack, and
chapter 13 had to tag every value, and check the tags while running,
to tell numbers from references. The JVM has `iadd` for ints, `ladd`
for longs, `fadd` and `dadd` for floats and doubles; and `iload` and
`aload` for ints and references. The type is in the instruction, so it
can be checked *before* the program runs.

**Verification.** That check is the JVM's verifier, which is chapter
19's verifier grown up. Before running a method, it works out what
type every stack slot and local variable has at every instruction,
and refuses the class if any instruction could get the wrong type, or
the stack could overflow or underflow. Each method in the class file
declares its `max_stack` and `max_locals` (`fib` has 3 and 1), which
chapter 19 had to compute. `jvm.py` does not verify, but it does stop
if a method's stack ever grows past its `max_stack`.

**Line numbers.** The class file keeps a table from bytecode offsets
to source lines, which is how the stack trace above can say
`Divide.java:4`. Chapter 7's traces pointed at addresses; this is the
next step, back to the source.

A real JVM, such as HotSpot, also does what Part IV did: it starts by
interpreting, counts which methods run often, and compiles those to
native code, while the program runs. Chapters 16 and 20, in one
machine.

## Run it

```
make test
python3 jvm.py classes/Fib.class
python3 jvm.py -c classes/Fib.class
```

`-c` shows the bytecode of every method, as `javap -c` does. `make
classes` compiles the sources again, with `javac`; the tests do not
need it. If `java` is installed, `make test` runs the real JVM on the
same classes too.

The archive has more: [`archive/jvm1`](../../archive/jvm1) and
[`archive/jvm2`](../../archive/jvm2) read class files in Python, and
[`archive/pitiful`](../../archive/pitiful) is PitifulVM, a small JVM in
C from National Cheng Kung University, under its own BSD licence.

## Exercises

1. Add `long`: `lconst_0`, `ladd`, `lload` and the rest. Longs take
   two local variable slots and two stack slots each. Why did the
   JVM's designers do that, and what does it cost?
2. Add objects: `new`, `invokespecial` for the constructor,
   `getfield` and `putfield`. Where does `jvm.py` find out how many
   fields an object has?
3. Write a verifier for the subset: for each instruction, the types
   on the stack before it, as chapter 19 did with depths. Then compile
   a class whose bytecode is wrong (edit the bytes) and see the real
   JVM refuse it with a `VerifyError`.
4. Add `try` and `catch`: the exception table, which `jvm.py` now
   skips, says which range of bytecode each handler covers.
