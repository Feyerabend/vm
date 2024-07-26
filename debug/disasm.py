import sys
import getopt

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

# read and split the "binary"
def read_binary_file(inputfile):
    with open(inputfile, 'r') as f:
        content = f.read()
    return [int(i) for i in content.split(',')]

# a two pass disassembler
def disassemble(content, outputfile, verbose):
    start_address = content[0] # first number start address
    machine_code = content[1:] # rest of file
    
    assembly_code = []
    labels = {start_address: "START"}

    # pass 1: identify labels, parse out the jumping
    pc = 0
    while pc < len(machine_code):
        op = machine_code[pc]
        if op in [ops.index('JP'), ops.index('JPNZ'), ops.index('JPZ'), ops.index('CALL')]:
            addr = machine_code[pc + 1]
            if addr not in labels:
                labels[addr] = f"L{addr}" # helpful numbering
        pc += 1 + ary[op]

    # pass 2: assembly
    pc = 0
    while pc < len(machine_code):
        if pc in labels:
            assembly_code.append(f"{labels[pc]}:")

        op = machine_code[pc]
        instruction = ops[op]
        opt = '{:03}'.format(op)
        if ary[op] == 1:
            operand = machine_code[pc + 1]
            opert = '{:03}'.format(operand)
            if op in [ops.index('JP'), ops.index('JPNZ'), ops.index('JPZ'), ops.index('CALL')] and operand in labels:
                assembly_code.append(f"\t{instruction} :{labels[operand]}\t# {opt} {opert}")
            else:
                assembly_code.append(f"\t{instruction} {operand}\t\t# {opt} {opert}")
            pc += 2
        else:
            assembly_code.append(f"\t{instruction}\t\t# {opt}")
            pc += 1

    if verbose == 1:
        print(assembly_code)

    with open(outputfile, "w") as f:
        for line in assembly_code:
            f.write(line + "\n")

def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('disasm.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: disasm.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if verbose == 1:
        print("disassembling ..")    
    content = read_binary_file(inputfile)
    disassemble(content, outputfile, verbose)
    if verbose == 1:
        print("done.")

if __name__ == "__main__":
   main(sys.argv[1:])