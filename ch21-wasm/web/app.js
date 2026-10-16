// The playground: an editor, the assembler of asm.js, and the machine
// of machine.js, which is core.c compiled to WebAssembly.

import { assemble, toFile } from "./asm.js";
import { Machine, Trap } from "./machine.js";

const EXAMPLES = {
    "Fibonacci": `; The first ten Fibonacci numbers (chapter 2).
; The stack holds a b n, where n counts down to zero.

        PUSH 0          ; a
        PUSH 1          ; b
        PUSH 10         ; n
loop:   DUP
        JZ end
        PUSH 1
        SUB
        ROT
        ROT             ; n a b
        OVER
        PRINT           ; print a
        SWAP
        OVER
        ADD             ; n b (a + b)
        ROT             ; b (a + b) n
        JMP loop
end:    HALT
`,
    "Factorial, recursively": `; Each call to fact gets a frame of its own (chapter 3).
; Step through it and watch the frames pile up, and come down.

main:   PUSH 6
        CALL fact 1
        PRINT
        HALT

fact:   LOAD 0
        PUSH 2
        LT
        JZ recurse
        PUSH 1
        RET
recurse:
        LOAD 0
        LOAD 0
        PUSH 1
        SUB
        CALL fact 1
        MUL
        RET
`,
    "A linked list": `; A list of cells on the heap (chapter 13), built and summed.
; References are shown as @n: block number n.

main:   PUSH 0          ; local 0: the list
        PUSH 5          ; local 1: n
build:  LOAD 1
        JZ sum
        PUSH 2
        NEW
        DUP
        PUSH 0
        LOAD 1
        SETF            ; cell.value = n
        DUP
        PUSH 1
        LOAD 0
        SETF            ; cell.next = list
        STORE 0
        LOAD 1
        PUSH 1
        SUB
        STORE 1
        JMP build
sum:    PUSH 0          ; local 2: total
walk:   LOAD 0
        PUSH 0
        EQ
        JZ add
        LOAD 2
        PRINT
        HALT
add:    LOAD 2
        LOAD 0
        PUSH 0
        GETF
        ADD
        STORE 2
        LOAD 0
        PUSH 1
        GETF
        STORE 0
        JMP walk
`,
    "Hello, world": `; EMIT writes one character (chapter 10).

        PUSH 72
        EMIT
        PUSH 101
        EMIT
        PUSH 108
        EMIT
        PUSH 108
        EMIT
        PUSH 111
        EMIT
        PUSH 44
        EMIT
        PUSH 32
        EMIT
        PUSH 119
        EMIT
        PUSH 111
        EMIT
        PUSH 114
        EMIT
        PUSH 108
        EMIT
        PUSH 100
        EMIT
        PUSH 10
        EMIT
        HALT
`,
    "A trap": `; Dividing by zero, three calls deep: the machine stops,
; and says where (chapter 4).

main:   PUSH 3
        CALL down 1
        HALT

down:   PUSH 100
        LOAD 0
        DIV
        PRINT
        LOAD 0
        PUSH 1
        SUB
        CALL down 1
        RET
`,
};

const $ = (id) => document.getElementById(id);
const source = $("source"), listing = $("listing"), stackView = $("stack");
const output = $("output"), status = $("status");

let machine = null;
let lines = [];
let ready = false;
let running = false;

function write(c) {
    output.textContent += String.fromCharCode(c);
}

function setStatus(text, error = false) {
    status.textContent = text;
    status.className = error ? "error" : "";
}

function enable() {
    $("step").disabled = !ready || running;
    $("run").disabled = !ready || running;
    $("stop").disabled = !running;
    $("assemble").disabled = running;
}

