// The assembler of chapter 6 (asm.py), in JavaScript, so that the web
// page can turn assembly language into a program without a server.
// test-asm.mjs checks that it makes exactly the same bytes as asm.py
// for every program in the conformance suite.

export const INSTRUCTIONS = [
    [0, "HALT", []],
    [1, "PUSH", ["n"]],
    [2, "ADD", []],
    [3, "SUB", []],
    [4, "MUL", []],
    [5, "PRINT", []],
    [6, "JMP", ["addr"]],
    [7, "JZ", ["addr"]],
    [8, "DUP", []],
    [9, "DROP", []],
    [10, "SWAP", []],
    [11, "OVER", []],
    [12, "ROT", []],
    [13, "LT", []],
    [14, "EQ", []],
    [15, "LOAD", ["k"]],
    [16, "STORE", ["k"]],
    [17, "CALL", ["addr", "n"]],
    [18, "RET", []],
    [19, "DIV", []],
    [20, "MOD", []],
    [21, "AND", []],
    [22, "OR", []],
    [23, "XOR", []],
    [24, "LOADM", []],
    [25, "STOREM", []],
    [26, "EMIT", []],
    [27, "NEW", []],
    [28, "GETF", []],
    [29, "SETF", []],
    [30, "LEN", []],
    [31, "CALLI", ["n"]],
];

export const BY_NAME = new Map(INSTRUCTIONS.map(([code, name, kinds]) => [name, { code, kinds }]));
export const BY_CODE = new Map(INSTRUCTIONS.map(([code, name, kinds]) => [code, { name, kinds }]));

const LABEL = /^([A-Za-z_][A-Za-z0-9_]*):/;
const NAME = /^[A-Za-z_][A-Za-z0-9_]*$/;

// A number written in decimal, or in hex as 0x1f, as Python's int(word, 0) reads it.
function number(word) {
    if (/^[+-]?(0|[1-9][0-9]*)$/.test(word)) return Number(word);
    if (/^[+-]?0[xX][0-9a-fA-F]+$/.test(word)) {
        const negative = word.startsWith("-");
        const n = parseInt(word.replace(/^[+-]/, ""), 16);
        return negative ? -n : n;
    }
    return null;
}

function parseLine(text) {
    let rest = text.split(/[#;]/, 1)[0].trim();
    const labels = [];
    for (let m; (m = LABEL.exec(rest)); rest = rest.slice(m[0].length).trim())
        labels.push(m[1]);
    const words = rest.split(/\s+/).filter((w) => w);
    return { labels, op: words[0] ?? null, operands: words.slice(1) };
}

function size(line) {
    if (line.op === null) return 0;
    if (line.op.toLowerCase() === ".word") return 1;
    const entry = BY_NAME.get(line.op.toUpperCase());
    return entry ? 1 + entry.kinds.length : 1;
}

// Assemble source text. Returns { code, lines, errors }: the code as an
// array of numbers; for each source line, its address and how many
// words it became; and every mistake found, with its line number.
export function assemble(source) {
    const lines = source.split("\n").map(parseLine);
    const labels = new Map();
    const errors = [];
    const error = (k, message) => errors.push({ line: k + 1, message });

    let address = 0;
    lines.forEach((line, k) => {
        for (const label of line.labels) {
            if (labels.has(label)) error(k, `label '${label}' is defined twice`);
            else labels.set(label, address);
        }
        line.address = address;
        line.size = size(line);
        address += line.size;
    });

    const operand = (k, kind, word) => {
        const n = number(word);
        if ((kind === "addr" || kind === "n") && n === null && NAME.test(word)) {
            if (!labels.has(word)) { error(k, `undefined label '${word}'`); return 0; }
            return labels.get(word);
        }
        if (n === null) { error(k, `expected a number, found '${word}'`); return 0; }
        if (n < -(2 ** 31) || n >= 2 ** 31) { error(k, `number out of range: ${word}`); return 0; }
        if (kind === "k" && n < 0) error(k, `a local number cannot be negative: ${n}`);
        return n;
    };

    const code = [];
    lines.forEach((line, k) => {
        if (line.op === null) return;
        if (line.op.toLowerCase() === ".word") {
            if (line.operands.length !== 1) { error(k, ".word takes one number"); code.push(0); }
            else code.push(operand(k, "n", line.operands[0]));
            return;
        }
        const entry = BY_NAME.get(line.op.toUpperCase());
        if (!entry) { error(k, `unknown instruction '${line.op}'`); code.push(0); return; }
        const { code: op, kinds } = entry;
        if (line.operands.length !== kinds.length) {
            const s = kinds.length === 1 ? "" : "s";
            error(k, `${line.op.toUpperCase()} takes ${kinds.length} operand${s}, found ${line.operands.length}`);
            code.push(op, ...kinds.map(() => 0));
            return;
        }
        code.push(op);
        kinds.forEach((kind, i) => code.push(operand(k, kind, line.operands[i])));
    });
    if (code.length === 0 && errors.length === 0) errors.push({ line: 0, message: "no code" });
    errors.sort((a, b) => a.line - b.line);
    return { code, lines, errors };
}

// The bytes of a .vm file holding the code: the format of chapter 5.
export function toFile(code) {
    const bytes = new Uint8Array(8 + 4 * code.length);
    const view = new DataView(bytes.buffer);
    bytes.set([83, 86, 77, 1]);             // "SVM", version 1
    view.setInt32(4, code.length, true);
    code.forEach((w, i) => view.setInt32(8 + 4 * i, w, true));
    return bytes;
}
