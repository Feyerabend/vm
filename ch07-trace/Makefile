CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := fib fact gcd primes collatz

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# Each check runs something and compares what it printed with a file
# of what it should print. 'make expected' rewrites those files from
# the current output; use it only after checking that output by hand.
CHECKS := tests/gcd.trace tests/gcd.debug.out tests/gcd.replay.out \
          tests/divzero.debug.out

tests/gcd.trace.got: vm samples/gcd.vm
	./vm -t samples/gcd.vm 2> $@ > /dev/null

tests/gcd.debug.out.got: vm samples/gcd.vm tests/gcd.debug
	./vm -d samples/gcd.vm < tests/gcd.debug > $@

tests/gcd.replay.out.got: tests/gcd.trace.got replay.py tests/gcd.replay
	$(PYTHON) replay.py tests/gcd.trace.got < tests/gcd.replay > $@

tests/divzero.debug.out.got: vm tests/divzero.vm tests/divzero.debug
	! ./vm -d tests/divzero.vm < tests/divzero.debug > $@ 2>&1

test: vm $(SAMPLES:%=samples/%.vm) $(CHECKS:%=%.got)
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	    ./vm -t samples/$$s.vm 2> /dev/null | diff -u samples/$$s.out - || exit 1; \
	done
	for c in $(CHECKS); do diff -u $$c $$c.got || exit 1; done
	@echo "ch07: ok"

expected: $(CHECKS:%=%.got)
	for c in $(CHECKS); do cp $$c.got $$c; done

clean:
	rm -f vm samples/*.vm tests/*.vm tests/*.got
	rm -rf __pycache__

.PHONY: test expected clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
