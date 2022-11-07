
from lexer import *
from macro import *
from parse import *
import getopt
import sys

# make code
def compilecode(inputfile, outputfile, verbose):
    # sequence of compiling
    tok = Tokenize(inputfile) # make tokens
    temp = 'tokens.csv' # use a file to store the tokens
    tok.write(temp) # write it ..
    mac = Filter(temp) # .. filter it ..
    parser = Parser(temp) # .. load the file
    out = parser.program() # parse file

    # finished assembly program
    with open(outputfile, "w") as f:
        for i in out:
            f.write(i)
            f.write('\n')
    f.close()

# call with parsing of args to compiler
def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('compiler.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: compiler.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if verbose == 1:
        print("compiling ..")
    compilecode(inputfile, outputfile, verbose)
    if verbose == 1:
        print("done.")


if __name__ == "__main__":
   main(sys.argv[1:])
