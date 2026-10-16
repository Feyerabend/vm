#!/bin/sh
rm -f sample.a
rm -f sample.b
./cmp4 sample.p
python3 ./asm.py -v -i sample.a -o sample.b
./runvm sample.b
