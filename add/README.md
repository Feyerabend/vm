
# Virtual Machines


So far, we’ve explored the primitives in our virtual machines
as abstract operations, implemented using programming languages
like Python, C, or JavaScript. Now, let’s take a deeper dive into
what happens under the hood when, for instance, we add two numbers
like 170 and 108. We’ll explore what this operation fundamentally
entails at the hardware level. Additionally, we’ll examine the
higher-level abstraction of what it means to add two numbers in
the broader context of computing and computers.

First, we delve into the basics by manually adding binary numbers,
aided by a C program that demonstrates how binary addition works.
This is followed by an implementation in Verilog, showing how you
could theoretically program an ASIC or FPGA to perform addition
directly in hardware.

Next, we shift towards a more abstract level. Two implementations,
modeled as virtual machines, illustrate how addition is carried out
using lambda calculus. While this approach might not be optimal
for the most common computers, it offers valuable insights into
functional programming concepts, which can be useful when working
with virtual machines.


## adding numbers by hand

This material should be familiar to readers with a basic
understanding of computer science, including binary numbers,
addition, and programming concepts. However, as a foundation
for discussing hardware abstraction, we'll start with an
example of adding two small integers.

Adding two 8-bit binary integers is analogous to adding
decimal numbers by hand, but it follows the rules o
 *binary arithmetic*.

Each 8-bit binary number consists of 8 digits (bits), each
of which can be either 0 or 1. For example, the binary
number `01101100` represents the decimal number 108,
and `10101010` represents the decimal number 170.

The addition process begins with the rightmost bit, known as
the 'least significant bit' (LSB), and moves towards the leftmost
bit, the 'most significant bit' (MSB). For each pair of
corresponding bits in the two numbers, you add them together,
including any carry from the previous bit's addition.

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
No carry from the last (7th) bit, so *no overflow*.
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

If you consider the carry and extend the result to accommodate
this:

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

- *Logic gates*
   - Functions for basic logic gates (`not`, `and`, `or`, and `xor`) 
     are defined using bitwise operations.
   - These functions mimic the behavior of physical logic gates in
     digital circuits.

- *Full adder*
   - This function takes three inputs: two bits (`x`, `y`) and a
     carry bit from the previous lower bit (`carry`).
   - It computes the sum (`s`) and carry (`c`) for these bits.
   - The sum is calculated using XOR operations, and the carry is
     determined by OR-ing the results of specific AND operations.
     This mimics the logic of a *full adder* in digital circuits.

- *Addition of two 8-bit numbers*
   - The `add` function calls the `adder` function for each bit of
     the two 8-bit integers, starting from the least significant bit
     (LSB) to the most significant bit (MSB).
   - The carry from each bit's addition is passed to the next higher
     bit's addition.
   - The function prints out the carry after each bit and the final
     sum in binary and decimal formats.

- *Extra*
   - `printbin`: Prints the binary representation of an 8-bit number.
   - `printcarry`: Displays the carry bits after each bit addition.
   - `printsum`: Shows the final sum in binary and checks for overflow.
   - `printadder`: 'Debugging' function that prints the result of a 
      single bit addition using the full adder.

- *Testing*
   - The `test` function demonstrates the functionality of the logic
     gates and the full adder by printing results for various input
     combinations.



### a von Neumann architecture

In the context of a *von Neumann architecture*, this program operates by
executing instructions sequentially, which are stored along with data in
the same memory. Here's how the program's operation fits within this
architecture:

1. *fetch and decode*
   - The CPU fetches the instructions for the logic gates, the *full adder*,
     and the addition operations from memory.
   - It decodes these instructions to determine the operations to perform
     (e.g., bitwise operations, function calls).

2. *execution*
   - The CPU executes the instructions step by step.
   - For each bit of the integers being added, the CPU calls the `adder`
     function, computes the sum and carry, and stores the results.

3. *memory*
   - The integers to be added (`i` and `j`) and the intermediate results
     (e.g., carries) are stored in memory.
   - The final sum and any overflows are printed out, with the output
     likely written to memory before being displayed.

4. *data path (bus)*
   - The arithmetic operations (e.g., bitwise AND, OR, XOR) are carried
     out in the ALU (Arithmetic Logic Unit) of the CPU.
   - Data (the bits of the numbers being added) is passed between the
     ALU and memory as the addition proceeds.

5. *control*
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
- *synthesis*: When synthesized onto an FPGA[^fpga] or ASIC[^asic], this
  Verilog code describes how the hardware should be configured to perform
  the addition.

[^fpga]: https://en.wikipedia.org/wiki/Field-programmable_gate_array
[^asic]: https://en.wikipedia.org/wiki/Application-specific_integrated_circuit


### testing

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



## lambda calculus and functional programming

In our vertical quest deep into the machine but also high up into the
abstrations, we will have a look at how what is called 'lambda calculus'[^calculus]
can be represented in this case: Python. THe lambda calculus is often
considered an abstract (and mathematical) basis for functional programming.

[^calculus]: https://en.wikipedia.org/wiki/Lambda_calculus


### first lambda vm, and lambda calculus

The provided code `lambda1.py` consists of two primary components:
a *compiler* that converts lambda calculus expressions into a simplified
assembly language and a *virtual machine* that interprets and executes
this assembly code. The assembly language is specifically designed to
model the computational behavior of lambda calculus.


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
  that will store the variable bindings. In this case there is no environment
  to store `{}`.
 
