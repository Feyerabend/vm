#!/bin/sh
# Time each benchmark interpreted (chapter 19's machine, which verifies
# and then runs without the checks it proved unnecessary) and compiled
# to native code by vm2c.py: best of five, milliseconds.
#
#     ./bench.sh            (after make benchmarks)

best() {
    b=""
    for i in 1 2 3 4 5; do
        s=$(date +%s%N)
        "$@" > /dev/null 2>&1
        e=$(date +%s%N)
        t=$(( (e - s) / 1000000 ))
        if [ -z "$b" ] || [ "$t" -lt "$b" ]; then b=$t; fi
    done
    echo "$b"
}

printf "%-12s %12s %10s %8s\n" "" "interpreted" "native" "faster"
for p in fib loop sieve closures enkel-sieve basal-loop; do
    i=$(best ./vm bench/$p.vm)
    n=$(best ./bench/$p)
    printf "%-12s %9s ms %7s ms %7sx\n" "$p" "$i" "$n" "$(echo "scale=1; $i / ($n + 0.5)" | bc)"
done
