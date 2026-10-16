CC ?= cc
CFLAGS ?= -std=c99 -O2 -Wall -Wextra
CLANG ?= clang
PYTHON ?= python3
NODE ?= node

all: vm web/vm.wasm web/playground.html

# The machine as a command: core.c with an ordinary C host.
vm: core.c ops.h host.c
	$(CC) $(CFLAGS) -o $@ core.c host.c

# The same core, compiled to WebAssembly with no C library at all.
web/vm.wasm: core.c ops.h
	$(CLANG) --target=wasm32 -std=c99 -O2 -Wall -Wextra -nostdlib \
	    -Wl,--no-entry -o $@ core.c

# The playground as one file, with the machine inside.
web/playground.html: web/index.html web/app.js web/asm.js web/machine.js web/vm.wasm bundle.py
	$(PYTHON) bundle.py web > $@

# 1. The core, with a C host, passes the conformance suite.
# 2. The core, compiled to WebAssembly and run by Node.js, passes it.
# 3. The assembler in JavaScript makes exactly the bytes asm.py makes.
test: all
	$(PYTHON) conform.py ./vm
	$(PYTHON) conform.py ./vm -g copy -S
	$(PYTHON) conform.py $(NODE) run.mjs
	$(PYTHON) conform.py $(NODE) run.mjs -g copy -S
	$(NODE) test-asm.mjs suite/*.asm
	@echo "ch21: ok"

# Serve the playground (web/index.html needs a server, to fetch vm.wasm;
# web/playground.html does not).
serve: all
	$(PYTHON) -m http.server -d web 8000

clean:
	rm -rf vm build __pycache__

.PHONY: all test serve clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
