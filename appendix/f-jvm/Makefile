PYTHON ?= python3
JAVA ?= java
JAVAC ?= javac

CLASSES := Fib Sieve Divide

# 1. Each class prints what it should, and ends as it should: its
#    output, its stack trace, and its exit status.
# 2. If Java is installed, the real JVM does exactly the same.
test:
	for c in $(CLASSES); do \
	    { $(PYTHON) jvm.py classes/$$c.class 2>&1; echo "status $$?"; } | diff -u tests/$$c.out - || exit 1; \
	done
	if command -v $(JAVA) > /dev/null; then \
	    for c in $(CLASSES); do \
	        { env -u JAVA_TOOL_OPTIONS $(JAVA) -cp classes $$c 2>&1; echo "status $$?"; } | diff -u tests/$$c.out - || exit 1; \
	    done; \
	    echo "the real JVM agrees"; \
	fi
	@echo "appendix f: ok"

# The class files are kept in the repository, so that the tests need
# no Java compiler. This makes them again.
classes:
	$(JAVAC) --release 11 -d classes src/*.java

clean:
	rm -rf __pycache__

.PHONY: test classes clean
