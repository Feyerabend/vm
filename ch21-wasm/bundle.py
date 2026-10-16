#!/usr/bin/env python3
"""
Make the playground into one self-contained HTML file: the page, its
three scripts, and the WebAssembly machine, written into the page as
base64. A browser will not fetch vm.wasm for a page opened straight
from a file, so web/index.html needs a web server; the bundle does
not. It can be opened from disk, sent by mail, or put anywhere.

    usage: bundle.py web/ > playground.html
"""

import base64
import os
import re
import sys


def strip_module(text):
    """Remove import lines, and the word export: the scripts become one."""
    text = re.sub(r'^import .*?;\n', '', text, flags=re.M)
    return re.sub(r'^export ', '', text, flags=re.M)


def main():
    web = sys.argv[1]
    read = lambda name: open(os.path.join(web, name)).read()
    wasm = base64.b64encode(open(os.path.join(web, "vm.wasm"), "rb").read()).decode()
    app = read("app.js").replace(
        'const bytes = await (await fetch("vm.wasm")).arrayBuffer();',
        'const bytes = Uint8Array.from(atob(WASM), (c) => c.charCodeAt(0));')
    assert "atob(WASM)" in app
    script = "\n".join([
        f'const WASM = "{wasm}";',
        strip_module(read("asm.js")),
        strip_module(read("machine.js")),
        strip_module(app),
    ])
    page = read("index.html").replace(
        '<script type="module" src="app.js"></script>',
        f'<script type="module">\n{script}\n</script>')
    assert "app.js" not in page
    sys.stdout.write(page)


if __name__ == "__main__":
    main()
