#!/bin/sh
rm -f sample.a
rm -f sample.b
rm -f sample.q
python3 ./strip.py -i sample.p -o sample.q
./enkel -v -i sample.q -o sample.a
python3 ./asm.py -v -i sample.a -o sample.b
./runvm sample.b
