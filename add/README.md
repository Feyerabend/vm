
# Virtual Machines


So far, we’ve explored the primitives in our virtual machines
as abstract operations, implemented using programming languages
like Python, C, or JavaScript. Now, let’s take a deeper dive into
what happens under the hood when, for instance, we add two numbers
like 170 and 108. We’ll explore what this operation fundamentally
entails at the hardware level. Additionally, we’ll examine the
higher-level abstraction of what it means to add two numbers in
the broader context of computing and how computers.


## adding numbers by hand

Much of this should be elementary to the reader as assumed
familiar with basic computer science, or already have
some knowledge of binary numbers, adding, programming,
or programming languages. But as a background for
hardware abstraction, we start with as at first, with
an example of adding two numbers, two (small) integers.
Adding two 8-bit binary integers is similar to the way you
would add two decimal numbers by hand. But they follow
a slightly different set of rules for *binary arithmetic*.

Each 8-bit binary number is made up of 8 digits (bits),
where each bit can be either 0 or 1. Say for instance,
the binary number `01100101` is an 8-bit number that
represents the decimal number 101. Another 8-bit number
is `10101010` that is 170 in decimal.

You add the numbers starting from the rightmost bit
what is also called 'least significant bit' (LSB).
Then move to the leftmost bit, the most significant bit
(MSB). For each pair of corresponding bits in the two
numbers, you add them together along with any carry from
the previous bit's addition.

The binary addition rules are:
- `0 + 0 = 0` (sum = 0, no carry)
- `0 + 1 = 1` (sum = 1, no carry)
- `1 + 0 = 1` (sum = 1, no carry)
- `1 + 1 = 10` (sum = 0, carry = 1)
- If both bits are 1, the sum is 0, and you carry over
a 1 to the next higher bit.

But what is the 'carry'? The carry is similar to what
happens when adding in decimal when a column adds up to
10 or more, when you do it by hand. If a *bit addition*
results in a carry (like `1 + 1`), this carry is then
added to the next column (bit) on the left.
Thus if you add two 1s and have a carry from the previous
bit, you do: `1 + 1 + 1 = 11` (sum = 1, carry = 1).
Read it (alound) as 'one plus one plus one is one-one',
so you don't easily confuse it with decimal numbers.


### adding two 8-bit binary numbers

First let's take an example where adding two 8-bit binary
numbers results in a sum that does *not overflow*, meaning
the result can still be represented within 8 bits (one byte).

Add 34 and 19. First, in 8-bit binary:

- 34 in binary (8-bit) is `00100010`.
- 19 in binary (8-bit) is `00010011`.

Let's add these two binary numbers:

```
   00100010   (34 in decimal)
+  00010011   (19 in decimal)
-----------
```

1. *bit 0*: `0 + 1 = 1`             (sum = 1, carry = 0)
2. *bit 1*: `1 + 1 = 10`            (sum = 0, carry = 1)
3. *bit 2*: `0 + 0 + 1 (carry) = 1` (sum = 1, carry = 0)
4. *bit 3*: `0 + 1 = 1`             (sum = 1, carry = 0)
5. *bit 4*: `0 + 0 = 0`             (sum = 0, carry = 0)
6. *bit 5*: `1 + 0 = 1`             (sum = 1, carry = 0)
7. *bit 6*: `0 + 0 = 0`             (sum = 0, carry = 0)
8. *bit 7*: `0 + 0 = 0`             (sum = 0, carry = 0)

Adding these up:

```
   00100010   (34 in decimal)
+  00010011   (19 in decimal)
-----------
   00110101   (53 in decimal)
```

Thus `00110101`, is the 8-bit binary of the number 53.
No carry from the last (7th) bit, so no overflow.
The sum fits perfectly within 8 bits (or a byte), and the
final binary result `00110101` correctly represents 53 in
decimal. Since the sum is within the 8-bit range (0 to 255),
there is no overflow.


### overflow when adding

Let's add two 8-bit numbers `10101010` 170 in decimal,
and `01101100` 108 in decimal.

```
   10101010   (170 in decimal)
+  01101100   (108 in decimal)
-----------
```

