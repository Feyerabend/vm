CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := basics
ERRORS := semicolon paren char large operand

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

# The whole pipeline: expression -> assembly -> program file.
%.asm: %.expr expr.py
	$(PYTHON) expr.py $< > $@

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. The samples print what they should.
# 2. 500 random expressions give the values worked out by fuzz.py.
# 3. Programs with mistakes get the right error messages.
# 4. Division by zero is a trap at run time, not a compile error.
test: vm $(SAMPLES:%=samples/%.vm) tests/divzero.vm
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	done
	$(PYTHON) fuzz.py 1 500 tests/fuzz.expr tests/fuzz.expected
	$(PYTHON) expr.py tests/fuzz.expr > tests/fuzz.asm
	$(PYTHON) asm.py tests/fuzz.asm tests/fuzz.vm
	./vm tests/fuzz.vm | diff -q tests/fuzz.expected -
	for e in $(ERRORS); do \
	    ! $(PYTHON) expr.py tests/$$e.expr 2>&1 >/dev/null || echo "$$e: no error"; \
	done | diff -u tests/errors.txt -
	! ./vm tests/divzero.vm > tests/divzero.got 2>&1
	diff -u tests/divzero.txt tests/divzero.got
	@echo "ch09: ok"

clean:
	rm -f vm samples/*.asm samples/*.vm tests/*.asm tests/*.vm tests/*.got
	rm -f tests/fuzz.expr tests/fuzz.expected
	rm -rf __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
