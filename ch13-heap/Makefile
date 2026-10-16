CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := strings lists bounds

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. Both machines pass the conformance suite of version 3, except
#    'garbage': this chapter's machines never reclaim anything, which
#    version 3 requires. Chapter 14 fixes that.
# 2. Their traces agree on every suite program and sample.
# 3. The samples print what they should (bounds.asm traps on purpose).
test: vm $(SAMPLES:%=samples/%.vm)
	$(PYTHON) conform.py --known garbage ./vm
	$(PYTHON) conform.py --known garbage $(PYTHON) vm.py
	$(PYTHON) compare.py ./vm "$(PYTHON) vm.py" build/*.vm samples/*.vm
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm 2>&1 | diff -u samples/$$s.out - || exit 1; \
	done
	@echo "ch13: ok"

clean:
	rm -rf vm samples/*.vm build __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
