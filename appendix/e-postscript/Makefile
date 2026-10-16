PYTHON ?= python3

PICTURES := tree star

# The calculation prints what it should, and each picture is drawn
# exactly as before: the SVG files are kept, and shown in README.md.
test:
	$(PYTHON) ps.py samples/calc.ps | diff -u samples/calc.out -
	for s in $(PICTURES); do \
	    $(PYTHON) ps.py samples/$$s.ps samples/$$s.got || exit 1; \
	    cmp samples/$$s.svg samples/$$s.got || exit 1; \
	done
	@echo "appendix e: ok"

clean:
	rm -rf samples/*.got __pycache__

.PHONY: test clean
