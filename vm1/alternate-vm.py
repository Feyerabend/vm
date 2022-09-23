#!/usr/bin/env python
# coding: utf-8

import sys


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        return self.stack.pop()


class VM:
    def __init__(self):
        self.code = []
        self.stack = Stack()
        self.pc = -1

    def mul(self):
        b = self.stack.pop()
        a = self.stack.pop()
        c = int(a) * int(b)
        self.stack.push(c)

    def add(self):
        b = self.stack.pop()
        a = self.stack.pop()
        c = int(a) + int(b)
        self.stack.push(c)

    def sub(self):
        b = self.stack.pop()
        a = self.stack.pop()
        c = int(a) - int(b)
        self.stack.push(c)

    def set(self, number):
        self.stack.push(number)

    def printn(self):
        a = self.stack.pop()
        print(a)

    def setcode(self, contents):
        self.code = contents

    def nextcode(self):
        self.pc = self.pc + 1
        return self.code[self.pc]

    def parse(self, command):
        match command.split():
            case ['MUL']:
                self.mul()
            case ['ADD']:
                self.add()
            case ['SUB']:
                self.sub()
            case ['SET', number]:
                self.set(number)
            case ['PRINT']:
                self.printn()
            case ['HALT']:
                sys.exit(0)
            case _:  # catch all
                print(f"{command!r}?")

    def run(self, contents):
        self.setcode(contents)
        while (True):
            opcode = self.nextcode()
            command = opcode.strip()
            self.parse(command)


class Runner:
    def __init__(self):
        self.vm = VM()
        self.contents = []

    def readsample(self, file):
        with open(file) as f:
            self.contents = f.readlines()
            print(self.contents)
        f.close()
        self.vm.run(self.contents)


run = Runner()
run.readsample('sample.txt')
