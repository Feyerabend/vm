CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := $(basename $(notdir $(wildcard samples/*.bas)))
ERRORS := label twice fornext nextfor nextvar step then endif string endwhile

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

# basal/0 -> assembly -> program file.
%.asm: %.bas basal.py
	$(PYTHON) basal.py $< > $@

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. Every sample prints what it should.
# 2. Programs with mistakes get the right error messages.
# 3. RETURN without GOSUB compiles, and traps when it runs.
test: vm $(SAMPLES:%=samples/%.vm) tests/return.vm
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	done
	for e in $(ERRORS); do \
	    ! $(PYTHON) basal.py tests/$$e.bas 2>&1 >/dev/null || echo "$$e: no error"; \
	done | diff -u tests/errors.txt -
	! ./vm tests/return.vm > tests/return.got 2>&1
	diff -u tests/return.txt tests/return.got
	@echo "ch11: ok"

clean:
	rm -rf vm samples/*.asm samples/*.vm tests/*.asm tests/*.vm tests/*.got __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
