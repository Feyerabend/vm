CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2

TRAPS := divzero underflow deep forever badop runoff badjump badret

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

# The good program must print what it should. Each bad program must
# stop with exit status 1 and the right message.
test: vm
	./vm | diff -u expected.txt -
	for p in $(TRAPS); do \
	    out=$$(./vm $$p 2>&1); st=$$?; \
	    echo "$$out" | sed "s/^/$$p: /"; \
	    test $$st = 1 || echo "$$p: exit status $$st"; \
	done | diff -u traps.txt -
	@echo "ch04: ok"

clean:
	rm -f vm

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
