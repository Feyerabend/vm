# Virtual Machines

The compilation here takes place in a series of steps.
Often these kinds of steps are referred to as a "toolchain".
Such a link in the "chain" can be a program that takes in
someting from a file and leaves someting (else) as output,
which has thus been processed. There can be other tools
(not present here) such as for profiling, linking or debugging
in a *toolchain*.


## strip

First we *strip* off any comments that may have been added
with `strip.py`. These are assumed to be the same as can
be found in C/C++. (You might change this to someting
else you find better, if you alter the regular expression
to handle it.)


## enkel/0

Now from text, as we see the program, the compiler *enkel/0*
converts the progamming ideas to code in the form of assembly.

This compiler `enkel.c` and `enkel.h` processes a the language
through the following stages:

1. **Lexical Analysis**:
    - Reads the input source code and converts it into a series
    of symbols (tokens) using functions defined in `scan.h`.

2. **Syntax Analysis**:
    - Parses the sequence of tokens to build an Abstract Syntax
    Tree (AST). This tree represents the hierarchical structure
    of the source code based on the grammar rules defined for
    expressions, terms, conditions, statements, and blocks.
    - Handles various constructs such as constants, arrays,
    variables, procedures, and control structures
    (e.g., if-else, while, do-while).

3. **Semantic Analysis and Symbol Management**:
    - Manages symbol tables for global and local scopes.
    - Checks for semantic errors such as undeclared variables
    or type mismatches.
    - Supports verbose output for debugging purposes.

4. **Code Generation**:
    - Translates the AST into a target assembly-like language.
    - Supports operations like addition, subtraction, multiplication,
    division, logical operations, and various control flow constructs.
    - Emits instructions for procedure calls, parameter handling,
    and variable storage.

5. **Output Handling**:
    - Manages input and output files specified via command-line options.
    - Provides options for verbose output and symbol table printing.

6. **Error Handling**:
    - Implements error reporting and recovery mechanisms for syntax
    and semantic errors encountered during compilation.

## scan

When compiling we need something to select the "words" in
the program (programming language). Here is where the "scanner" or
"tokenizer" comes in.

The code provided is a part of a compiler's lexical analyzer,
responsible for reading the input source code and converting
it into a series of symbols (tokens) which are used in later
stages of the compiler. Here's a simplified breakdown:

1. **Headers and Macros**:
    - The code includes necessary header files for standard I/O,
    string operations, and character type checking.
    - It defines `TRUE` and `FALSE` for boolean values and declares
    a buffer `buf` to store tokens.

2. **Global Variables**:
    - `buf`: A character array used to store the current token being read.
    - `input`: A file pointer to the source code file being analyzed.

3. **Helper Functions**:
    - `maxbuf()`: Prints an error message if a token exceeds the maximum allowed length.
    - `setinput(FILE* inputfile)`: Sets the `input` file pointer to the provided input file.
    - `advance()`: Reads the next character from the input file.

4. **Main Function (`scan()`)**:
    - `scan()` is the main function that performs lexical analysis and
    returns the next token from the input source code.
    - It skips any whitespace characters and then determines the type
    of token based on the first non-whitespace character.

5. **Token Types**:
    - **Identifiers and Keywords**: 
        - If the first character is a letter, it continues to read
        letters, digits, or underscores to form a complete word.
        - It then checks if the word matches any reserved keywords
        (e.g., "procedure", "var") and returns the corresponding token.
        If not, it returns `IDENT` for an identifier.
    - **Numbers**: 
        - If the first character is a digit, it continues to read digits
        to form a complete number and returns `NUMBER`.
    - **Comparison Operators**: 
        - Handles operators like `<`, `<=`, `>`, `>=`.
    - **Single Character Tokens**: 
        - Handles single character tokens such as `+`, `-`, `*`, `/`, `=`, `(`, `)`, etc.

6. **Error Handling**:
    - If a token exceeds the maximum buffer length, it prints an error and exits.
    - If an unrecognized token is encountered, it prints an error.

### steps

1. **Setup and Initialization**:
    - Includes necessary headers and defines constants and global variables.

2. **Reading Input**:
    - Reads characters from the input file one at a time, skipping whitespace.

3. **Token Formation**:
    - Depending on the first non-whitespace character, it forms a token:
        - **Words**: Forms identifiers or keywords.
        - **Numbers**: Forms numeric tokens.
        - **Operators and Symbols**: Recognizes various operators and punctuation marks.

4. **Returning Tokens**:
    - Returns the appropriate token for further processing by the compiler.

5. **Handling Errors**:
    - Reports and handles errors such as buffer overflow or unrecognized tokens.

## symbol

As we are more used to remembering names or at least it is
easier to connect parts in the program.

This code handles various operations related to symbol
management in a compiler, such as packing/unpacking numbers,
creating labels, managing symbol nodes (snode) in lists, and
handling global and local variables.
Here's a simplified breakdown:

1. **Headers and Macros**:
    - Includes necessary header files and custom headers for
    error handling and symbol definitions.
    - Defines constants like `LABEL_MAX` and a boolean `TRUE`.

