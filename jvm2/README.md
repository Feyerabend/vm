# Virtual Machines

## sample class again

Let's go back to a very simple Java program.

```java
public class Sample {
    public static void main(String[] args) {
        System.out.println("Hi!");
    }
}
```

Most of the parsing has been done by 'classread.py'. And if we recapitulate
the main parts from running `javap -v`:

#### 1. A summary of ingredients of the class.

```console
class Sample
  minor version: 0
  major version: 62
  flags: (0x0020) ACC_SUPER
  this_class: #21                         // Sample
  super_class: #2                         // java/lang/Object
  interfaces: 0, fields: 0, methods: 2, attributes: 1
```

#### 2. What the important 'constant pool' looks like.

```console
Constant pool:
   #1 = Methodref          #2.#3          // java/lang/Object."<init>":()V
   #2 = Class              #4             // java/lang/Object
   #3 = NameAndType        #5:#6          // "<init>":()V
   #4 = Utf8               java/lang/Object
   #5 = Utf8               <init>
   #6 = Utf8               ()V
   #7 = Fieldref           #8.#9          // java/lang/System.out:Ljava/io/PrintStream;
   #8 = Class              #10            // java/lang/System
   #9 = NameAndType        #11:#12        // out:Ljava/io/PrintStream;
  #10 = Utf8               java/lang/System
  #11 = Utf8               out
  #12 = Utf8               Ljava/io/PrintStream;
  #13 = String             #14            // Hi!
  #14 = Utf8               Hi!
  #15 = Methodref          #16.#17        // java/io/PrintStream.println:(Ljava/lang/String;)V
  #16 = Class              #18            // java/io/PrintStream
  #17 = NameAndType        #19:#20        // println:(Ljava/lang/String;)V
  #18 = Utf8               java/io/PrintStream
  #19 = Utf8               println
  #20 = Utf8               (Ljava/lang/String;)V
  #21 = Class              #22            // Sample
  #22 = Utf8               Sample
  #23 = Utf8               Code
  #24 = Utf8               LineNumberTable
  #25 = Utf8               main
  #26 = Utf8               ([Ljava/lang/String;)V
  #27 = Utf8               SourceFile
  #28 = Utf8               Sample.java
```

#### 3. The contents of he program: code.

```console
{
  Sample();
    descriptor: ()V
    flags: (0x0000)
    Code:
      stack=1, locals=1, args_size=1
         0: aload_0
         1: invokespecial #1                  // Method java/lang/Object."<init>":()V
         4: return
      LineNumberTable:
        line 1: 0

  public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: (0x0009) ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=1, args_size=1
         0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
         3: ldc           #13                 // String Hi!
         5: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
         8: return
      LineNumberTable:
        line 3: 0
        line 4: 8
}
SourceFile: "Sample.java"
```

What we first can take notice of is that the program could in principle be written as:

```java
public class Sample extends Object {
    Sample() {
        super();
    }
    public static void main(String[] args) {
        System.out.println("Hi!");
    }
}
```

That is: many things are here implicit in Java that also could be made explicit.
The constructor 'super()' is calling the super class 'Object' as an initialisation.
That is what the first code block is doing under 'Sample()' above.

We are, to begin with, more interested in what the second block of code do.

```console
  public static void main(java.lang.String[]);
    ..
    Code:
        ..
         0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
         3: ldc           #13                 // String Hi!
         5: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
         8: return
```

If we isolate the referenced parts from the constant pool, then we can split them into relevant parts.

#### a. get static
```console
   #7 = Fieldref           #8.#9          // java/lang/System.out:Ljava/io/PrintStream;
   #8 = Class              #10            // java/lang/System
   #9 = NameAndType        #11:#12        // out:Ljava/io/PrintStream;
  #10 = Utf8               java/lang/System
  #11 = Utf8               out
  #12 = Utf8               Ljava/io/PrintStream;
```

#### b. ldc
```console
  #13 = String             #14            // Hi!
```

#### c. invoke virtual
```console
  #15 = Methodref          #16.#17        // java/io/PrintStream.println:(Ljava/lang/String;)V
  #16 = Class              #18            // java/io/PrintStream
  #17 = NameAndType        #19:#20        // println:(Ljava/lang/String;)V
  #18 = Utf8               java/io/PrintStream
  #19 = Utf8               println
  #20 = Utf8               (Ljava/lang/String;)V
```

The hierachical structure of referenced (native) classes, methods and fields thus can
be illustrated as:

```
java
    io
        PrintStream
            println
    lang
        System
            out = Printstream
```

