# Virtual Machines

You might be more familiar with register-based machines, if you have
experience with assembly language on a typical PC. The assembly code
for register machines and stack machines will naturally differ. In
practice, many machines combine elements of both architectures,
allowing programs to leverage the strengths of each approach.

Later on we will only deal with stack machines for simplicity.


## assembly instructions

In the programs `regvm.c` and `regvm.py` you will see how 
simple virutal register machines work.

Registers often implies a more complex structure of the machine
and also program. Here is a description of the assembly language used:

- *MOV <reg> <val>*
   - *Description*: Moves a value into a register.
   - *Arguments*:
     - `<reg>`: The register to receive the value (e.g., `A`, `B`).
     - `<val>`: The value to be moved into the register. This can
       be an integer literal or another register name.
   - *Flags*: None.
   - *Example*: `MOV A 1` sets register `A` to `1`.

- *ADD <reg> <val>*
   - *Description*: Adds a value to the specified register.
   - *Arguments*:
     - `<reg>`: The register to which the value will be added.
     - `<val>`: The value to add. This can be an integer literal
       or another register.
   - *Flags*: `Z` (Zero Flag) and `N` (Negative Flag). The flags
     are updated based on the result of the addition.
   - *Example*: `ADD A B` adds the value in register `B` to register `A`.

- *SUB <reg> <val>*
   - *Description*: Subtracts a value from the specified register.
   - *Arguments*:
     - `<reg>`: The register from which the value will be subtracted.
     - `<val>`: The value to subtract. This can be an integer literal
       or another register.
   - *Flags*: `Z` (Zero Flag) and `N` (Negative Flag). The flags are
     updated based on the result of the subtraction.
   - *Example*: `SUB A 1` subtracts `1` from the value in register `A`.

- *MUL <reg> <val>*
   - *Description*: Multiplies the specified register by a value.
   - *Arguments*:
     - `<reg>`: The register to be multiplied.
     - `<val>`: The value to multiply by. This can be an integer literal
       or another register.
   - *Flags*: `Z` (Zero Flag) and `N` (Negative Flag). The flags are
     updated based on the result of the multiplication.
   - *Example*: `MUL A B` multiplies the value in register `A` by the
     value in register `B`.

- *CMP <reg> <val>*
   - *Description*: Compares a register value to a value.
   - *Arguments*:
     - `<reg>`: The register to compare.
     - `<val>`: The value to compare to. This can be an integer literal.
   - *Flags*: `Z` (Zero Flag). The `Z` flag is set if the register
     value equals the value being compared.
   - *Example*: `CMP B 0` sets the `Z` flag if the value in register
     `B` is `0`.

- *JMP <addr>*
   - *Description*: Unconditionally jumps to a specified address in
     the program.
   - *Arguments*:
     - `<addr>`: The address in the program to jump to.
   - *Flags*: None.
   - *Example*: `JMP 4` sets the program counter (`pc`) to `4`,
     causing the VM to execute the instruction at address `4`.

- *JZ <addr>*
   - *Description*: Conditionally jumps to a specified address if
     the zero flag (`Z`) is set.
   - *Arguments*:
     - `<addr>`: The address in the program to jump to if `Z` is `1`.
   - *Flags*: None.
   - *Example*: `JZ 8` jumps to address `8` if the `Z` flag is set.

- *PRINT <reg>*
   - *Description*: Prints the value of the specified register.
   - *Arguments*:
     - `<reg>`: The register whose value will be printed.
   - *Flags*: None.
   - *Example*: `PRINT A` prints the value in register `A`.


### factorial sample

Factorial of `5` as a sample of what the machines can do.

*START*:

1. *MOV A 1*: Register `A` with `1`. `A` will hold the result of the factorial calculation.
2. *MOV B 5*: Register `B` with `5`. `B` holds the current number to multiply.

*LOOP*:

3. *CMP B 0*: Compares the value in register `B` with `0`.
4. *JZ 7*: Jumps to `8` (`PRINT`) if `B` is `0`, ending the loop.

5. *MUL A B*: Multiplies value in register `A` with value in register `B`, and stores in register `A`.
6. *SUB B 1*: Subtracts `1` from value in register `B`.
7. *JMP 3*: Jumps back to `4` (the `CMP`) to continue the loop.

*END*:

8. *PRINT A*: Prints value in register `A`, which holds the result.
