# Virtual Machines

*Java Virtual Machine* and/or *Java* might be the best well known implementation
of a virtual machine. I started with Java when it first came out as beta in 1995.
You could then download Java and its tools, if you adhere to it from a educational
viewpoint. I dived into Java, and wrote a simple introduction in 1997 to the language
which was printed and reprinted in a total of 16.000 copies.[^progjava] I was invited
as a journalist to JavaOne, San Fransisco, in 1999. Java was hot and exciting.
But I wasn't the only one  absorbed with the apparent future. The web was growing
quite fast, and Java promised to deliver a way to work with programs across the web
we didn't see from elsewere. Today it's quite another story, and maybe Java will
fade as things change. But that's another story ...

[^progjava]: Lonnert, Set, *Programmering i JAVA*, 1. utg., KnowWare Publ., Bromma, 1997-,
and also https://libris.kb.se/bib/2324301.
Unfortunately it is here spelled as 'JAVA' instead of the correct 'Java'.
Why, I have no idea, but it is not an abbreviation, such as 'BASIC' for instance is
Beginners' All-purpose Symbolic Instruction Code.


## preparation

First, for obvious reasons, this will not be a full or even partial
implementation of Java, or even of a proper JVM (Java Virtual Machine).
The aim here is to illustrate some aspects of the ideas that was introduced
with the JVM, and hence Java back in 1995.[^copy]

[^copy]: The prototype here will not even be called a 'JVM' because it is
trademarked/copyrighted by Sun/Oracle.
There are now adays also proper verifications routines for
these machines to guarantee (or be as secure as you can)
for a proper use.
The official machine HotSpot, now from Oracle, is highly optimized
and requires in depth learning to get aquainted with.
See e.g. https://docs.oracle.com/en/java/javase/20/vm/java-virtual-machine-guide.pdf

To amend problems with different implementations of virtual machines,
a *specification* will be helpful. On the other hand, for our purpose as
a pedagogical tool, the specification for Java is today quite intricate and
voluminous.[^javaspec] It is simply not practical to write a JVM in this
context. However, stripping the spec down to only some details for
implementation, the result might enlighten the reader/coder of how a
reasonable modern virtual machine works.

[^javaspec]: Specifications of versions of JVM: https://docs.oracle.com/javase/specs/index.html

An assumption here is that Java[^javawiki] is well known for its principals,
a virtual machine for running bytecodes, a compiler which translate for a
Java-program to a sequence of bytecodes. *Sounds familiar?* Previous samples
of virtual machines have had a string of *integers* as the minimal information
encoded and decoded between machine and compiler (or raw code). Another
similarity is the separation of language from the machine, which implies
the benefits of explicit interfaces. There can be different languages that
can run on the same machine, as there can be different implementations of
the machine adjusted for different hardwares.

The basis for Java starts with the interface between the virtual machine and
what comes out of the compiler: the `bytecode`,[^bytecodewiki] or its physical
representation in the `class file`.[^classfilewiki]

[^javawiki]: https://en.wikipedia.org/wiki/Java_(programming_language), and
https://en.wikipedia.org/wiki/Java_(software_platform).

[^bytecodewiki]: https://en.wikipedia.org/wiki/Java_bytecode
[^classfilewiki]: https://en.wikipedia.org/wiki/Java_class_file


### java and javac

Let's take a most simple example to illustrate what takes place when you use Java
in programming. The source (code) is written in simple text, here saved as a text
file 'Sample.java'.[^javaversion]

[^javaversion]: These samples have been compiled and examined with tools from
version Java 18.0.2.1.

```java
public class Sample {
    public static void main(String[] args) {
        System.out.println("Hi to you!");
    }
}
```

The sample should be rather straight forward: it prints "Hi to you!" at the prompt
when it runs. The source should be familiar with C, from which it borrows a lot.

We use tools for manipulating this by compiling it with `javac` and then
running the compiled file with `java`. In this case an interaction with
the tools might look like this:

```console
> javac Sample.java
> java Sample
Hi to you!
```

