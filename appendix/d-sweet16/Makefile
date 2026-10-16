PYTHON ?= python3

# Each sample leaves the registers and the memory it should.
test:
	$(PYTHON) sweet16.py -m 0900:090F samples/copy.s16 | diff -u samples/copy.out -
	$(PYTHON) sweet16.py -m 0900:092F samples/fib.s16 | diff -u samples/fib.out -
	@echo "appendix d: ok"

clean:
	rm -rf __pycache__

.PHONY: test clean