1. *bit 0*: `0 + 0 = 0` (sum = 0, carry = 0)
2. *bit 1*: `1 + 0 = 1` (sum = 1, carry = 0)
3. *bit 2*: `0 + 1 = 1` (sum = 1, carry = 0)
4. *bit 3*: `1 + 1 = 10` (sum = 0, carry = 1)
5. *bit 4*: `0 + 1 + 1 (carry) = 10` (sum = 0, carry = 1)
6. *bit 5*: `1 + 0 + 1 (carry) = 10` (sum = 0, carry = 1)
7. *bit 6*: `0 + 1 + 1 (carry) = 10` (sum = 0, carry = 1)
8. *bit 7*: `1 + 0 + 1 (carry) = 10` (sum = 0, carry = 1)

This gives us:

```
   10101010
+  01101100
-----------
   00010110 (sum) and a carry of 1 to the next bit
```

Because this is an 8-bit addition, the final carry out
of the most significant bit (MSB) must be accounted for.
This carry indicates that the result is larger than what
can be represented by 8 bits alone.

If you consider the carry and extend the result to accommodate this:

*carry out*: `1`  
*result*: `100010110` (which is in total 278 in decimal).

If you only look at the sum without regarding the carry,
it becomes 8-bit result (`00010110`) which by itself
suggests an incorrect answer if viewed as a standalone 8-bit result.
The correct full binary sum is `100010110` when you include the carry,
*278* in decimal, which is indeed the correct sum of 170 and 108.

```
   10101010
+  01101100
-----------
  100010110 (sum) and a carry of 1 to the next bit
```




### adder in C

The code of `adder.c` is a binary adder that simulates the
addition of two 8-bit integers. The core of this program
is the implementation of a *full adder* using bitwise operations.
This full adder is used repeatedly to add corresponding bits
from two binary numbers, taking into account the carry from
the previous bit's addition.

1. *Logic gates*:
   - Functions for basic logic gates (`not`, `and`, `or`, and `xor`) 
     are defined using bitwise operations.
   - These functions mimic the behavior of physical logic gates in
     digital circuits.

2. *Full adder*:
   - This function takes three inputs: two bits (`x`, `y`) and a
     carry bit from the previous lower bit (`carry`).
   - It computes the sum (`s`) and carry (`c`) for these bits.
   - The sum is calculated using XOR operations, and the carry is
     determined by OR-ing the results of specific AND operations.
     This mimics the logic of a *full adder* in digital circuits.

3. *Addition of two 8-bit numbers*:
   - The `add` function calls the `adder` function for each bit of
     the two 8-bit integers, starting from the least significant bit
     (LSB) to the most significant bit (MSB).
   - The carry from each bit's addition is passed to the next higher
     bit's addition.
   - The function prints out the carry after each bit and the final
     sum in binary and decimal formats.

4. *Extra*:
   - `printbin`: Prints the binary representation of an 8-bit number.
   - `printcarry`: Displays the carry bits after each bit addition.
   - `printsum`: Shows the final sum in binary and checks for overflow.
   - `printadder`: 'Debugging' function that prints the result of a 
      single bit addition using the full adder.

5. *Testing*:
   - The `test` function demonstrates the functionality of the logic
     gates and the full adder by printing results for various input
     combinations.



### a von Neumann architecture

In the context of a *von Neumann architecture*, this program operates by
executing instructions sequentially, which are stored along with data in
the same memory. Here's how the program's operation fits within this
architecture:

1. *fetch and decode*:
   - The CPU fetches the instructions for the logic gates, the *full adder*,
     and the addition operations from memory.
   - It decodes these instructions to determine the operations to perform
     (e.g., bitwise operations, function calls).

2. *execution*:
   - The CPU executes the instructions step by step.
   - For each bit of the integers being added, the CPU calls the `adder`
     function, computes the sum and carry, and stores the results.

3. *memory*:
   - The integers to be added (`i` and `j`) and the intermediate results
     (e.g., carries) are stored in memory.
   - The final sum and any overflows are printed out, with the output
     likely written to memory before being displayed.

4. *data path (bus)*:
   - The arithmetic operations (e.g., bitwise AND, OR, XOR) are carried
     out in the ALU (Arithmetic Logic Unit) of the CPU.
   - Data (the bits of the numbers being added) is passed between the
     ALU and memory as the addition proceeds.

