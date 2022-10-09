#!/bin/sh
rm -f etf.b
python3 met.py -v -i etf.mc -o etf.b
python3 calfe.py -v -t etf.test -i etf.b -o etf.out
