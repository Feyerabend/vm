from enum import Enum, unique
from collections import deque
import queue
import time
import csv
import sys

TRUE = 1
FALSE = 0

@unique
class OP(Enum):
	ADD = 0
	AND = 1
	CALL = 2
	DIV = 3
	EMIT = 4
	EQ = 5
	GT = 6
	GQ = 7
	HALT = 8
	JP = 9
	JPNZ = 10
	JPZ = 11
	LD = 12
	LDARG = 13
	LOAD = 14
	LT = 15
	LQ = 16
	MOD = 17
	MUL = 18
	NEQ = 19
	NOP = 20
	OR = 21
	PRINT = 22
	PRNT = 23
	RET = 24
	RLOAD = 25
	RSTORE = 26
	SET = 27
	ST = 28
	STARG = 29
	STORE = 30
	SUB = 31
	UMIN = 32
	XOR	= 33


class Stack:
	def __init__(self):
		self.stack = []
	def push(self, value):
		self.stack.append(value)
	def pop(self):
		return self.stack.pop()
	def peek(self):
		return self.stack[-1]
	def isEmpty(self):
		return self.stack == []
	def size(self):
		return len(self.stack)


class VM:
	def __init__(self, code, start, arrs, args, vars):
		self.stack = [] # Stack
		self.sp = -1
		self.fp = 0

		self.arrs = [] # "arrays"
		self.args = [] # passed to routines/procedures
		self.vars = [] # global variables
		self.arrs = [0 for i in range(arrs)]
		self.args = [0 for i in range(args)]
		self.vars = [0 for i in range(vars)]

		self.pc = start # where to start
		self.code = code

	def pop(self):
		if self.stack == []:
			raise Exception("Runtime error: stack is empty")
		self.sp -= 1
		value = int(self.stack.pop())
		return value

	def push(self, value):
		self.sp += 1
		self.stack.append(int(value))

	def nextcode(self):
		if self.pc < 0 or self.pc > len(self.code) - 1:
			raise Exception("Runtime error: program counter out of range (%d)" % self.pc)
		acode = self.code[self.pc]
		self.pc += 1
		return acode

	def run(self):

		while True:
			op = self.nextcode()
			if op == None:
				break

			if op == OP.ADD.value:
				b = self.pop()
				a = self.pop()
				c = a + b
				self.push(c)

			elif op == OP.AND.value:
				b = self.pop()
				a = self.pop()
				c = a & b
				self.push(c)

			elif op == OP.CALL.value:
				addr = self.nextcode()
				self.push(self.fp)
				self.push(self.pc)
				self.fp = self.sp
				self.pc = addr

			elif op == OP.DIV.value:
				b = self.pop()
				a = self.pop()
				if b == 0:
					raise Exception("Runtime error: division by zero.")
				c = a // b # divmod?
				self.push(c)

			elif op == OP.EMIT.value:
				v = self.pop()
				print(chr(v), end='')

			elif op == OP.EQ.value:
				b = self.pop()
				a = self.pop()
				if a == b:
					c = TRUE
				else:
					c = FALSE
				self.push(c)

			elif op == OP.GT.value:
				b = self.pop()
				a = self.pop()
				if a > b:
					c = TRUE
				else:
					c = FALSE
				self.push(c)

			elif op == OP.GQ.value:
				b = self.pop()
				a = self.pop()
				if a >= b:
					c = TRUE
				else:
					c = FALSE
				self.push(c)

			elif op == OP.HALT.value:
				break

			elif op == OP.JP.value:
				next = self.nextcode()
				if next < 0 or next > len(self.code) - 1:
					raise Exception("Runtime error: program counter out of range (%d)" % next)
				self.pc = next

			elif op == OP.JPNZ.value:
				addr = self.nextcode()
				v = self.pop()
				if addr < 0 or addr > len(self.code) - 1:
					raise Exception("Runtime error: program counter out of range (%d)" % addr)
				if v != 0:
					self.pc = addr

			elif op == OP.JPZ.value:
				addr = self.nextcode()
				v = self.pop()
				if addr < 0 or addr > len(self.code) - 1:
					raise Exception("Runtime error: program counter out of range (%d)" % addr)
				if v == 0:
					self.pc = addr

			elif op == OP.LD.value:
				offset = self.nextcode()
				next = self.fp + offset
				if next > len(self.vars) - 1:
					raise Exception("Runtime error: memory address out of ranges (%d)" % next)
				v = self.vars[next]
				self.push(v)

			elif op == OP.LDARG.value:
				addr = self.nextcode()
				if addr < 0 or addr > len(self.args) - 1:
					raise Exception("Runtime error: loading from argument address out of range (%d)" % addr)
				v = self.args[addr]
				self.push(v)

			elif op == OP.LOAD.value:
				addr = self.nextcode()
				if addr < 0 or addr > len(self.vars) - 1:
					raise Exception("Runtime error: loading from variable address out of range (%d)" % addr)
				v = self.vars[addr]
				self.push(v)

			elif op == OP.LT.value:
				b = self.pop()
				a = self.pop()
				if a < b:
					c = TRUE
				else:
					c = FALSE
				self.push(c)

			elif op == OP.LQ.value:
				b = self.pop()
				a = self.pop()
				if a <= b:
					c = TRUE
				else:
					c = FALSE
				self.push(c)

			elif op == OP.MOD.value:
				b = self.pop()
				a = self.pop()
				c = a % b
				self.push(c)

			elif op == OP.MUL.value:
				b = self.pop()
				a = self.pop()
				c = a * b
				self.push(c)

			elif op == OP.NEQ.value:
				b = self.pop()
				a = self.pop()
				if a != b:
					c = TRUE
				else:
					c = FALSE
				self.push(c)

			elif op == OP.NOP.value:
				pass

			elif op == OP.OR.value:
				b = self.pop()
				a = self.pop()
				c = a | b
				self.push(c)

			elif op == OP.PRINT.value:
				v = self.pop()
				print(int(v))

			elif op == OP.PRNT.value:
				v = self.pop()
				print(int(v), end='')

			elif op == OP.RET.value:
				self.sp = self.fp
				self.pc = self.pop()
				self.fp = self.pop()

			elif op == OP.RLOAD.value:
				a = self.pop()
				if a < 0 or a > len(self.arrs) - 1:
					raise Exception("Runtime error: storing value in array out of range (%d)" % a)
				v = self.arrs[a]
				self.push(v)

			elif op == OP.RSTORE.value:
				a = self.pop()
				b = self.pop()
				if a < 0 or a > len(self.arrs) - 1:
					raise Exception("Runtime error: storing value in array out of range (%d)" % a)
				self.arrs[a] = b

			elif op == OP.SET.value:
				v = self.nextcode()
				self.push(v)

			elif op == OP.ST.value:
				v = self.pop()
				offset = self.nextcode()
				next = self.fp + offset
				if next > len(self.vars) - 1:
					raise Exception("Runtime error: not enough memory reserved for variables (%d)" % next)
				self.vars[next] = v

			elif op == OP.STARG.value:
				v = self.pop()
				addr = self.nextcode()
				if addr < 0 or addr > len(self.args) - 1:
					raise Exception("Runtime error: storing argument out of range (%d)" % addr)
				self.args[addr] = v

			elif op == OP.STORE.value:
				v = self.pop()
				addr = self.nextcode()
				if addr < 0 or addr > len(self.vars) - 1:
					raise Exception("Runtime error: variable storing address out of range (%d)" % addr)
				self.vars[addr] = v

			elif op == OP.SUB.value:
				b = self.pop()
				a = self.pop()
				c = a - b
				self.push(c)

			elif op == OP.UMIN.value:
				a = self.pop(vm)
				self.push(int(-a))

			elif op == OP.XOR.value:
				b = self.pop()
				a = self.pop()
				c = a ^ b
				self.push(c)
# break here?
#			else:
#				break

		return


class Runner:

	# some allocations
	def __init__(self):

		# init (and "allocate")
		self.ARRS = 2048
		self.ARGS = 2048
		self.VARS = 2048

	# get the bytecode and setup the code
	def file(self, file):
		self.file = file

		# read tokens from file, put in temporary queue (store)
		input = []
		with open(self.file, 'r') as f:
			csvf = csv.reader(f, delimiter = ',')
			input.extend(csvf)
		f.close()
		nums = input.pop(0) # get [[list]] to [list]
		self.start = int(nums.pop(0)) # first elem is start
		code = [int(i) for i in nums] # from str to int
		self.code = code

	def run(self):
		# run
		vm = VM(self.code, self.start, self.ARRS, self.ARGS, self.VARS)
		begin = time.time()
		vm.run()
		end = time.time()
		self.duration = end - begin

if __name__ == "__main__":
	runr = Runner()
	print("loading ..")
	runr.file("sample.b")
	print("running ..")
	print("----------------")
	runr.run()
	print("----------------")
	print("duration ", runr.duration, " seconds")
