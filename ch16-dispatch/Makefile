CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra
PYTHON ?= python3

BUILDS := vm-switch vm-goto vm-threaded
BENCHMARKS := fib loop sieve closures

all: $(BUILDS)

# The switch build is standard C99. The other two use computed goto,
# an extension of GCC and Clang.
vm-switch: vm.c ops.h
	$(CC) -std=c99 -Wpedantic $(CFLAGS) -DDISPATCH=SWITCH -o $@ vm.c

vm-goto: vm.c ops.h
	$(CC) -std=gnu99 $(CFLAGS) -DDISPATCH=GOTO -o $@ vm.c

vm-threaded: vm.c ops.h
	$(CC) -std=gnu99 $(CFLAGS) -DDISPATCH=THREADED -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

benchmarks: $(BENCHMARKS:%=bench/%.vm)

# 1. Every build passes the conformance suite, with both collectors
#    and under stress: the way of dispatching must change nothing.
# 2. Every build gets the benchmarks right.
test: all benchmarks
	for v in $(BUILDS); do \
	    $(PYTHON) conform.py ./$$v -g mark || exit 1; \
	    $(PYTHON) conform.py ./$$v -g copy -S || exit 1; \
	    for b in $(BENCHMARKS); do \
	        ./$$v bench/$$b.vm | diff -q bench/$$b.out - || exit 1; \
	    done; \
	done
	@echo "ch16: ok"

# Timing: best of three runs of each benchmark on each build.
bench: all benchmarks
	./bench.sh

clean:
	rm -rf $(BUILDS) bench/*.vm build __pycache__

.PHONY: all benchmarks test bench clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
