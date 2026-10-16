#!/bin/sh
# Run every program in a directory twice, verified and with every
# check (-C), on a machine built for testing: with AddressSanitizer and
# UndefinedBehaviorSanitizer, and with a limit on steps, so that
# programs that loop forever stop at the same place both times. Any
# difference between the two runs, or any complaint from a sanitizer,
# means the verifier accepted something it should not have.
#
#     ./fuzz.sh ./vm-fuzz directory

vm=$1
dir=$2
total=0
verified=0
failed=0
for p in "$dir"/*.vm; do
    total=$((total + 1))
    if "$vm" -V "$p" > /dev/null 2>&1 || [ $? -ne 2 ]; then
        verified=$((verified + 1))
    fi
    a=$("$vm" "$p" 2>&1; echo "status $?")
    c=$("$vm" -C "$p" 2>&1; echo "status $?")
    case "$a$c" in
        *Sanitizer*|*"runtime error"*)
            echo "$p: a sanitizer complained"
            failed=1
            continue
            ;;
    esac
    if [ "$a" != "$c" ]; then
        echo "$p: the verified and the checked run differ"
        failed=1
    fi
done
echo "$total programs, $verified of them verified"
[ $failed = 0 ] && echo "every verified run was the same as the checked run"
exit $failed
