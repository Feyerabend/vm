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

### run

Move (or copy or reference) the class file 'Sample.class' to where the 'main.py' program is.
Test the sample.

```shell
> python3 main.py -i Sample.class
> Hi!
```

## more parsing

Most of the parsing has been done by 'classread.py'. And if we recapitulate
the main parts from running `javap -v`:

#### 1. a summary of ingredients of the class.

```console
class Sample
  minor version: 0
  major version: 62
  flags: (0x0020) ACC_SUPER
  this_class: #21                         // Sample
  super_class: #2                         // java/lang/Object
  interfaces: 0, fields: 0, methods: 2, attributes: 1
```

#### 2. what the important 'constant pool' looks like.

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

#### 3. the contents of the program: code.

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

Looking at the dependency of classes we could also write 'Sample.java' even more explicit
in the following way:

```java
public class Sample extends java.lang.Object {
    Sample() {
        super();
    }
    public static void main(java.lang.String[] args) {
        java.lang.System.out.println("Hi!");
    }
}
```

All these variations compiles to (almost) the same class files. In principal
they are the same Java program.


## interpret

### code

We are more interested in what the second block of code does above.

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

If we isolate the referenced parts from the __constant pool__, then we can split them into relevant parts.

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
  #14 = Utf8               Hi!
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

Return only returns from the calling method.

### table of some instructions[^table]

Looking at what the specification (or a simplification of specification) we get more
details of what the instructions are.

[^table]: See https://en.wikipedia.org/wiki/List_of_Java_bytecode_instructions

| Instruction     | Decimal |  Hex  |  **Binary**   |   Description |
| --------------- | ------- | ----- | ------------- | ------------- |
| `getstatic`     |   178   | b2	| **10110010** |  get a static field value of a class, where the field is identified by field reference in the constant pool index (indexbyte1 << 8 \| indexbyte2)  |
| `ldc`           |   18    | 12    | **00010010** |   push a constant #index from a constant pool (String, int, float, Class, java.lang.invoke.MethodType, java.lang.invoke.MethodHandle, or a dynamically-computed constant) onto the stack  |
| `invokevirtual` |   177   | b6    | **10110110** |  invoke virtual method on object objectref and puts the result on the stack (might be void); the method is identified by method reference index in constant pool (indexbyte1 << 8 \| indexbyte2) |

A can be deduced an interpretation of a program here is collecting items
from the pool and manipulating them in different ways. This behaviour becomes
the significant part of 'main.py'.

There are naturally other operations in Java such as aritmetic that works more
directly on and from the code itself, but not so much using the pool.


### the simplest of implementations

A Python implementation 'main.py' running *only* the simplest of Java programs (above) shows
how the principles works.[^jvmimpl]

[^jvmimpl]: I'm most grateful for the implementation given at: https://github.com/phoro3/python_jvm,
from which I have borrowed heavily.

The hierachical structure of some referenced (native) classes, methods and fields
thus can be illustrated as:

```
java
    io
        PrintStream
            println
    lang
        System
            out = PrintStream
```

This lends itself to an easier task in Python. To load a 'native' class from the structure
one could use `importlib.import_module(class_name)`. Other Python constructions of 'reflection'
of `getattr(object, name)` and dynamically calling methods helps.

Extending previous parsing of a class, the code attribute was then left untouched.

```python
    # code attr
    def get_code_of_method(self, method_name):
        codeattr = self.get_attr_of_method(method_name, 'Code')
        if codeattr:
            t = io.BytesIO(codeattr)
            max_stack = struct.unpack('!H', t.read(2))[0]
            max_locals = struct.unpack('!H', t.read(2))[0]
            code_len = struct.unpack('!I', t.read(4))[0]
            code = t.read(code_len)
            return (max_stack, max_locals, code)
        return None
```

Besides the instructions in `code` limits of local variables and the local stack comes to the aid
for implementation especially in languages where allocation/eallocation is handled manually.

The previous sequence:

```text
  Code:
    ..
    getstatic     #7
    ldc           #13   // String Hi!
    invokevirtual #15
    return
```

```text
Constant pool:
    ..
    #13 = String  #14   // Hi!
    #14 = Utf8    Hi!
```

```python
class Interpret():
    ..
        self.instructions = {
            18:     self.instr_ldc,
            177:    self.instr_return,
            178:    self.instr_getstatic,
            182:    self.instr_invokevirtual
        }
    ..
    def instr_ldc(self):
        index = self.advance()
        string_ref = self.pool[index - 1].value
        string = self.pool[string_ref - 1].value
        self.stack.append(string)

```
