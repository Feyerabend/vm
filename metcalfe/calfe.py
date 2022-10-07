#!/usr/bin/env python
# coding: utf-8

import sys
from collections import deque

# internal
EXIT =     -1
DONE =     -2

# instructions
# must be in sync with met.py
NOP =       0
CALL =      1
FALSE =     2
FFLAG =     3
TFLAG =     4
MATCH =     5
PRINT =     6
RETURN =    7
STOP =      8
TRUE =      9

# stack
class Stack:

    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if (len(self.stack) > 0):
            return self.stack.pop()
        return EXIT


class Machine:

    def __init__(self):
        self.code = [] # deque()
        self.stack = Stack()
        self.tape = Stack()
        self.pc = 0
        self.FLAG = False # global flag
        self.INPUT = ""
        self.inp = 0 # input pointer
        self.OUTPUT = []
        self.outp = 0 # output pointer

    def setcode(self, contents):
        self.code = contents

    def setinput(self, input):
        self.INPUT = input
        self.OUTPUT = []

    def getoutput(self):
        return ' '.join(self.OUTPUT)

    # get value from address
    # increase programcounter
    def nextcode(self):
        if (self.pc < len(self.code)):
            c = self.code[self.pc]
            self.pc = self.pc + 1
            return c
        return EXIT

    # parse one op at a time
    # then execute/interpret on op
    def parse(self, op):

        # call address and
        # put current pc on stack
        if (op == CALL):
            address = self.nextcode()
            self.tape.push(self.inp)
            self.tape.push(self.outp)
            self.stack.push(self.pc)
            self.pc = address

        # if flag is false, then jump address
        # always consume address
        elif (op == FALSE):
            address = self.nextcode()
            if (self.FLAG == False):
                self.pc = address
            arg = address

        # set global FLAG to false
        elif (op == FFLAG):
            self.FLAG = False

        # set global FLAG to true
        elif (op == TFLAG):
            self.FLAG = True

        # check what's on input tape
        # match item with tape
        # put mathcing item on output
        # advance input tape
        elif (op == MATCH):
            item = self.nextcode()
            c = self.INPUT[self.inp]
            if (c == '$'):
                return DONE
            if (c == item):
                self.FLAG = True
                self.inp = self.inp + 1
            else:
                self.FLAG = False

        # print to output tape following item
        elif (op == PRINT):
            item = self.nextcode()
            self.OUTPUT.insert(self.outp, item)
            self.outp = self.outp + 1

        # return from call
        # pop address from stack
        # jump to address
        elif (op == RETURN):
            # print("return")
            # pop address, set pc
            address = self.stack.pop()
            self.pc = address

            # pop the output pointer
            self.outp = self.tape.pop()

            # if flag is false then set input pointer
            # from tape stack
            # if true the just pop from stack, correct?
            pointer = self.tape.pop()
            if (self.FLAG == False):
                self.inp = pointer

        # explicit stop program and exit loop
        elif (op == STOP):
            return DONE

        # if flag is then, then jump address
        # always consume address
        elif (op == TRUE):
            address = self.nextcode()
            if (self.FLAG == True):
                self.pc = address

        return

    # at last a print out
    def printout(self):
        print("OUTPUT=", self.getoutput())

    # running code
    def run(self, contents):
        self.setcode(contents)
        while (True):
            opcode = self.nextcode()
            if (opcode == EXIT): # no more codes
                return
            endflag = self.parse(opcode)
            if (endflag == DONE): # explicit stop
                self.printout()
                return


class Runner:

    def __init__(self):
        self.m = Machine()
        self.contents = []

    def readsample(self, input, file):
        self.m.setinput(input + '$') # if not already mark $ end
        print("INPUT=", self.m.INPUT)

        with open(file, 'r') as f:
            for line in f.readlines():
                chars = line.strip().split(',')
                # if not a digit assume a character for matching, assemble in array
                self.contents.extend([int(i) if i.isdigit() else i for i in chars])
        f.close()
        self.m.run(self.contents)


run = Runner()
run.readsample('(i+i)', 'etf.b') # ((i+i)*i+(i*i*i))
