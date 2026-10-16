CC ?= cc
CFLAGS ?= -std=gnu99 -O2 -Wall -Wextra
PYTHON ?= python3

BENCHMARKS := fib loop sieve closures enkel-sieve basal-loop

all: vm-threaded vm-super

vm-threaded: vm.c ops.h
	$(CC) $(CFLAGS) -DDISPATCH=THREADED -o $@ vm.c

vm-super: vm.c ops.h super.h
	$(CC) $(CFLAGS) -DDISPATCH=THREADED -DSUPER -o $@ vm.c

%.opt.asm: %.asm opt.py flow.py
	$(PYTHON) opt.py $< > $@

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

benchmarks: $(BENCHMARKS:%=bench/%.vm) $(BENCHMARKS:%=bench/%.opt.vm)

# 1. Superinstructions change nothing: the conformance suite passes,
#    and every program in tests/super, written to trap inside a pair
#    or jump into the middle of one, behaves exactly as without them.
# 2. The optimiser changes nothing a program does, for every program
#    in the suite, the samples and the benchmarks.
# 3. The benchmarks give the right answers, every way they are run.
test: all benchmarks
	$(PYTHON) conform.py ./vm-super
	$(PYTHON) conform.py ./vm-super -g copy -S
	for t in tests/super/*.asm; do \
	    $(PYTHON) asm.py $$t tests/super/t.vm || exit 1; \
	    a=$$(./vm-threaded tests/super/t.vm 2>&1; echo $$?); \
	    s=$$(./vm-super tests/super/t.vm 2>&1; echo $$?); \
	    test "$$a" = "$$s" || { echo "$$t differs"; exit 1; }; \
	done
	./same.sh suite/*.asm samples/*.asm tests/super/*.asm \
	    $(BENCHMARKS:%=bench/%.asm)
	for b in $(BENCHMARKS); do for v in vm-threaded vm-super; do \
	    ./$$v bench/$$b.vm | diff -q bench/$$b.out - || exit 1; \
	    ./$$v bench/$$b.opt.vm | diff -q bench/$$b.out - || exit 1; \
	done; done
	@echo "ch18: ok"

measure: all benchmarks
	./measure.sh

clean:
	rm -rf vm-threaded vm-super bench/*.vm bench/*.opt.asm tests/super/*.vm build __pycache__

.PHONY: all benchmarks test measure clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