```python
    return [('CLOSURE', body_code, {})]
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
and manipulating functions. We limit ourselves here to some aspects
of the calculus.

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
   - *In general*, the Church numeral for `n` is `λf. λx. f (f ( .. (f x) .. ))`
     where `f` is applied `n` times.

A Church numeral $n$ is a function defined as:
$n = \lambda f. \lambda x. f^n x$ where $f^n x$
denotes the function $f$ applied $n$ times to
the argument $x$.

We can illustrate the substitution with an example:
- Suppose you have a function `λx. x + 2`. Here:
- `x` is the parameter.
- `x + 2` is the expression E.
- Now, apply this function to the argument of `5`:
- The function application is `(λx. x + 2) 5`.
- Substitution: According to the substitution principle,
  you replace `x` in the expression `x + 2` with `5`:
- `x + 2` becomes `5 + 2`.
- The result of the application is `7`.

To give an example how to add two Church numerals, you can define
a lambda expression that takes two Church numerals and returns
their sum.

As we have seen `0` is represented as `λf.λx.x`, or in general
`n` is represented as `λf.λx.f (f (...(f x)...))` with `n`
applications of `f`.
The idea now is to combine two Church numerals by applying the
first numeral's function the second numeral's number of times.

Given two Church numerals `m` and `n`, their sum can be expressed as:

```lambda
    λm. λn. λf. λx. m f (n f x)
```

This can be understood as the function `m f` applies `f` `m` times.
The function `n f x` applies `f` to `x` `n` times. Then `m f` applies
`f` `m` times to the result of `n f x`, thus adding the two numbers.

We will later see a bit of cheating as we use the built-in
lambda in Python.

```python
    def add_church(m, n):
        return lambda f: lambda x: m(f)(n(f)(x))
```

But let's see how adding works with `1` and `2`:

- `1` is `λf.λx.f x`
- `2` is `λf.λx.f (f x)`

To add `1` and `2`:

```lambda
    (λm. λn. λf. λx. m f (n f x)) (λf.λx.f x) (λf.λx.f (f x))
```

Substituting `m` with `1` and `n` with `2`:

```lambda
    λf.λx. (λf.λx.f x) f ((λf.λx.f (f x)) f x)
```

Simplifying further:

- Apply `(λf.λx.f (f x))` to `f` and `x`: `f (f x)`.
- Then, apply `λf.λx.f x` to `f (f x)`: `f (f (f x))`.

The result is `λf.λx.f (f (f x))`, which is the Church numeral for `3`.

As can be deduced from this exploration of lambda calculus, building
a computer based on the von Neumann architecture with similar abstractions
of numerals might be somewhat impractical or overly complex. However,
becoming familiar with functional thinking through lambda calculus and
implementing it in programs can be highly beneficial. This knowledge
can enhance your understanding when working with virtual machines that
incorporate concepts from functional programming.


### a second lambda vm

The code in `lambda2.py` implements a virtual machine that supports
lambda calculus with Church numerals and basic arithmetic operations.
It uses a stack-based execution model where instructions manipulate
the stack and environment to evaluate expressions. The `compile_expr`
function translates lambda calculus expressions into a sequence of
instructions that the VM can execute, allowing computations
like Church numeral addition.

   - `PUSH`: This instruction pushes a value onto the stack.
      If the value is a number, it’s converted to a
      *Church numeral* representation.

```python
    if opcode == 'PUSH':
        value = parts[1]
        if value.isdigit():
            value = int(value)
            if value == 0:
                self.stack.append(lambda f: lambda x: x)
            elif value == 1:
                self.stack.append(lambda f: lambda x: f(x))
            elif value == 2:
                self.stack.append(lambda f: lambda x: f(f(x)))
            else:
                def church_numeral(n):
                    return lambda f: lambda x: f(church_numeral(n - 1)(f)(x)) if n > 0 else x
                self.stack.append(church_numeral(value))
        else:
            self.stack.append(value)
```

   - `LOAD`: This instruction loads a variable from the
      environment and pushes its value onto the stack.


```python
     elif opcode == 'LOAD':
         var = parts[1]
         if var in self.env:
             self.stack.append(self.env[var])
         else:
             raise ValueError(f"Variable '{var}' not found in environment")
```

   - `APPLY`: This instruction applies a function to an argument.
     If the function is a closure, it creates a new VM
     to run the function's body with the argument bound
     to `x`.

```python
    elif opcode == 'APPLY':
        arg = self.stack.pop()
        func = self.stack.pop()
        if isinstance(func, tuple) and func[0] == 'CLOSURE':
            func_body, closure_env = func[1], func[2]
            new_env = closure_env.copy()
            var_name = self.get_closure_arg(func_body)                        
            new_env.update(self.env)
            new_env[var_name] = arg                        
            new_vm = VirtualMachine()
            new_vm.env = new_env                        
            result = new_vm.run(func_body)
            self.stack.append(result)
        elif callable(func):
            result = func(arg)
            self.stack.append(result)
        else:
            raise ValueError("Expected a function or closure during APPLY")
```

   - `RET`: The instruction returns the top value from the
     stack as the result of the function.

```python
     elif opcode == 'RET':
         if not self.stack:
             raise IndexError("Stack is empty during RET execution")
         return self.stack.pop()
```

   - `ADD`: This instruction adds two Church numerals.
     It expects two functions on the stack, applies
     Church numeral addition, and pushes the result
     back onto the stack.

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

The compilation from expressions to instructions for the vm are rather
straitforward. An example is going from `('add', 1, 19)` to
`['PUSH 1', 'PUSH 19', 'ADD']` and running it on the vm which gives `20`
as a result.
