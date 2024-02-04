# a very, very, very limited interpreter
# that shows the ideas of a Java interpreter
# it can not parse and run more than a simple
# "hello world" program
# mostly inspired from https://github.com/phoro3/python_jvm

import io
import importlib
from classread import *


class Parser():

    # parse a class file
    def readclass(self, inputfile):
        with open(inputfile, "rb") as f:

            # ClassFile {
            #    u4             magic;
            #    u2             minor_version;
            #    u2             major_version;
            #     u2             constant_pool_count;
            #    cp_info        constant_pool[constant_pool_count-1];
            #    u2             access_flags;
            #    u2             this_class;
            #    u2             super_class;
            #    u2             interfaces_count;
            #    u2             interfaces[interfaces_count];
            #    u2             fields_count;
            #    field_info     fields[fields_count];
            #    u2             methods_count;
            #    method_info    methods[methods_count];
            #    u2             attributes_count;
            #    attribute_info attributes[attributes_count];
            # }

            self.header =            parse_header(f)
            self.constant_pool =     parse_constant_pool(f)
            self.flags =             parse_flags(f)
            self.this =              parse_this(f, self.constant_pool)
            self.super =             parse_super(f, self.constant_pool)
            self.interfaces =        parse_interfaces(f, self.constant_pool)
            self.fields =            parse_fields(f, self.constant_pool)
            self.methods =           parse_methods(f, self.constant_pool)
            self.attributes =        parse_attributes(f, self.constant_pool)
            f.close()

    # method
    def get_method(self, method_name):
        if self.methods:
            for _, m in enumerate(self.methods):
                if m.name == method_name:
                    return m
        return None

    # attr of method
    def get_attr_of_method(self, method_name, attr_name):
        method = self.get_method(method_name)
        if method:
            for _, m in enumerate(method.attributes):
                if (m.name == attr_name):
                    return m.info
        return None

    # code attr of method
    def get_code_of_method(self, method_name):
        codeattr = self.get_attr_of_method(method_name, 'Code')
        if codeattr:
            t = io.BytesIO(codeattr)
            max_stack = struct.unpack('!H', t.read(2))[0] # not used
            max_locals = struct.unpack('!H', t.read(2))[0] # not used
            code_len = struct.unpack('!I', t.read(4))[0]
            code = t.read(code_len)
            return (max_stack, max_locals, code)
        return None


class Interpret():

    def __init__(self, codes, constant_pool):
        self.instructions = {
            18:     self.instr_ldc,
            177:    self.instr_return,
            178:    self.instr_getstatic,
            182:    self.instr_invokevirtual
        }
        self.pc = 0
        self.stack = []

        # tuple decode
        self.max_stack = int(codes[0]) # not used
        self.max_locals = int(codes[1]) # not used
        self.code = list(codes[2])

        # need the pool
        self.pool = constant_pool

    # get the code, advance one step in pc,
    # then return the code value
    def advance(self):
        data = self.code[self.pc]
        self.pc += 1
        return data

    # loop until end of code
    def run(self):
        clen = len(self.code)
        while self.pc < clen:
            op = self.advance()
            self.instructions[op]()

    def instr_getstatic(self):
        index = self.advance() << 8 | self.advance()

        field_ref = self.pool[index - 1]

        class_index = field_ref.value[0]
        class_pointer = self.pool[class_index - 1]
        class_name = self.pool[class_pointer.value - 1].value
        class_name = class_name.replace('/', '.')

        name_and_type_index = field_ref.value[1]
        name_and_type = self.pool[name_and_type_index - 1].value
        name_index = name_and_type[0]
        name = self.pool[name_index - 1].value

        target_class = importlib.import_module(class_name)
        target_field = getattr(target_class, name)
        self.stack.append(target_field)

    def instr_invokevirtual(self):
        index = self.advance() << 8 | self.advance()

        method_ref = self.pool[index - 1]

        name_and_type = method_ref.value[1]
        name_ref = self.pool[name_and_type - 1].value[0]
        type_ref = self.pool[name_and_type - 1].value[1]

        name = self.pool[name_ref - 1].value
        typee = self.pool[type_ref - 1].value

        arg_num = len(typee.split(';')) - 1
        args = [self.stack.pop() for _ in range(arg_num)]
        args.reverse()

        target_method = getattr(self.stack.pop(), name)
        target_method(*args)

    def instr_ldc(self):
        index = self.advance()
        string_ref = self.pool[index - 1].value
        string = self.pool[string_ref - 1].value
        self.stack.append(string)

    def instr_return(self):
        return

# 
def main(argv):
    inputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:",["ifile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: main.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    if verbose == 1:
        print("reading ..")
    parser = Parser()
    parser.readclass(inputfile)

    if verbose == 1:
        print("search for 'main' ..")
    codes = parser.get_code_of_method('main')
    if verbose == 1:
        print("code list =", list(codes[2]))
    pool = parser.constant_pool

    if verbose == 1:
        print("interpret ..")
    interpret = Interpret(codes, pool)
    interpret.run()

    if verbose == 1:
        print("done.")


if __name__ == "__main__":
   main(sys.argv[1:])