2. **Error Handling**:
    - `printerr(char *str1, char *str2)`: Prints an error message.

3. **Packing and Unpacking Numbers**:
    - Functions to pack two 16-bit integers into a 32-bit integer and unpack them back.
    - `unpacka(int32_t x)`: Extracts the high-order 16 bits.
    - `unpackb(int32_t x)`: Extracts the low-order 16 bits.
    - `pack(int16_t a, int16_t b)`: Packs two 16-bit integers into a 32-bit integer.
    - `packint(int a, int b)`: Packs two integers into one 32-bit integer.

4. **Label Management**:
    - Manages labels used for calls and jumps in the form of strings like "C0001" or "L0001".
    - Functions to create, manage, and return labels:
        - `labelincrease()`, `labelnumber()`, `createconnect()`, `createlabel()`, `label()`, `newlabel()`, etc.
    - Functions to unpack labels from packed integers:
        - `labela()`, `labelb()`.

5. **Array Offset Management**:
    - `nextoffset(int length)`: Manages offsets for arrays in a virtual machine.

6. **Symbol Node (snode) Management**:
    - `snode` structure represents a node in a linked list.
    - Functions to allocate, push, pop, search, and delete `snode` structures.
    - `allocatesnode()`: Allocates memory for a new `snode`.
    - `push()`, `pop()`: Add and remove nodes from the list.
    - `searchid()`, `searchidlevel()`: Search for nodes by identifier and level.

7. **Connection Management**:
    - Functions to manage connections between calls and procedures.
    - `setconnectnumber()`, `connectexistnumber()`, `getconnectnumber()`.

8. **Current Procedure Identifier Management**:
    - Functions to manage the current procedure identifier used for local variables.
    - `pushcurrent()`, `popcurrent()`, `peekcurrent()`.

9. **Global Variable Management**:
    - Functions to manage global variables.
    - `newglobal()`, `globalexist()`, `getglobal()`, `setglobal()`, `initrval()`.

10. **Local Variable Management**:
    - Functions to manage local variables and parameters.
    - `newlocal()`, `resetlocal()`, `getlocal()`, `setlocal()`, `localexist()`.

11. **General Routines**:
    - Functions to delete `snode` lists and perform debug operations.
    - `dsnode()`, `destroysymbols()`.
    - Debug functions: `printsnode()`, `psnode()`, `printglobal()`, `printlocal()`.

### steps

1. **Setup and Initialization**:
    - Includes necessary headers and defines constants and global variables.

2. **Error Handling**:
    - Provides a function to print error messages.

3. **Packing and Unpacking Numbers**:
    - Provides functions to handle packing and unpacking of integers for
    efficient storage and retrieval.

4. **Label Management**:
    - Handles creation, management, and retrieval of labels used for identifying
    code segments (calls and jumps).

5. **Array Offset Management**:
    - Manages offsets for arrays to ensure proper memory allocation in a virtual
    machine environment.

6. **Symbol Node (snode) Management**:
    - Manages nodes in a linked list to keep track of various symbols and their attributes.

7. **Connection Management**:
    - Manages connections between different parts of the code, especially calls and procedures.

8. **Current Procedure Identifier Management**:
    - Keeps track of the current procedure's identifier to differentiate local variables.

9. **Global Variable Management**:
    - Manages global variables, ensuring their unique identification and proper memory allocation.

10. **Local Variable Management**:
    - Manages local variables and parameters within procedures, ensuring proper scope and memory allocation.

11. **General Routines**:
    - Provides functions to delete symbol nodes and perform debugging operations to visualize the symbol lists.


## error

A separate handling of errors does not too much clutter the compiler.

This code handles error reporting and symbol printing for a hypothetical
compiler or interpreter. It includes functions for mapping error codes
to error messages, printing error messages, and printing recognized symbols.

#### `errorstring(int ERROR)`

- **Purpose**: Returns a string representation of an error code.
- **Parameters**: `int ERROR` - The error code.
- **Returns**: `char*` - A string describing the error.

#### `errnum(int error)`

- **Purpose**: Prints the error message to `stderr`.
- **Parameters**: `int error` - The error code.
- **Behavior**: Uses `errorstring()` to get the error message and prints
it along with the error code.

#### `printsymb(Symbol s)`

- **Purpose**: Prints a human-readable representation of a symbol.
- **Parameters**: `Symbol s` - The symbol to print.
- **Behavior**: Uses a `switch` statement to match the symbol and prints
its string representation.

#### `printsymbol(int s)`

- **Purpose**: Prints a symbol.
- **Parameters**: `int s` - The symbol to print.
- **Behavior**: Casts the integer to `Symbol` type and calls `printsymb()`.



## asm

The assembler/assembly follows previous examples as an abstraction layer
from the machine code. We can handle several optimizations here or
immediately before by adding a filtering program in the chain.
Another place is in the compiler, through the AST.

The assembler follows the usual way of handling compiling, where
it is sliced from programming language, to assembly, to machine
language.