5. *control*:
   - The control unit manages the sequence of operations, ensuring that
     each instruction is carried out in the correct order and that data
     flows properly between the CPU's components.


In a real-world CPU, this type of bitwise addition would typically
be handled much faster by *built-in* machine instructions like `ADD`.
However, the program simulates this process at a lower level to
demonstrate the underlying logic. The von Neumann bottleneck
(the limitation of fetching both instructions and data from the same
memory) could make such a simulation slower compared to a
hardware-level addition.


## verilog

Adding two numbers in *Verilog* (a hardware description language)
involves describing the behavior of a digital circuit that performs
the addition. Below is an example of a Verilog[^verilog] module that
implements an 8-bit binary adder, very similar to the C code:

[^verilog]: https://en.wikipedia.org/wiki/Verilog

### 8-bit adder

```verilog
module adder_8bit (
    input [7:0] a,    // 8-bit input 'a'
    input [7:0] b,    // 8-bit input 'b'
    input cin,        // carry-in (for cascading multiple adders)
    output [7:0] sum, // 8-bit sum output
    output cout       // carry-out (for overflow detection)
);
    wire [7:0] c;     // internal carry signals

    // full adder for each bit
    assign {c[0], sum[0]} = a[0] + b[0] + cin;
    assign {c[1], sum[1]} = a[1] + b[1] + c[0];
    assign {c[2], sum[2]} = a[2] + b[2] + c[1];
    assign {c[3], sum[3]} = a[3] + b[3] + c[2];
    assign {c[4], sum[4]} = a[4] + b[4] + c[3];
    assign {c[5], sum[5]} = a[5] + b[5] + c[4];
    assign {c[6], sum[6]} = a[6] + b[6] + c[5];
    assign {c[7], sum[7]} = a[7] + b[7] + c[6];
    
    // the final carry-out is the overflow bit
    assign cout = c[7];

endmodule
```

- *module*: The `module` keyword defines a module named
  `adder_8bit`, which represents an 8-bit adder circuit.
  The inputs are `a` and `b` 8-bit wide (`[7:0]`), and `cin`
  is a single-bit carry-in. The outputs are `sum` (an 8-bit sum)
  and `cout` (the carry-out bit).

- *internal carry*:
  A wire array `c` is declared to hold the internal carry signals
  between each bit addition.

- *full adder*:
  Each line of the form `assign {c[N], sum[N]} = a[N] + b[N] + c[N-1];`
  implements a full adder for the *corresponding bit*.
  The `{carry, sum}` notation represents concatenation, where the most
  significant bit of the addition result is the carry (`c[N]`), and the
  least significant bit is the sum (`sum[N]`).

- *carry-out*:
  The final carry-out `cout` is taken from the carry of the last bit
  (`c[7]`), which can be used to detect overflow.


### simulation or synthesis

- *simulation*: You can simulate this Verilog module using a tool like
  ModelSim (or Vivado) to verify that it correctly adds two 8-bit numbers.
- *synthesis*: When synthesized onto an FPGA or ASIC, this Verilog code
  describes how the hardware should be configured to perform the addition.


### test

```verilog
module testbench;
    reg [7:0] a, b;
    reg cin;
    wire [7:0] sum;
    wire cout;

    adder_8bit uut (
        .a(a),
        .b(b),
        .cin(cin),
        .sum(sum),
        .cout(cout)
    );

    initial begin
        // test case 1
        a = 8'b00000001; b = 8'b00000001; cin = 0;
        #10;  // wait for 10 time units

        // test case 2
        a = 8'b11111111; b = 8'b00000001; cin = 0;
        #10;

        // test case 3
        a = 8'b10101010; b = 8'b01010101; cin = 1;
        #10;

        $stop;
    end
endmodule
```

- *Module instantiation*: The `adder_8bit` module is
  instantiated as `uut` (Unit Under Test).
- *Stimulus*: Different values of `a`, `b`, and `cin`
  are applied, and the resulting `sum` and `cout` are observed.
- *Simulation control*: The simulation runs for a brief
  period for each test case (`#10` time units), then stops.

