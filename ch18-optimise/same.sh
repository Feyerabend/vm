#!/bin/sh
# Check that the optimiser changes nothing a program does: run each
# program as it is and optimised, and compare what it prints, its exit
# status, and its trap message. Only the address in a trap message may
# differ, since optimising moves code.
#
#     ./same.sh program.asm ...

failed=0
for f in "$@"; do
    tmp=$(mktemp -d)
    python3 asm.py "$f" "$tmp/a.vm" 2>/dev/null || { rm -rf "$tmp"; continue; }
    python3 opt.py "$f" > "$tmp/o.asm" && python3 asm.py "$tmp/o.asm" "$tmp/o.vm" || {
        echo "$f: the optimised program does not assemble"; failed=1; rm -rf "$tmp"; continue; }
    a=$(./vm-threaded "$tmp/a.vm" 2>&1; echo "status $?")
    o=$(./vm-threaded "$tmp/o.vm" 2>&1; echo "status $?")
    a=$(echo "$a" | sed 's/^\(trap: .*\) at [0-9]*$/\1/')
    o=$(echo "$o" | sed 's/^\(trap: .*\) at [0-9]*$/\1/')
    if [ "$a" != "$o" ]; then
        echo "$f: behaves differently when optimised"
        failed=1
    fi
    rm -rf "$tmp"
done
exit $failed
