
import re
import sys
import getopt


CALL =      0
FALSE =     1
FFALSE =    2
FTRUE =     3
MATCH =     4
PRINT =     5
RETURN =    6
STOP =      7
TRUE =      8

# must be in sync with calfe.py
ops = {
    CALL:   'call',
    FALSE:  'false',
    FFALSE: 'fflag',
    FTRUE:  'tflag',
    MATCH:  'match',
    PRINT:  'print',
    RETURN: 'return',
    STOP:   'stop',
    TRUE:   'true'}

ary = [
    1,      # call addr
    1,      # false addr
    0,      # fflag
    0,      # tflag
    1,      # match item
    1,      # print item
    0,      # return
    0,      # stop
    1]      # true addr

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

# replace the corresponing opcodes with numbers,
# and add arguments
def parse(line):

    # check for command in ops .. first item in line
    val = [i for i in ops if ops[i] == line[0]]

    # if command not empty
    if (val != []):
        nline = []
        i = val[0]
        code = int(i) # convert command to it's int
        ar = ary[i] # important if ary > 0
        nline.append(code) # add command to list
        if (ar == 1):
            nline.append(line[1]) # add arg as is to list
        return nline
    else:
        # don't touch
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

    if verbose:
        print("parsed:", content)

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

    if verbose:
        print("no labels:", ncontent)

    # stringify the numbers for output
    final = [str(int) for int in ncontent]
    final = ','.join(final)

    if verbose:
        print("out to file:", final)

    with open(outputfile, "w") as f:
        f.write(final)
    f.close()

    return final


# call with parsing of args to assembler
def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('met.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: met.py -i <inputfile> -o <outputfile>')
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
