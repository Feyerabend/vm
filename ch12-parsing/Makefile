CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

PARSERS := descent pratt combinators
ERRORS := operand paren two semicolon

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. 500 random expressions: all three parsers build the same trees,
#    and so the same assembly, and it prints the right values.
# 2. The sample, through each parser, prints what it should.
# 3. Each parser gives its own error messages for the same mistakes.
test: vm
	$(PYTHON) fuzz.py 3 500 tests/fuzz.expr tests/fuzz.expected
	$(PYTHON) same.py tests/fuzz.expr
	for p in $(PARSERS); do \
	    $(PYTHON) compile.py -$$p tests/fuzz.expr > tests/fuzz-$$p.asm || exit 1; \
	done
	cmp tests/fuzz-descent.asm tests/fuzz-pratt.asm
	cmp tests/fuzz-descent.asm tests/fuzz-combinators.asm
	$(PYTHON) asm.py tests/fuzz-descent.asm tests/fuzz.vm
	./vm tests/fuzz.vm | diff -q tests/fuzz.expected -
	for p in $(PARSERS); do \
	    $(PYTHON) compile.py -$$p samples/compare.expr > samples/compare.asm || exit 1; \
	    $(PYTHON) asm.py samples/compare.asm samples/compare.vm || exit 1; \
	    ./vm samples/compare.vm | diff -u samples/compare.out - || exit 1; \
	done
	for t in $(ERRORS); do for p in $(PARSERS); do \
	    echo "-$$p: $$($(PYTHON) compile.py -$$p tests/$$t.expr 2>&1 | head -1)"; \
	done; done | diff -u tests/errors.txt -
	@echo "ch12: ok"

clean:
	rm -rf vm samples/*.asm samples/*.vm tests/*.asm tests/*.vm tests/fuzz.* __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
