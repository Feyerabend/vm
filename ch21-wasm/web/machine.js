// The machine, compiled to WebAssembly from core.c, and the little
// JavaScript it needs around it. Used both by the web page and by
// run.mjs under Node.js.
//
// The WebAssembly module imports two functions, and this file provides
// them: host_write, for every byte the program prints, and host_trap,
// which stops the machine. A trap is turned into a JavaScript
// exception, Trap, which unwinds out of the WebAssembly code.

export class Trap extends Error {
    constructor(reason, address) {
        super(`trap: ${reason} at ${address}`);
        this.reason = reason;
        this.address = address;
    }
}

export class Machine {
    // wasmBytes: the contents of vm.wasm. write: called with each byte
    // the program prints.
    static async create(wasmBytes, write) {
        const m = new Machine();
        const imports = {
            env: {
                host_write: (c) => write(c),
                host_trap: (why, at) => { throw new Trap(m.string(why), at); },
            },
        };
        const { instance } = await WebAssembly.instantiate(wasmBytes, imports);
        m.vm = instance.exports;
        return m;
    }

    // A C string in the module's memory.
    string(address) {
        const bytes = new Uint8Array(this.vm.memory.buffer);
        let end = address;
        while (bytes[end] !== 0) end++;
        return new TextDecoder().decode(bytes.subarray(address, end));
    }

    // Load a program from the bytes of a .vm file. Returns null, or the
    // reason the file was refused, in the words of chapter 5.
    load(fileBytes, { copying = false, stress = false } = {}) {
        const size = Math.min(fileBytes.length, this.vm.vm_input_size());
        new Uint8Array(this.vm.memory.buffer, this.vm.vm_input(), size)
            .set(fileBytes.subarray(0, size));
        const why = this.vm.vm_load(size);
        if (why !== 0) return this.string(why);
        this.vm.vm_set_collector(copying ? 1 : 0, stress ? 1 : 0);
        this.vm.vm_reset();
        return null;
    }

    run() { this.vm.vm_run(); }
    step() { return this.vm.vm_step() !== 0; }

    // Everything a debugger shows: where the machine is, and the stack,
    // with the place where each frame's locals begin.
    state() {
        const v = this.vm;
        const stack = [];
        for (let i = 0; i < v.vm_sp(); i++)
            stack.push(v.vm_is_ref(i) ? `@${v.vm_value(i)}` : String(v.vm_value(i)));
        const frames = [];
        for (let f = 1; f <= v.vm_frames(); f++) frames.push(v.vm_frame_start(f));
        return { pc: v.vm_pc(), start: v.vm_start(), halted: v.vm_halted() !== 0, stack, frames };
    }

    code() {
        const out = [];
        for (let a = 0; a < this.vm.vm_code_length(); a++) out.push(this.vm.vm_code(a));
        return out;
    }
}
