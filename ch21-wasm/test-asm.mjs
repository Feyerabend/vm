// Check that the JavaScript assembler makes exactly the same bytes as
// asm.py, for every program given:
//
//     node test-asm.mjs suite/*.asm

import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { assemble, toFile } from "./web/asm.js";

const dir = mkdtempSync(join(tmpdir(), "test-asm-"));
const out = join(dir, "p.vm");
let failed = 0;
for (const path of process.argv.slice(2)) {
    const { code, errors } = assemble(readFileSync(path, "utf8"));
    if (errors.length) {
        console.log(`${path}: ${errors[0].message}`);
        failed++;
        continue;
    }
    execFileSync("python3", ["asm.py", path, out]);
    const expected = readFileSync(out);
    if (Buffer.compare(Buffer.from(toFile(code)), expected) !== 0) {
        console.log(`${path}: different bytes from asm.py`);
        failed++;
    }
}
rmSync(dir, { recursive: true });
console.log(`${process.argv.length - 2 - failed} of ${process.argv.length - 2} programs assembled exactly as asm.py does`);
process.exit(failed ? 1 : 0);
