CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := $(basename $(notdir $(wildcard samples/*.p)))
ERRORS := undeclared args const index noindex nested twice then comment \
          noproc period procvalue

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

# enkel/0 -> assembly -> program file.
%.asm: %.p enkel.py
	$(PYTHON) enkel.py $< > $@

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. Both machines pass the conformance suite of specification version 2.
# 2. Every sample prints what it should, on both machines.
# 3. 300 random expressions give the values worked out by fuzz.py.
# 4. Programs with mistakes get the right error messages.
test: vm $(SAMPLES:%=samples/%.vm)
	$(PYTHON) conform.py ./vm
	$(PYTHON) conform.py $(PYTHON) vm.py
	$(PYTHON) compare.py ./vm "$(PYTHON) vm.py" build/*.vm samples/*.vm
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	done
	$(PYTHON) fuzz.py 2 300 tests/fuzz.p tests/fuzz.expected
	$(PYTHON) enkel.py tests/fuzz.p > tests/fuzz.asm
	$(PYTHON) asm.py tests/fuzz.asm tests/fuzz.vm
	./vm tests/fuzz.vm | diff -q tests/fuzz.expected -
	for e in $(ERRORS); do \
	    ! $(PYTHON) enkel.py tests/$$e.p 2>&1 >/dev/null || echo "$$e: no error"; \
	done | diff -u tests/errors.txt -
	@echo "ch10: ok"

clean:
	rm -rf vm samples/*.asm samples/*.vm tests/*.asm tests/*.vm build __pycache__
	rm -f tests/fuzz.p tests/fuzz.expected

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
