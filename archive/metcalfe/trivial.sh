#!/bin/sh
rm -f trivial.b
python3 met.py -v -i trivial.mc -o trivial.b
python3 calfe.py -v -t trivial.test -i trivial.b -o trivial.out
