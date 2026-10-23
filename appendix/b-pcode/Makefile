PYTHON ?= python3
FPC ?= fpc

PL0 := gcd nested
P4 := hello nested

# 1. Each PL/0 sample prints what it should.
# 2. Each P4 program written by hand prints what it should.
# 3. Each pascal/0 program compiles to the P4 code kept beside it, and
#    that code prints what it should and ends as it should. The ones in
#    traps/ break a rule, and the machine stops them with a message.
# 4. The compiler refuses each program in errors/, with a message.
# 5. If Free Pascal is installed, it prints exactly the same as the P4
#    machine for every program in pascal/.
test:
	for s in $(PL0); do \
	    $(PYTHON) pmachine.py samples/$$s.p | diff -u samples/$$s.out - || exit 1; \
	done
	for s in $(P4); do \
	    $(PYTHON) p4.py samples/$$s.p4 | diff -u samples/$$s.out - || exit 1; \
	done
	for f in pascal/*.pas pascal/traps/*.pas; do \
	    p=$${f%.pas}; in=/dev/null; [ -f $$p.in ] && in=$$p.in; \
	    $(PYTHON) pascal.py $$f | diff -u $$p.p4 - || exit 1; \
	    { $(PYTHON) p4.py $$p.p4 < $$in 2>&1; echo "status $$?"; } | diff -u $$p.out - || exit 1; \
	done
	for f in pascal/errors/*.pas; do \
	    { $(PYTHON) pascal.py $$f 2>&1 > /dev/null; echo "status $$?"; } | diff -u $${f%.pas}.err - || exit 1; \
	done
	if command -v $(FPC) > /dev/null; then \
	    mkdir -p build; \
	    for f in pascal/*.pas; do \
	        p=$${f%.pas}; s=$$(basename $$p); in=/dev/null; [ -f $$p.in ] && in=$$p.in; \
	        $(FPC) -Miso -v0 -FEbuild $$f > build/$$s.log 2>&1 || { cat build/$$s.log; exit 1; }; \
	        { build/$$s < $$in 2>&1; echo "status $$?"; } | diff -u $$p.out - || exit 1; \
	    done; \
	    echo "Free Pascal agrees"; \
	fi
	@echo "appendix b: ok"

# The P4 code and the expected output of every pascal/0 program, made
# again. Read the differences before keeping them.
expect:
	for f in pascal/*.pas pascal/traps/*.pas; do \
	    p=$${f%.pas}; in=/dev/null; [ -f $$p.in ] && in=$$p.in; \
	    $(PYTHON) pascal.py $$f > $$p.p4; \
	    { $(PYTHON) p4.py $$p.p4 < $$in 2>&1; echo "status $$?"; } > $$p.out; \
	done
	for f in pascal/errors/*.pas; do \
	    { $(PYTHON) pascal.py $$f 2>&1 > /dev/null; echo "status $$?"; } > $${f%.pas}.err; \
	done

clean:
	rm -rf __pycache__ build

.PHONY: test expect clean
