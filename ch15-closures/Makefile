CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := closures recursion data garbage
ERRORS := undefined rec in value char
RUNTIME := callnumber printfun

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

# lambda/0 -> assembly -> program file.
%.asm: %.lam lambda.py
	$(PYTHON) lambda.py $< > $@

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. The conformance suite of version 4, on every collector and both machines.
# 2. Traces agree across collectors and machines.
# 3. The samples print what they should, with both collectors, and
#    under stress.
# 4. Mistakes are reported when compiling; type errors trap when running.
test: vm $(SAMPLES:%=samples/%.vm) $(RUNTIME:%=tests/%.vm)
	$(PYTHON) conform.py ./vm -g mark
	$(PYTHON) conform.py ./vm -g copy -S
	$(PYTHON) conform.py $(PYTHON) vm.py
	programs="$$(ls build/*.vm | grep -v garbage) samples/closures.vm samples/data.vm"; \
	$(PYTHON) compare.py "./vm -g mark" "./vm -g copy -S" $$programs && \
	$(PYTHON) compare.py "./vm" "$(PYTHON) vm.py" $$programs
	for g in "-g mark" "-g copy" "-g mark -S" "-g copy -S"; do for s in $(SAMPLES); do \
	    ./vm $$g samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	done; done
	for e in $(ERRORS); do \
	    ! $(PYTHON) lambda.py tests/$$e.lam 2>&1 >/dev/null || echo "$$e: no error"; \
	done | diff -u tests/errors.txt -
	for r in $(RUNTIME); do \
	    ! ./vm tests/$$r.vm > tests/$$r.got 2>&1 || exit 1; \
	    diff -u tests/$$r.txt tests/$$r.got || exit 1; \
	done
	@echo "ch15: ok"

clean:
	rm -rf vm samples/*.asm samples/*.vm tests/*.asm tests/*.vm tests/*.got build __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
