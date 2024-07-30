#!/bin/sh
clear
python3 vm.py --singlestep true --breakpoints 14,16 --trace true --input sample.b