First we convert the textfile with `javac Sample.java` with the text file as
argument, to a new file. If we were to list the content of the directory after
compilation `javac`, an additional file would appear 'Sample.class' as the
result from the compilation.

Running this latter class file (without assigning the extension '.class') as
above would result in a message to the console being printed "Hi to you!".

These are the two elementary steps in building a Java program:
* compile tool `javac`,
* and the run tool `java`.


### sample class

The class file can be displayed in 'hexadecimal' and in ASCII:

![Sample bytecode](../assets/images/bytecode-sample.jpeg)

Already here is a lot of information conveyed in ASCII. We can already see that
much of the understandable source is included in the class file.
If we know about Java we can see other things such as the type of a return value,
native (library) methods called for printing, etc.

With official releases of Java there comes another tool:
* the disassembler tool `javap`.

And if we disassemble `Sample.class` with the tool `javap` with option `-c`,
we get:

```console
> javap -c Sample.class
Compiled from "Sample.java"
public class Sample {
  public Sample();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
       3: ldc           #13                 // String Hi to you!
       5: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
       8: return
}
```

### another sample

The sample 'Sample.java' above isn't however delivering much to inform us about the
byte code executable instructions that are familiar to us from previously, as they
mosly refer to invoking calls to procedures (or equivalent) in the native machine,
and also referes to other classes. (More on this below.)

We could however use another sample to illustrate how two numbers can be added.

```java
public class Add {
    public static void main(String[] args) {
        System.out.println(add(23, 45));
    }
    public static int add(int a, int b) {
        return a + b;
    }
}
```

Disassembled code:

```console
> javap -c Add.java
Compiled from "Add.java"
public class Add {
  public Add();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
       3: bipush        23
       5: bipush        45
       7: invokestatic  #13                 // Method add:(II)I
      10: invokevirtual #19                 // Method java/io/PrintStream.println:(I)V
      13: return

  public static int add(int, int);
    Code:
       0: iload_0
       1: iload_1
       2: iadd
       3: ireturn
}
```

Especially the last part here is instructive. If we combine descriptions of
the instructions,[^instrwiki] with the above we get a familiar picture:

```text
       0: iload_0        // load an int value from local variable 0  --> 1A
       1: iload_1        // load an int value from local variable 1  --> 1B
       2: iadd           // add two ints                             --> 60
       3: ireturn        // return an integer from a method          --> AC
```

[^instrwiki]: https://en.wikipedia.org/wiki/List_of_Java_bytecode_instructions

You can find the equivalent core encoded in the class file as '1A 1B 60 AC' in
hexadecimal. The instruction 'iload_0' is '1A' and so on.


## jvm1


### reading class files

Class files are structured in a certain way to ease reading and interpreting
code. Each file starts with a "magic number" which is in hexadecimal 'CAFEBABE',
cf. the hexdump above. This is a very common way for identifying files. E.g.
PDF can start with 'PDF-1.3', where a version number follows. Or, for RTF
(Rich Text Format) there is a start with '{\rtf1' or something like this,
and then other instructions of the format for text follows. In this way a
file can even be identified without an extension to the file.

Here is a small script to show the start of a class file, and hardcoded
for reading 'Sample.class' to have it short.

```python
# reading sample Java class
# classread-sample.py

import struct

with open("Sample.class", "rb") as cf:

    # cafebabe
    magic = struct.unpack('!I', cf.read(4))
    print(f"magic: {hex(magic[0])}")

    # version
    minor, major = struct.unpack('!HH', cf.read(4))
    print(f"version: {major}.{minor}")
```

We can compare this to what we can find in the specification:[^specmagic]

[^specmagic]: https://docs.oracle.com/javase/specs/jvms/se20/html/jvms-4.html

> #### magic
> The magic item supplies the magic number identifying the class file format; it has the value 0xCAFEBABE.

> #### minor_version, major_version
> The values of the minor_version and major_version items are the minor and major version numbers of this class file. Together, a major and a minor version number determine the version of the class file format. If a class file has major version number M and minor version number m, we denote the version of its class file format as M.m. Thus, class file format versions may be ordered lexicographically, for example, 1.5 < 2.0 < 2.1.

