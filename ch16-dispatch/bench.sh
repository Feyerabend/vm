#!/bin/sh
# Time each benchmark with each build, best of three runs.
#
#     ./bench.sh
#
# Needs vm-switch, vm-goto and vm-threaded (make all) and the
# benchmarks assembled (make benchmarks).

best() {
    b=""
    for i in 1 2 3; do
        s=$(date +%s%N)
        "$@" > /dev/null
        e=$(date +%s%N)
        t=$(( (e - s) / 1000000 ))
        if [ -z "$b" ] || [ "$t" -lt "$b" ]; then b=$t; fi
    done
    echo "$b"
}

printf "%-10s %10s %10s %10s\n" "" "switch" "goto" "threaded"
for p in fib loop sieve closures; do
    printf "%-10s" "$p"
    for v in switch goto threaded; do
        printf " %8s ms" "$(best ./vm-$v bench/$p.vm)"
    done
    printf "\n"
done
