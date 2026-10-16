import sys
import re

if len(sys.argv) != 3:
    print("Usage: asm <input> <output>")
    exit()

with open(sys.argv[1]) as f:
    content = f.readlines()

def no_comments(content):
    ncontent = []
    for line in content:
        temp = re.sub('#.*', '', line)
        ncontent.append(temp)
    return ncontent

# no comments and other stuff
def prepare(content):
    content = no_comments(content)
    # no new lines
    content = [' '.join(line.split()) for line in content]
    # no white space
    content = [line for line in content if line.strip()]
    # group and "tokenize"
    content = [line.split() for line in content if line]
    return content

ops = [
    'ADD',
    'AND',
    'CALL',
    'DEC',
    'DROP',
    'DUP',
    'EQ',
    'EQZ',
    'HALT',
    'INC',
    'JP',
    'JPNZ',
    'JPZ',
    'LD',
    'LDARG',
    'LOAD',
    'LSH',
    'LT',
    'MOD',
    'MUL',
    'NA',
    'NOP',
    'OR',
    'PRINT',
    'PRNT',
    'RET',
    'RSH',
    'SET',
    'SETZ',
    'ST',
    'STARG',
    'STORE',
    'SUB']

ary = [
    0,      # ADD
    0,      # AND
    1,      # CALL addr
    0,      # DEC
    0,      # DROP
    0,      # DUP
    0,      # EQ
    0,      # EQZ
    0,      # HALT
    0,      # INC
    1,      # JP addr
    1,      # JPNZ addr
    1,      # JPZ addr
    1,      # LD local_reg
    1,      # LDARG arg_reg
    1,      # LOAD global_reg
    0,      # LSH
    0,      # LT
    0,      # MOD
    0,      # MUL
    0,      # NA
    0,      # NOP
    0,      # OR
    0,      # PRINT
    0,      # PRNT
    0,      # RET
    0,      # RSH
    1,      # SET number
    0,      # SETZ
    1,      # ST local_reg
    1,      # STARG arg_reg
    1,      # STORE global_reg
    0]      # SUB

registers = [
    'R0',
    'R1',
    'R2',
    'R3',
    'R4',
    'R5',
    'R6',
    'R7',
    'R8',
    'R9']

# turn to decimal
def to_decimal(number):
    return int(number)

# find syntax of "registers", and replace with number
def reg(token):
    if token not in registers:
        return token
    return registers.index(token)

# replace the corresponing opcodes with numbers, and arguments
def parse(line):
    if (line[0] in ops):
        nline = []
        i = ops.index(line[0])
        code = int(i)
        ar = ary[i]
        nline.append(code)
        if (ar == 1):
            nline.append(reg(line[1]))
        return nline
    else:
        return line

# main:
# prep
content = prepare(content)

# parse
ncontent = []
for item in range(len(content)):
    line = content[item]
    line = parse(line)
    ncontent.append(line)
content = ncontent

# hunt for labels
ncontent = []
labels = {} # a dictionary of labels
offset = 0 # begin at address zero
for item in [val for sublist in content for val in sublist]:
    islabel = (str(item)[-1] == ':') # ex. START:
    if islabel:
        matchlabel = (':' + item[:-1])
        labels[matchlabel] = offset # ex. :START
    else:
        offset = offset + 1
        ncontent.append(item)

# replace labels with their offset
ncontent = [labels[token] if token in labels else token for token in ncontent]

# convert some remains to decimal
final = [to_decimal(i) for i in ncontent]

print("------- copy and paste")
print(final)
print("START: ", labels[':START'])

final_str = [str(int) for int in final]
with open(sys.argv[2], "w") as f:
    f.write(','.join(final_str))