function showListing(code) {
    listing.innerHTML = "";
    const text = source.value.split("\n");
    lines.forEach((line, k) => {
        if (line.op === null && line.labels.length === 0) return;
        const div = document.createElement("div");
        div.dataset.address = line.size > 0 ? line.address : "";
        const addr = document.createElement("span");
        addr.className = "addr";
        addr.textContent = line.size > 0 ? line.address : "";
        div.append(addr, text[k].replace(/\s*[;#].*$/, "").trimEnd() || text[k].trim());
        listing.append(div);
    });
}

function show(trapAt = null) {
    const s = machine.state();
    for (const div of listing.children) {
        const a = div.dataset.address === "" ? null : Number(div.dataset.address);
        div.classList.toggle("here", !s.halted && trapAt === null && a === s.pc);
        div.classList.toggle("trapped", trapAt !== null && a === trapAt);
        if (a === (trapAt ?? s.pc) && div.scrollIntoView) div.scrollIntoView({ block: "nearest" });
    }
    stackView.innerHTML = "";
    if (s.stack.length === 0 && s.frames.length === 0) {
        stackView.innerHTML = '<div class="empty">empty</div>';
        return;
    }
    for (let i = 0; i <= s.stack.length; i++) {
        s.frames.forEach((start, f) => {
            if (start === i) {
                const bar = document.createElement("div");
                bar.className = "frame";
                bar.textContent = `call ${f + 1}`;
                stackView.append(bar);
            }
        });
        if (i < s.stack.length) {
            const cell = document.createElement("div");
            cell.className = "cell" + (s.stack[i].startsWith("@") ? " ref" : "");
            cell.textContent = s.stack[i];
            stackView.append(cell);
        }
    }
}

function load() {
    const result = assemble(source.value);
    lines = result.lines;
    output.textContent = "";
    if (result.errors.length) {
        ready = false;
        const e = result.errors[0];
        setStatus(`line ${e.line}: ${e.message}` + (result.errors.length > 1 ? ` (and ${result.errors.length - 1} more)` : ""), true);
        listing.innerHTML = '<div class="empty">Fix the mistake, and assemble again.</div>';
        enable();
        return false;
    }
    const why = machine.load(toFile(result.code), {
        copying: $("copying").checked,
        stress: $("stress").checked,
    });
    if (why) {
        ready = false;
        setStatus(why, true);
        enable();
        return false;
    }
    ready = true;
    showListing(result.code);
    show();
    setStatus(`${result.code.length} words. Step, or run.`);
    enable();
    return true;
}

function trapped(e) {
    if (!(e instanceof Trap)) throw e;
    ready = false;
    running = false;
    setStatus(e.message, true);
    show(e.address);
    enable();
}

function step() {
    try {
        if (!machine.step()) {
            ready = false;
            setStatus("Halted.");
        }
        show();
    } catch (e) {
        trapped(e);
    }
    enable();
}

// Run in slices, so that a program that never ends does not freeze
// the page, and Stop can be pressed.
function run() {
    running = true;
    enable();
    const slice = () => {
        if (!running) return;
        try {
            for (let i = 0; i < 200000; i++) {
                if (!machine.step()) {
                    running = false;
                    ready = false;
                    setStatus("Halted.");
                    show();
                    enable();
                    return;
                }
            }
            setStatus("Running...");
            requestAnimationFrame(slice);
        } catch (e) {
            trapped(e);
        }
    };
    slice();
}

async function start() {
    const examples = $("examples");
    for (const name of Object.keys(EXAMPLES)) examples.add(new Option(name, name));
    examples.onchange = () => {
        source.value = EXAMPLES[examples.value];
        load();
    };
    source.value = EXAMPLES[examples.value];
    const bytes = await (await fetch("vm.wasm")).arrayBuffer();
    machine = await Machine.create(bytes, write);
    $("assemble").onclick = load;
    $("step").onclick = step;
    $("run").onclick = run;
    $("stop").onclick = () => { running = false; setStatus("Stopped."); show(); enable(); };
    $("copying").onchange = $("stress").onchange = load;
    load();
}

start().catch((e) => setStatus(`Could not start the machine: ${e.message}`, true));