This Verilog code models the behavior of an 8-bit binary adder in hardware,
similar to how C code simulates it in software. Verilog describes the addition
at the level of digital circuits, allowing it to be synthesized into physical
hardware on an FPGA or ASIC.



## lambda calculus and some functional programming

In our vertical quest deep into the machine but also high up into the
abstrations, we will have a look at how what is called 'lambda calculus'[^calculus]
can be represented in this case: Python. THe lambda calculus is often
considered a abstract (and mathematical) basis for functional programming.

[^calculus]: https://en.wikipedia.org/wiki/Lambda_calculus


### 'lambda1.py' and lambda calculus

The provided code `lambda1.py` consists of two primary components:
a *compiler* that converts lambda calculus expressions into a simplified
assembly language and a *virtual machine* that interprets and executes
this assembly code. The assembly language is specifically designed to
model the computational behavior of lambda calculus, which is a foundational
concept in functional programming and theoretical computer science.


#### lambda expressions and the compilation

In lambda calculus, a lambda expression represents an *anonymous function*
(no name). For example, the expression $\(\lambda x. x\)$ defines a function
that simply returns its argument. In this code, lambda expressions are
represented as tuples in Python. The compiler (`compile_expr`) translates
these tuples into a sequence of assembly instructions that the virtual
machine can execute.

What is called an 'environment'[^env] keep tracks of variables and their values
when running the program. When the variable occurs somewhere e.g. a value
will be set, the variable binds to the value (at a certian level).
Previously we have delt with frames (arrays and stacks) to do this kind of
work.

[^env]: https://en.wikipedia.org/wiki/Variable_(computer_science)


- *abstraction*:
  The expression `('lambda', 'x', 'x')` is a lambda abstraction that
  corresponds to $\(\lambda x. x\)$. When the compiler encounters this
  expression, it generates a *closure*: a pair consisting of the compiled
  body of the lambda (in this case, `['LOAD x', 'RET']`) and an environment
  that will store the variable bindings.
 
    ```python
    return [('CLOSURE', <body_code>, {})]
    ```

- *application*:
  The expression `('apply', ('lambda', 'x', 'x'), 2)` represents the
  application of the lambda function $\(\lambda x. x\)$ to the argument
  $\(2\)$. The compiler translates this into an instruction sequence that
  pushes the closure onto the stack, then pushes the argument, and
  finally applies the function.
  
    ```python
    return compile_expr(func) + compile_expr(arg) + ['APPLY']
    ```

The virtual machine is designed to execute the compiled assembly code
by simulating a stack-based machine.

- *closure*:
  When the virtual machine encounters a closure, it pushes it onto the stack.
  The closure is later applied when the `APPLY` instruction is encountered.
  
    ```python
    self.stack.append(instr)
    ```

- *application*:
  The `APPLY` instruction pops the function closure and its argument from the
  stack, creates a new virtual machine with the closure's environment, binds
  the argument to the function's parameter (in this case only `x`), and executes
  the function body.

    ```python
    new_vm = VirtualMachine()
    new_vm.env = closure_env.copy()
    new_vm.env.update({'x': arg}) # special 'x'
    result = new_vm.run(func_body)
    ```

- *return*:
  The `RET` instruction is used to signal the end of a function's execution,
  allowing the virtual machine to return the result from the stack to the caller.
  
    ```python
    return self.stack.pop()
    ```

### lambda calculus

*Lambda calculus* (λ-calculus) is a formal system in mathematical
logic and computer science for expressing computation based on
function *abstraction* and *application*. It uses functions as its
fundamental building blocks and provides a framework for defining
and manipulating functions.

1. *Lambda Abstraction*: This is used to define anonymous functions.
In lambda calculus, a function is defined as `λx. E`, where `λx` is
the lambda symbol and `E` is the expression that uses the variable
`x`.

2. *Function Application*: This is the process of applying a function
to an argument. If you have a function `λx. E` and you apply it to
an argument `A`, you get `E[x := A]`, which means substituting `A`
for `x` in `E` (also by notation `E[A/x]`).

3. *Church Numerals*: These are a way of representing natural numbers
using lambda calculus. Each number is represented as a function that
takes a function `f` and returns another function that applies `f`
a certain number of times. For example:
   - *0* is `λf. λx. x`
   - *1* is `λf. λx. f x`
   - *2* is `λf. λx. f (f x)`

