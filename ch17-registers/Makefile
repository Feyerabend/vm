CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

BENCHMARKS := fib loop sieve
SAMPLES := $(basename $(notdir $(wildcard samples/*.asm)))

all: vm rvm

vm: vm.c ops.h
	$(CC) $(CFLAGS) -o $@ vm.c

rvm: rvm.c
	$(CC) $(CFLAGS) -o $@ rvm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

%.rvm: %.vm translate.py
	$(PYTHON) translate.py $< $@

%-naive.rvm: %.vm translate.py
	$(PYTHON) translate.py -naive $< $@

benchmarks: $(BENCHMARKS:%=bench/%.rvm) $(BENCHMARKS:%=bench/%-naive.rvm) $(BENCHMARKS:%=bench/%.vm)

# 1. Translator and register machine together pass the conformance
#    suite, except for what they do not do, on purpose: CALLI, which
#    the translator refuses, and garbage collection, which rvm lacks.
# 2. Real programs, compiled from enkel/0, basal/0 and assembly, give
#    the same output on both machines; so do the benchmarks.
# 3. The translation of bench/loop.asm is as expected, and a program
#    whose stack depth depends on the path is refused.
test: all benchmarks $(SAMPLES:%=samples/%.rvm)
	$(PYTHON) conform.py --known garbage,calli,trap-calli-address,trap-calli-args,trap-calli-reference ./rvm-run
	for s in $(SAMPLES); do \
	    ./vm samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	    ./rvm samples/$$s.rvm | diff -u samples/$$s.out - || exit 1; \
	done
	for b in $(BENCHMARKS); do \
	    ./rvm bench/$$b.rvm | diff -q bench/$$b.out - || exit 1; \
	    ./rvm bench/$$b-naive.rvm | diff -q bench/$$b.out - || exit 1; \
	done
	$(PYTHON) translate.py -l bench/loop.vm /dev/null | diff -u tests/loop.listing -
	$(PYTHON) asm.py tests/shared.asm tests/shared.vm
	! $(PYTHON) translate.py tests/shared.vm tests/shared.rvm 2> /dev/null
	@echo "ch17: ok"

bench: all benchmarks
	./bench.sh

clean:
	rm -rf vm rvm samples/*.vm samples/*.rvm bench/*.vm bench/*.rvm tests/*.vm tests/*.rvm build __pycache__

.PHONY: all benchmarks test bench clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
