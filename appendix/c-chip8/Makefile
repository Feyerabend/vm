PYTHON ?= python3

SAMPLES := answer collide

# Each sample leaves the screen it should.
test:
	for s in $(SAMPLES); do \
	    $(PYTHON) chip8.py samples/$$s.hex | diff -u samples/$$s.out - || exit 1; \
	done
	@echo "appendix c: ok"

clean:
	rm -rf __pycache__

.PHONY: test clean
