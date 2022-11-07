import re
import sys
import getopt

# must be in sync with vm.h
ops = [
    'ADD',
    'AND',
    'CALL',
    'DIV',
    'EMIT',
    'EQ',
    'GT',
    'GQ',
    'HALT',
    'JP',
    'JPNZ',
    'JPZ',
    'LD',
    'LDARG',
    'LOAD',
    'LT',
    'LQ',
    'MOD',
    'MUL',
    'NEQ',
    'NOP',
    'OR',
    'PRINT',
    'PRNT',
    'RET',
    'RLOAD',
    'RSTORE',
    'SET',
    'ST',
    'STARG',
    'STORE',
    'SUB',
    'UMIN',
    'XOR']

ary = [
    0,      # ADD
    0,      # AND
    1,      # CALL addr
    0,      # DIV
    0,      # EMIT
    0,      # EQ
    0,      # GT
    0,      # GQ
    0,      # HALT
    1,      # JP addr
    1,      # JPNZ addr
    1,      # JPZ addr
    1,      # LD local_reg
    1,      # LDARG arg_reg
    1,      # LOAD global_reg
    0,      # LT
    0,      # LQ
    0,      # MOD
    0,      # MUL
    0,      # NEQ
    0,      # NOP
    0,      # OR
    0,      # PRINT
    0,      # PRNT
    0,      # RET
    0,      # RLOAD
    0,      # RSTORE
    1,      # SET number
    1,      # ST local_reg
    1,      # STARG arg_reg
    1,      # STORE global_reg
    0,      # SUB
    0,      # UMIN
    0]      # XOR

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

# turn to decimal
def to_decimal(number):
    return int(number)

# replace the corresponing opcodes with numbers, and arguments
def parse(line):
    if (line[0] in ops):
        nline = []
        i = ops.index(line[0])
        code = int(i)
        ar = ary[i]
        nline.append(code)
        if (ar == 1):
            nline.append(line[1])
        return nline
    else:
        return line

# assemble binary
def assemble(inputfile, outputfile, verbose):

    # read in file
    with open(inputfile) as f:
        content = f.readlines()

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

    if verbose == 1:
        print(final)
        print("START: ", labels[':START'])

    final.insert(0, labels[':START'])
    final_str = [str(int) for int in final]
    with open(outputfile, "w") as f:
        f.write(','.join(final_str))


# call with parsing of args to assembler
def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('asm.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: asm.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if verbose == 1:
        print("assembling ..")
    assemble(inputfile, outputfile, verbose)
    if verbose == 1:
        print("done.")


if __name__ == "__main__":
   main(sys.argv[1:])
