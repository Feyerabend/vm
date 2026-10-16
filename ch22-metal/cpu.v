`timescale 1ns / 1ns

// Chapter 22: the machine as hardware.
//
// The stack machine of the specification, version 2, as a circuit
// described in Verilog: instructions 0 to 26, with memory and EMIT,
// and every trap. The heap of version 3 (NEW, GETF, SETF, LEN) and CALLI
// are not here: a garbage collector in hardware is a project of its own.
// Codes 27 and above are unknown instructions, as they were in version 2.
//
// One instruction runs on every rising edge of the clock. Everything an
// instruction needs, the words of its operands, the values on top of the
// stack, is read at once, and everything it changes is written at the
// end of the cycle, together. That is the simplest way to build it, not
// the fastest: a real processor would split each instruction into
// stages, and overlap them.
//
// The CPU talks to the world through a few signals. When an instruction
// prints, print_valid is 1 for one cycle, with the number on print_value;
// EMIT does the same with emit_valid and emit_char. When the machine
// stops, halted or trapped becomes 1 and stays so; after a trap,
// trap_reason says which one, and trap_at where.

module cpu #(
    parameter CODE_SIZE = 65536
) (
    input  wire               clock,
    input  wire               reset,
    input  wire        [31:0] code_len,
    output reg                halted,
    output reg                trapped,
    output reg          [3:0] trap_reason,
    output reg         [31:0] trap_at,
    output reg                print_valid,
    output reg  signed [31:0] print_value,
    output reg                emit_valid,
    output reg          [7:0] emit_char
);

    // The instruction codes.
    localparam HALT = 0, PUSH = 1, ADD = 2, SUB = 3, MUL = 4, PRINT = 5,
               JMP = 6, JZ = 7, DUP = 8, DROP = 9, SWAP = 10, OVER = 11,
               ROT = 12, LT = 13, EQ = 14, LOAD = 15, STORE = 16, CALL = 17,
               RET = 18, DIV = 19, MOD = 20, AND = 21, OR = 22, XOR = 23,
               LOADM = 24, STOREM = 25, EMIT = 26;

    // The reasons for a trap, numbered for trap_reason; the testbench
    // turns them back into the specification's words.
    localparam T_RUNOFF = 1, T_UNKNOWN = 2, T_OPERAND = 3, T_JUMP = 4,
               T_UNDERFLOW = 5, T_OVERFLOW = 6, T_LOCAL = 7, T_ARGS = 8,
               T_DEPTH = 9, T_RETURN = 10, T_DIVZERO = 11, T_MEMORY = 12,
               T_CHAR = 13;

    localparam STACK_SIZE = 256, FRAMES = 256, MEMORY_SIZE = 4096;

    // The machine's state: the same parts as in SPEC.md, section 2.
    reg signed [31:0] code   [0:CODE_SIZE-1];   // loaded by the testbench
    reg signed [31:0] stack  [0:STACK_SIZE-1];
    reg        [31:0] ret    [0:FRAMES-1];      // a frame: return address
    reg        [31:0] saved  [0:FRAMES-1];      //   and the caller's fp
    reg signed [31:0] memory [0:MEMORY_SIZE-1];
    reg        [31:0] pc, sp, fp, fsp;

    // What the current instruction reads: its code, its operands, and
    // the three values on top of the stack (c on top, then b, then a).
    wire signed [31:0] op   = code[pc];
    wire signed [31:0] arg1 = code[pc + 1];
    wire signed [31:0] arg2 = code[pc + 2];
    wire        [31:0] room = sp - fp;          // values in the current frame
    wire signed [31:0] c = stack[sp - 1];
    wire signed [31:0] b = stack[sp - 2];
    wire signed [31:0] a = stack[sp - 3];

    // How many words follow the opcode in the code: an instruction cut
    // off by the end of the program has "missing operand".
    wire [31:0] after = code_len - pc - 1;

    function automatic is_address(input signed [31:0] t);
        is_address = t >= 0 && t < $signed(code_len);
    endfunction

    task automatic stop(input [3:0] reason);
        begin
            trapped <= 1;
            trap_reason <= reason;
            trap_at <= pc;
        end
    endtask

    integer i;

    always @(posedge clock) begin
        print_valid <= 0;
        emit_valid <= 0;
        if (reset) begin
            pc <= 0;
            sp <= 0;
            fp <= 0;
            fsp <= 0;
            halted <= 0;
            trapped <= 0;
            trap_reason <= 0;
            for (i = 0; i < MEMORY_SIZE; i = i + 1)
                memory[i] <= 0;
        end else if (!halted && !trapped) begin
            if (pc >= code_len)
                stop(T_RUNOFF);
            else case (op)
            HALT:
                halted <= 1;
            PUSH:
                if (after < 1) stop(T_OPERAND);
                else if (sp == STACK_SIZE) stop(T_OVERFLOW);
                else begin
                    stack[sp] <= arg1;
                    sp <= sp + 1;
                    pc <= pc + 2;
                end
            ADD, SUB, MUL, AND, OR, XOR, LT, EQ, DIV, MOD:
                if (room < 2) stop(T_UNDERFLOW);
                else if ((op == DIV || op == MOD) && c == 0) stop(T_DIVZERO);
                else begin
                    case (op)
                    ADD: stack[sp - 2] <= b + c;
                    SUB: stack[sp - 2] <= b - c;
                    MUL: stack[sp - 2] <= b * c;
                    AND: stack[sp - 2] <= b & c;
                    OR:  stack[sp - 2] <= b | c;
                    XOR: stack[sp - 2] <= b ^ c;
                    LT:  stack[sp - 2] <= b < c;
                    EQ:  stack[sp - 2] <= b == c;
                    DIV: stack[sp - 2] <= b / c;
                    MOD: stack[sp - 2] <= b % c;
                    endcase
                    sp <= sp - 1;
                    pc <= pc + 1;
                end
            PRINT:
                if (room < 1) stop(T_UNDERFLOW);
                else begin
                    print_valid <= 1;
                    print_value <= c;
                    sp <= sp - 1;
                    pc <= pc + 1;
                end
            EMIT:
                if (room < 1) stop(T_UNDERFLOW);
                else if (c < 0 || c > 255) stop(T_CHAR);
                else begin
                    emit_valid <= 1;
                    emit_char <= c[7:0];
                    sp <= sp - 1;
                    pc <= pc + 1;
                end
            JMP:
                if (after < 1) stop(T_OPERAND);
                else if (!is_address(arg1)) stop(T_JUMP);
                else pc <= arg1;
            JZ:
                if (after < 1) stop(T_OPERAND);
                else if (!is_address(arg1)) stop(T_JUMP);
                else if (room < 1) stop(T_UNDERFLOW);
                else begin
                    sp <= sp - 1;
                    pc <= c == 0 ? arg1 : pc + 2;
                end
            DUP:
                if (room < 1) stop(T_UNDERFLOW);
                else if (sp == STACK_SIZE) stop(T_OVERFLOW);
                else begin
                    stack[sp] <= c;
                    sp <= sp + 1;
                    pc <= pc + 1;
                end
            DROP:
                if (room < 1) stop(T_UNDERFLOW);
                else begin
                    sp <= sp - 1;
                    pc <= pc + 1;
                end
            SWAP:
                if (room < 2) stop(T_UNDERFLOW);
                else begin
                    stack[sp - 2] <= c;
                    stack[sp - 1] <= b;
                    pc <= pc + 1;
                end
            OVER:
                if (room < 2) stop(T_UNDERFLOW);
                else if (sp == STACK_SIZE) stop(T_OVERFLOW);
                else begin
                    stack[sp] <= b;
                    sp <= sp + 1;
                    pc <= pc + 1;
                end
            ROT:                                    // a b c -> b c a
                if (room < 3) stop(T_UNDERFLOW);
                else begin
                    stack[sp - 3] <= b;
                    stack[sp - 2] <= c;
                    stack[sp - 1] <= a;
                    pc <= pc + 1;
                end
            LOAD:
                if (after < 1) stop(T_OPERAND);
                else if (arg1 < 0 || fp + arg1 >= sp) stop(T_LOCAL);
                else if (sp == STACK_SIZE) stop(T_OVERFLOW);
                else begin
                    stack[sp] <= stack[fp + arg1];
                    sp <= sp + 1;
                    pc <= pc + 2;
                end
            STORE:                                  // pops first, then checks
                if (after < 1) stop(T_OPERAND);
                else if (room < 1) stop(T_UNDERFLOW);
                else if (arg1 < 0 || fp + arg1 >= sp - 1) stop(T_LOCAL);
                else begin
                    stack[fp + arg1] <= c;
                    sp <= sp - 1;
                    pc <= pc + 2;
                end
            CALL:
                if (after < 1) stop(T_OPERAND);
                else if (!is_address(arg1)) stop(T_JUMP);
                else if (after < 2) stop(T_OPERAND);
                else if (arg2 < 0 || arg2 > room) stop(T_ARGS);
                else if (fsp == FRAMES) stop(T_DEPTH);
                else begin
                    ret[fsp] <= pc + 3;
                    saved[fsp] <= fp;
                    fsp <= fsp + 1;
                    fp <= sp - arg2;
                    pc <= arg1;
                end
            RET:
                if (fsp == 0) stop(T_RETURN);
                else if (room < 1) stop(T_UNDERFLOW);
                else begin
                    stack[fp] <= c;                 // the result, where the frame began
                    sp <= fp + 1;
                    fsp <= fsp - 1;
                    pc <= ret[fsp - 1];
                    fp <= saved[fsp - 1];
                end
            LOADM:
                if (room < 1) stop(T_UNDERFLOW);
                else if (c < 0 || c >= MEMORY_SIZE) stop(T_MEMORY);
                else begin
                    stack[sp - 1] <= memory[c];
                    pc <= pc + 1;
                end
            STOREM:                                 // a v -> ; memory[a] = v
                if (room < 2) stop(T_UNDERFLOW);
                else if (b < 0 || b >= MEMORY_SIZE) stop(T_MEMORY);
                else begin
                    memory[b] <= c;
                    sp <= sp - 2;
                    pc <= pc + 1;
                end
            default:
                stop(T_UNKNOWN);
            endcase
        end
    end

endmodule
