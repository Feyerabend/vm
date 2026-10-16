IVERILOG ?= iverilog
PYTHON ?= python3

SAMPLES := $(basename $(notdir $(wildcard samples/*.asm)))

# The tests of the suite that use the heap or CALLI, version 3 and 4 of
# the specification, which this CPU does not implement. Found from the
# tests themselves, so that the list cannot drift.
LATER := $(shell grep -l -E '^\s*[A-Za-z_]*:?\s*(NEW|GETF|SETF|LEN|CALLI)\b|\.word (2[7-9]|3[01])' \
             suite/*.asm | xargs -n1 basename | sed 's/\.asm$$//' | paste -sd, -)

all: sim

# Compile the CPU and its testbench into a simulation.
sim: cpu.v tb.v
	$(IVERILOG) -g2012 -Wall -o $@ tb.v cpu.v

%.vm: %.asm asm.py isa.py vmfile.py
	$(PYTHON) asm.py $< $@

# 1. The simulated CPU passes the conformance suite: every test of
#    versions 1 and 2. The tests of versions 3 and 4 are known failures.
# 2. Programs compiled from enkel/0 and basal/0 run on it, and print
#    what they should.
test: sim $(SAMPLES:%=samples/%.vm)
	$(PYTHON) conform.py --known $(LATER) $(PYTHON) vrun.py
	for s in $(SAMPLES); do \
	    $(PYTHON) vrun.py samples/$$s.vm | diff -u samples/$$s.out - || exit 1; \
	done
	@echo "ch22: ok"

clean:
	rm -rf sim samples/*.vm build __pycache__

.PHONY: all test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