> A Java Virtual Machine implementation can support a class file format of version v if and only if v lies in some contiguous range Mi.0 ≤ v ≤ Mj.m. The release level of the Java SE platform to which a Java Virtual Machine implementation conforms is responsible for determining the range.

Thus we can build in similar ways upon the specification for reading, storing,
and executing code.


### getting into some more detail

The file format for classes besides the above, have a large part called the
'constant pool', data fields, methods, and a list of attributes.
If we limit the sample to just a static method in a class, with a simple
multiplication operation:

```java
public class Mul {
    public static int mul(int a, int b) {
        return a * b;
    }
}
```

The disassembly might be easier to decode:

```console
> javap -v Mul.class
Classfile /Users/user/Documents/jdk/Mul.class
  Last modified 30 aug. 2023; size 236 bytes
  SHA-256 checksum 0beea4fe71e627f6d7acc6a5e49ad233b05fa35aa186a1358e1fe186d7c06900
  Compiled from "Mul.java"
public class Mul
  minor version: 0
  major version: 62
  flags: (0x0021) ACC_PUBLIC, ACC_SUPER
  this_class: #7                          // Mul
  super_class: #2                         // java/lang/Object
  interfaces: 0, fields: 0, methods: 2, attributes: 1
Constant pool:
   #1 = Methodref          #2.#3          // java/lang/Object."<init>":()V
   #2 = Class              #4             // java/lang/Object
   #3 = NameAndType        #5:#6          // "<init>":()V
   #4 = Utf8               java/lang/Object
   #5 = Utf8               <init>
   #6 = Utf8               ()V
   #7 = Class              #8             // Mul
   #8 = Utf8               Mul
   #9 = Utf8               Code
  #10 = Utf8               LineNumberTable
  #11 = Utf8               mul
  #12 = Utf8               (II)I
  #13 = Utf8               SourceFile
  #14 = Utf8               Mul.java
{
  public Mul();
    descriptor: ()V
    flags: (0x0001) ACC_PUBLIC
    Code:
      stack=1, locals=1, args_size=1
         0: aload_0
         1: invokespecial #1                  // Method java/lang/Object."<init>":()V
         4: return
      LineNumberTable:
        line 2: 0

  public static int mul(int, int);
    descriptor: (II)I
    flags: (0x0009) ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=2, args_size=2
         0: iload_0
         1: iload_1
         2: imul
         3: ireturn
      LineNumberTable:
        line 4: 0
}
SourceFile: "Mul.java"
```

Starting at the end, we will leave some text unexplained,
but under 'Code' we find the core of what the class
does: *multiplies to integers and returns the resulting integer*. We can
see that primitive types, i.e. here integers, have direct representation
in the instructions. Multiplications of integers have a special single instruction.
We also find the number of arguments as '2' which should go in the method.
Futher we can see something for the stack as '2' and also for 'locals' as '2'.
What is up with that? This could be how to deal with the arguments, store them at
the stack or set them into local registers (for the method). The primitive
types can be dealt with more directly or indirect depending on hardware,
adding not only integers, but also floats or doubles in floting point
representations. This openess or fuzziness is actually not as bad as
one might think. The specification for JVM is open to different
implementations, e.g. both as a stack and/or as registers for these local
variables/arguments. Special hardware could make use of these *conceptual
specification*, rather than having a description of a reference implementation,
for memory or speed considerations.

There is only one method in the class 'Mul', which is called 'mul'.
The disassembly shows that there are two? Well, there is a 'hidden'
constructor that can be called for the class. When a new object is
constructed, the super class `Object` is called which can be seen
by `invokedspecial`, where it is loaded a reference onto the stack 
from local variable 0.

If there is an error, it is helful to have a message where
the error occured through a line number of the source, for instance.

The 'constant pool' have some similarities to a symbol table, but it is
for the 'class'. The constant pool contains e.g. names of classes referenced,
initial values of strings/numeric constants, and other things. The class loader
must e.g. identify other referenced classes for loading, which here are explicit
names (paths) for them.

Much more information can be deduced, but we will stop at this.
