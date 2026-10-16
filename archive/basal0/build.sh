#!/bin/sh
rm -f sample.a
rm -f sample.b
clear
python3 compiler.py -i sample.bas -o sample.a
python3 asm.py -i sample.a -o sample.b
./runvm sample.b