In general, the Church numeral for `n` is `λf. λx. f (f ( ... (f x) ... ))`
where `f` is applied `n` times.


#### VM

The code in `lambda2.py` implements a virtual machine that supports
lambda calculus with Church numerals and basic arithmetic operations.
It uses a stack-based execution model where instructions manipulate
the stack and environment to evaluate expressions. The `compile_expr`
function translates lambda calculus expressions into a sequence of
instructions that the VM can execute, allowing computations
like Church numeral addition.


*initialization*:

   ```python
   def __init__(self):
       self.stack = []
       self.env = {}
   ```
   - `self.stack`: A stack used to store intermediate
     values and functions during computation.
   - `self.env`: An environment for variable bindings.

*running*:

   ```python
   def run(self, instructions):
       pc = 0
       while pc < len(instructions):
           instr = instructions[pc]
           ...
           pc += 1
   ```
   - `pc` (program counter) keeps track of the
     current instruction.
   - The loop iterates over the instructions,
     executing them one by one.

*instructions*:

   - `PUSH`:
     ```python
     if opcode == 'PUSH':
         value = parts[1]
         if value.isdigit():
             value = int(value)
             ...
         self.stack.append(value)
     ```

- This instruction pushes a value onto the stack.
  If the value is a number, it’s converted to a
  *Church numeral* representation.

   - `LOAD`:
     ```python
     elif opcode == 'LOAD':
         var = parts[1]
         if var in self.env:
             self.stack.append(self.env[var])
         else:
             raise ValueError(f"Variable '{var}' not found in environment")
     ```

- This instruction loads a variable from the
  environment and pushes its value onto the stack.

   - `APPLY`:
     ```python
     elif opcode == 'APPLY':
         arg = self.stack.pop()
         func = self.stack.pop()
         if isinstance(func, tuple) and func[0] == 'CLOSURE':
             func_body, closure_env = func[1], func[2]
             new_vm = VirtualMachine()
             new_vm.env = closure_env.copy()
             new_vm.env.update({'x': arg})
             result = new_vm.run(func_body)
             self.stack.append(result)
             return result
         elif callable(func):
             result = func(arg)
             self.stack.append(result)
         else:
             raise ValueError("Expected a function or closure during APPLY")
     ```

This instruction applies a function to an argument.
If the function is a closure, it creates a new VM
to run the function's body with the argument bound
to `x`.

   - `RET`:
     ```python
     elif opcode == 'RET':
         if not self.stack:
             raise IndexError("Stack is empty during RET execution")
         return self.stack.pop()
     ```

The instruction returns the top value from the
stack as the result of the function.

   - `ADD`:
     ```python
     elif opcode == 'ADD':
         if len(self.stack) < 2:
             raise IndexError("Not enough values on the stack to perform ADD")
         b = self.stack.pop()
         a = self.stack.pop()
         if callable(a) and callable(b):
             def add_church(m, n):
                 return lambda f: lambda x: m(f)(n(f)(x))
             self.stack.append(add_church(a, b))
         else:
             raise TypeError("ADD operation expects Church numerals")
     ```
This instruction adds two Church numerals.
It expects two functions on the stack, applies
Church numeral addition, and pushes the result
back onto the stack.


#### Compile

This function converts high-level expressions
into a list of instructions for the VM:

1. *variables*:
   ```python
   if isinstance(expr, str):
       return [f'LOAD {expr}']
   ```

2. *integer literals*:
   ```python
   elif isinstance(expr, int):
       return [f'PUSH {expr}']
   ```

3. *lambda abstractions*:
   ```python
   elif isinstance(expr, tuple):
       if expr[0] == 'lambda':
           _, var, body = expr
           body_code = compile_expr(body) + ['RET']
           return [('CLOSURE', body_code, {})]
   ```

4. *function applications*:
   ```python
   elif expr[0] == 'apply':
       _, func, arg = expr
       return compile_expr(func) + compile_expr(arg) + ['APPLY']
   ```

5. *addition*:
   ```python
   elif expr[0] == 'add':
       _, num1, num2 = expr
       return compile_expr(num1) + compile_expr(num2) + ['ADD']
   ```

..
