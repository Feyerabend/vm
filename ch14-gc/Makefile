CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2
PYTHON ?= python3

SAMPLES := strings lists bounds trees

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. The conformance suite passes, 'garbage' included, with both
#    collectors, with and without stress, and on the Python machine.
# 2. A trace is the same whichever collector runs, under stress or
#    not, and on the Python machine. ('garbage' and 'trees' are left
#    out here only because their traces run to millions of lines.)
# 3. The samples print what they should, with both collectors.
test: vm $(SAMPLES:%=samples/%.vm)
	$(PYTHON) conform.py ./vm -g mark
	$(PYTHON) conform.py ./vm -g copy
	$(PYTHON) conform.py ./vm -g mark -S
	$(PYTHON) conform.py ./vm -g copy -S
	$(PYTHON) conform.py $(PYTHON) vm.py
	programs="$$(ls build/*.vm | grep -v garbage) samples/strings.vm samples/lists.vm samples/bounds.vm"; \
	$(PYTHON) compare.py "./vm -g mark" "./vm -g copy -S" $$programs && \
	$(PYTHON) compare.py "./vm -g copy" "./vm -g mark -S" $$programs && \
	$(PYTHON) compare.py "./vm" "$(PYTHON) vm.py" $$programs
	for g in mark copy; do for s in $(SAMPLES); do \
	    ./vm -g $$g samples/$$s.vm 2>&1 | diff -u samples/$$s.out - || exit 1; \
	done; done
	@echo "ch14: ok"

clean:
	rm -rf vm samples/*.vm build __pycache__

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
