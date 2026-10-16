#!/bin/sh
# Time each benchmark with every check (-C) and verified: best of five.
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

printf "%-12s %10s %10s\n" "" "checked" "verified"
for p in fib loop sieve enkel-sieve basal-loop; do
    printf "%-12s %7s ms %7s ms\n" "$p" "$(best ./vm -C bench/$p.vm)" "$(best ./vm bench/$p.vm)"
done
