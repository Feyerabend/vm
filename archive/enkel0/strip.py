import re
import sys
import getopt


# found in github gist
# https://gist.github.com/ChunMinChang/88bfa5842396c1fbbc5b
def nocomments(text):

    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return "\n" * s.count("\n")
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('strip.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: strip.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if verbose == 1:
        print("uncomment ..")
    with open(inputfile) as f:
        content = f.read()
    uncommented = nocomments(content)
    with open(outputfile, "w") as f:
        f.write(uncommented)
    if verbose == 1:
        print("done.")

if __name__ == "__main__":
   main(sys.argv[1:])
