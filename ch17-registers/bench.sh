#!/bin/sh
# Time each benchmark on the stack machine and on the register
# machine, with naive and improved translation: best of three runs.
#
#     ./bench.sh            (after make benchmarks)

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

printf "%-8s %12s %16s %16s\n" "" "stack" "register, naive" "register"
for p in fib loop sieve; do
    printf "%-8s %9s ms %13s ms %13s ms\n" "$p" \
        "$(best ./vm bench/$p.vm)" "$(best ./rvm bench/$p-naive.rvm)" "$(best ./rvm bench/$p.rvm)"
done
