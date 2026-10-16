// The testbench: the world around the CPU, in simulation.
//
// It loads a program into the CPU's code memory, from a file of
// hexadecimal words written by vrun.py, drives the clock, and turns the
// CPU's output signals into output: a number and a newline for PRINT, a
// byte for EMIT. When the CPU stops, it writes "status 0" (halted) or the
// trap message and "status 1" to standard error, for vrun.py to read.
//
//     vvp sim +program=prog.hex +length=27 [+limit=cycles]

`timescale 1ns / 1ns

module tb;
    reg clock = 0;
    reg reset = 1;
    reg [31:0] length;
    reg [1023:0] file;
    reg [63:0] limit;
    reg [63:0] cycles = 0;

    wire halted, trapped, print_valid, emit_valid;
    wire [3:0] trap_reason;
    wire [31:0] trap_at;
    wire signed [31:0] print_value;
    wire [7:0] emit_char;

    cpu machine (
        .clock(clock), .reset(reset), .code_len(length),
        .halted(halted), .trapped(trapped), .trap_reason(trap_reason), .trap_at(trap_at),
        .print_valid(print_valid), .print_value(print_value),
        .emit_valid(emit_valid), .emit_char(emit_char)
    );

    localparam STDERR = 32'h8000_0002;

    initial begin
        if (!$value$plusargs("program=%s", file) || !$value$plusargs("length=%d", length)) begin
            $fdisplay(STDERR, "usage: vvp sim +program=prog.hex +length=n");
            $finish(0);
        end
        if (!$value$plusargs("limit=%d", limit))
            limit = 100000000;
        $readmemh(file, machine.code, 0, length - 1);
        #5 clock = 1;
        #5 clock = 0;
        reset = 0;
        forever begin
            #5 clock = 1;
            #5 clock = 0;
        end
    end

    // Output, and the end, are seen on the falling edge, after the rising
    // edge on which the CPU set them.
    always @(negedge clock) if (!reset) begin
        if (print_valid)
            $write("%0d\n", print_value);
        if (emit_valid)
            $write("%c", emit_char);
        cycles = cycles + 1;
        if (halted) begin
            $fflush;
            $fdisplay(STDERR, "cycles %0d", cycles);
            $fdisplay(STDERR, "status 0");
            $finish(0);
        end
        if (trapped) begin
            $fflush;
            case (trap_reason)
                1: $fdisplay(STDERR, "trap: ran off the end of the program at %0d", trap_at);
                2: $fdisplay(STDERR, "trap: unknown instruction at %0d", trap_at);
                3: $fdisplay(STDERR, "trap: missing operand at %0d", trap_at);
                4: $fdisplay(STDERR, "trap: jump out of program at %0d", trap_at);
                5: $fdisplay(STDERR, "trap: stack underflow at %0d", trap_at);
                6: $fdisplay(STDERR, "trap: stack overflow at %0d", trap_at);
                7: $fdisplay(STDERR, "trap: no such local at %0d", trap_at);
                8: $fdisplay(STDERR, "trap: not enough arguments at %0d", trap_at);
                9: $fdisplay(STDERR, "trap: too many nested calls at %0d", trap_at);
                10: $fdisplay(STDERR, "trap: return without call at %0d", trap_at);
                11: $fdisplay(STDERR, "trap: division by zero at %0d", trap_at);
                12: $fdisplay(STDERR, "trap: no such memory address at %0d", trap_at);
                13: $fdisplay(STDERR, "trap: not a character at %0d", trap_at);
            endcase
            $fdisplay(STDERR, "cycles %0d", cycles);
            $fdisplay(STDERR, "status 1");
            $finish(0);
        end
        if (cycles > limit) begin
            $fflush;
            $fdisplay(STDERR, "stopped after %0d cycles", limit);
            $fdisplay(STDERR, "status 3");
            $finish(0);
        end
    end
endmodule
