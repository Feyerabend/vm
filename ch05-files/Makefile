CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := fib fact gcd primes

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.txt tobin.py
	$(PYTHON) tobin.py $< $@

# Every sample must print what it should. Every broken file must be
# refused with exit status 2 and the right message.
test: vm $(SAMPLES:%=samples/%.vm)
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	done
	$(PYTHON) badfiles.py tests
	for f in tests/*.vm; do \
	    out=$$(./vm $$f 2>&1); st=$$?; \
	    echo "$$out"; \
	    test $$st = 2 || echo "$$f: exit status $$st"; \
	done | diff -u badfiles.txt -
	@echo "ch05: ok"

clean:
	rm -rf vm samples/*.vm tests

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
