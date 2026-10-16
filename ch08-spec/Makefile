CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := fib fact gcd primes collatz

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. Both machines pass the conformance suite.
# 2. Both machines trace every suite program and sample identically.
# 3. Both machines run the samples correctly.
test: vm $(SAMPLES:%=samples/%.vm)
	$(PYTHON) conform.py ./vm
	$(PYTHON) conform.py $(PYTHON) vm.py
	$(PYTHON) compare.py ./vm "$(PYTHON) vm.py" build/*.vm samples/*.vm
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	    $(PYTHON) vm.py samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	done
	@echo "ch08: ok"

clean:
	rm -rf vm samples/*.vm build __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
