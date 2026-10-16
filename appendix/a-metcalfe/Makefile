PYTHON ?= python3

SAMPLES := postfix choice

# Each sample program reads its lines, and says what it made of them.
test:
	for s in $(SAMPLES); do \
	    $(PYTHON) metcalfe.py samples/$$s.mc < samples/$$s.in | diff -u samples/$$s.out - || exit 1; \
	done
	@echo "appendix a: ok"

clean:
	rm -rf __pycache__

.PHONY: test clean
