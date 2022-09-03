#!/bin/sh
rm -f sample.a
rm -f sample.b
./enkel -v -i sample.p -o sample.a
python3 ./asm.py -v -i sample.a -o sample.b
./runvm sample.b
