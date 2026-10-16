// Run a .vm file on the WebAssembly machine, under Node.js, as a
// command like the other machines, so that the conformance suite can
// test it:
//
//     node run.mjs [-g mark | -g copy] [-S] program.vm

import { readFileSync, writeSync } from "node:fs";
import { Machine, Trap } from "./web/machine.js";

const args = process.argv.slice(2);
const path = args.pop();
const copying = args.includes("copy");
const stress = args.includes("-S");

let out = [];
const flush = () => {
    if (out.length) writeSync(1, Buffer.from(out));
    out = [];
};

const wasm = readFileSync(new URL("./web/vm.wasm", import.meta.url));
const machine = await Machine.create(wasm, (c) => {
    out.push(c);
    if (out.length >= 4096) flush();
});

let file;
try {
    file = readFileSync(path);
} catch {
    writeSync(2, `${path}: cannot open\n`);
    process.exit(2);
}
const why = machine.load(new Uint8Array(file), { copying, stress });
if (why !== null) {
    writeSync(2, `${path}: ${why}\n`);
    process.exit(2);
}
try {
    machine.run();
} catch (e) {
    if (!(e instanceof Trap)) throw e;
    flush();
    writeSync(2, e.message + "\n");
    process.exit(1);
}
flush();
