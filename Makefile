# Build and test every chapter, and the appendix.

CHAPTERS := $(sort $(wildcard ch[0-9][0-9]-*))

test:
	@for d in $(CHAPTERS); do $(MAKE) -s -C $$d test || exit 1; done
	@$(MAKE) -s -C appendix test

clean:
	@for d in $(CHAPTERS); do $(MAKE) -s -C $$d clean; done
	@$(MAKE) -s -C appendix clean

.PHONY: test clean
