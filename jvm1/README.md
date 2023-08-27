# Virtual Machines

*Java Virtual Machine* and/or *Java* might be the best well known implementation
of a virtual machine. I started with Java when it first came out as beta in 1995.
You could then download Java and its tools, if you adhere to it from a educational
viewpoint. I dived into Java, and wrote a simple introduction in 1997 to the language
which was printed and reprinted in a total of 16.000 ex.[^progjava] I was invited as
a journalist to JavaOne, San Fransisco, in 1999. Java was hot and exciting.
But I wasn't the only one  absorbed with the apparent future.
The web was growing quite fast, and Java promised
to deliver a way to work with programs across the web we didn't see from elsewere.
Today it's quite another story, and maybe Java will fade as things change.
But that's another story ...

[^progjava]: Lonnert, Set, *Programmering i JAVA*, 1. utg., KnowWare Publ., Bromma, 1997-,
and also https://libris.kb.se/bib/2324301.


## jvm1

To amend problems with different implementations of virtual machines,
a *specification* would be helpful. On the other hand, for our purpose as
a pedagogical tool, the specification for Java is today quite intricate and
voluminous.[^javaspec] However, stripping some details it might enlighten
the reader/coder of how a reasonable modern virtual machine works in principal.

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

[^javawiki]: https://en.wikipedia.org/wiki/Java_(programming_language)

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

And if we disassemble `Sample.class` with the tool `javap` with option `-c`:

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
byte code instructions, as they mosly refer to invoking calls to procedures (or equivalent)
in the native machine, and also referes to other classes.

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

Especially the last part is instructive. If we combine descriptions of
the instructions,[^instrwiki] with the above we get a familiar picture:

```text
       0: iload_0        // load an int value from local variable 0
       1: iload_1        // load an int value from local variable 1
       2: iadd           // add two ints
       3: ireturn        // return an integer from a method
```

[^instrwiki]: https://en.wikipedia.org/wiki/List_of_Java_bytecode_instructions

You can find the equivalent core encoded in the class file as '1A 1B 60 AC' in
hexadecimal.
