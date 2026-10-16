CC ?= cc
CFLAGS ?= -std=gnu99 -O2 -Wall -Wextra
NATIVE_CFLAGS ?= -O2
PYTHON ?= python3

BENCHMARKS := fib loop sieve closures enkel-sieve basal-loop

# vm is chapter 19's interpreter, here to compare against.
all: vm

vm: vm.c loop.h ops.h
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

%.c: %.vm vm2c.py flow.py
	$(PYTHON) vm2c.py $< > $@

bench/%: bench/%.c runtime.h
	$(CC) $(NATIVE_CFLAGS) -w -I. $< -o $@

benchmarks: $(BENCHMARKS:%=bench/%.vm) $(BENCHMARKS:%=bench/%)

# 1. Every program in the conformance suite, compiled to native code,
#    passes: same output, same traps at the same addresses, same exit
#    status. With both collectors, and under stress.
# 2. The benchmarks, compiled, give the right answers.
test: all benchmarks
	$(PYTHON) conform.py ./vmc
	$(PYTHON) conform.py ./vmc -g copy -S
	for b in $(BENCHMARKS); do \
	    ./bench/$$b | diff -q bench/$$b.out - || exit 1; \
	    ./vm bench/$$b.vm | diff -q bench/$$b.out - || exit 1; \
	done
	@echo "ch20: ok"

bench: all benchmarks
	./bench.sh

clean:
	rm -rf vm bench/*.vm bench/*.c $(BENCHMARKS:%=bench/%) build __pycache__

.PHONY: all benchmarks test bench clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
