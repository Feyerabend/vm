#!/bin/sh
# For each benchmark: instructions dispatched, and time (best of five
# runs, milliseconds), without and with the optimiser, on threaded code
# without and with superinstructions.
#
#     ./measure.sh          (after make benchmarks)

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

steps() {
    "$@" 2>&1 >/dev/null | sed -n 's/^steps: //p'
}

printf "%-12s %14s %14s %14s %14s\n" "dispatches" "plain" "optimised" "super" "both"
for p in fib loop sieve closures enkel-sieve basal-loop; do
    printf "%-12s %14s %14s %14s %14s\n" "$p" \
        "$(steps ./vm-threaded -c bench/$p.vm)" "$(steps ./vm-threaded -c bench/$p.opt.vm)" \
        "$(steps ./vm-super -c bench/$p.vm)" "$(steps ./vm-super -c bench/$p.opt.vm)"
done
echo
printf "%-12s %11s %14s %14s %14s\n" "ms" "plain" "optimised" "super" "both"
for p in fib loop sieve closures enkel-sieve basal-loop; do
    printf "%-12s %11s %14s %14s %14s\n" "$p" \
        "$(best ./vm-threaded bench/$p.vm)" "$(best ./vm-threaded bench/$p.opt.vm)" \
        "$(best ./vm-super bench/$p.vm)" "$(best ./vm-super bench/$p.opt.vm)"
done
