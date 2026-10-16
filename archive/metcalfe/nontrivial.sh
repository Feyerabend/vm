#!/bin/sh
rm -f nontrivial.b
python3 met.py -v -i nontrivial.mc -o nontrivial.b
python3 calfe.py -v -t nontrivial.test -i nontrivial.b -o nontrivial.out
