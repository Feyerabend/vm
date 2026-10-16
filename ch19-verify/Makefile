CC ?= cc
CFLAGS ?= -std=gnu99 -O2 -Wall -Wextra
PYTHON ?= python3

BENCHMARKS := fib loop sieve enkel-sieve basal-loop

all: vm

vm: vm.c loop.h ops.h
	$(CC) $(CFLAGS) -o $@ vm.c

# For testing the verifier: sanitizers, and a limit on steps so that
# programs that never end can still be compared.
vm-fuzz: vm.c loop.h ops.h
	$(CC) -std=gnu99 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all \
	    -DSTEP_LIMIT=20000 -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

benchmarks: $(BENCHMARKS:%=bench/%.vm)

# 1. The conformance suite passes: programs that verify run without
#    the checks, the rest with them, and both behave as specified.
# 2. The verifier accepts and refuses exactly what tests/verdicts.txt
#    says, for every program in the suite.
# 3. 600 random programs, run verified and with every check on a
#    machine built with sanitizers, behave exactly the same.
# 4. The benchmarks verify, and give the right answers.
test: vm vm-fuzz benchmarks
	$(PYTHON) conform.py ./vm
	$(PYTHON) conform.py ./vm -g copy -S
	$(PYTHON) conform.py ./vm -C
	for f in suite/*.asm; do \
	    n=$$(basename $$f .asm); \
	    $(PYTHON) asm.py $$f tests/v.vm || exit 1; \
	    r=$$(./vm -V tests/v.vm 2>&1 >/dev/null | sed -n 's/.*not verified: //p'); \
	    echo "$$n: $${r:-verified}"; \
	done | diff -u tests/verdicts.txt -
	rm -rf tests/fuzz
	$(PYTHON) fuzz.py 1 600 tests/fuzz
	./fuzz.sh ./vm-fuzz tests/fuzz
	for b in $(BENCHMARKS); do \
	    ./vm -V bench/$$b.vm | diff -q bench/$$b.out - || exit 1; \
	done
	@echo "ch19: ok"

bench: vm benchmarks
	./bench.sh

clean:
	rm -rf vm vm-fuzz bench/*.vm tests/*.vm tests/fuzz build __pycache__

.PHONY: all benchmarks test bench clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
