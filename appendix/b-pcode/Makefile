PYTHON ?= python3

SAMPLES := gcd nested

# Each sample prints what it should.
test:
	for s in $(SAMPLES); do \
	    $(PYTHON) pmachine.py samples/$$s.p | diff -u samples/$$s.out - || exit 1; \
	done
	@echo "appendix b: ok"

clean:
	rm -rf __pycache__

.PHONY: test clean
