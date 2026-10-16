CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := fib fact gcd primes collatz

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. Every sample, assembled, prints what it should.
# 2. Every sample, disassembled and assembled again, gives the same bytes.
# 3. A source full of mistakes gets every one of them reported.
test: vm $(SAMPLES:%=samples/%.vm)
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	    $(PYTHON) disasm.py samples/$$s.vm > samples/$$s.dis.asm || exit 1; \
	    $(PYTHON) asm.py samples/$$s.dis.asm samples/$$s.dis.vm || exit 1; \
	    cmp samples/$$s.vm samples/$$s.dis.vm || exit 1; \
	done
	$(PYTHON) asm.py tests/odd.asm tests/odd.vm
	$(PYTHON) disasm.py tests/odd.vm > tests/odd.dis.asm
	$(PYTHON) asm.py tests/odd.dis.asm tests/odd.dis.vm
	cmp tests/odd.vm tests/odd.dis.vm
	! $(PYTHON) asm.py tests/errors.asm tests/errors.vm 2> tests/errors.got
	diff -u tests/errors.txt tests/errors.got
	@echo "ch06: ok"

clean:
	rm -f vm samples/*.vm samples/*.dis.asm tests/*.vm tests/*.dis.asm tests/*.got
	rm -rf __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
