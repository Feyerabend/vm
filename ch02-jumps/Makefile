CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -O2

vm: vm.c
	$(CC) $(CFLAGS) -o $@ vm.c

test: vm
	./vm | diff -u expected.txt - && echo "ch02: ok"

clean:
	rm -f vm

.PHONY: test clean

# Keep files made on the way, such as a .vm made only to become a
# .rvm: by default make deletes them, and a second run then fails.
.SECONDARY:
