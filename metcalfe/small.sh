#!/bin/sh
rm -f small.b
python3 met.py -v -i small.mc -o small.b
python3 calfe.py -v -t small.test -i small.b -o small.out
