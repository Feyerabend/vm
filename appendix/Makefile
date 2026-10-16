# Test every study of the appendix.

STUDIES := $(sort $(wildcard [a-z]-*))

test:
	@for d in $(STUDIES); do $(MAKE) -s -C $$d test || exit 1; done

clean:
	@for d in $(STUDIES); do $(MAKE) -s -C $$d clean; done

.PHONY: test clean
