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


class Emulator:
    def __init__(self):
        self.stack = Stack()

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


class Runner:
    def __init__(self):
        self.emu = Emulator()

    def read(self, file):
        with open(file) as f:
            contents = f.readlines()
            print(contents)
            for line in contents:
                command = line.strip()
                self.emu.parse(command)
        f.close()

run = Runner()
run.read('sample.txt')
