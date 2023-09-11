# reading a given sample Java class
# classread-constant-pool.py

import struct
import getopt
import sys

# see the specification at e.g.
# https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html

class Header():
    def __init__(self, magic, minor, major):
        self.magic = magic
        self.minor = minor
        self.major = major
    def __str__(self) -> str:
        return f"version: {self.major}.{self.minor}"

# CAFEBABE and version
def parse_header(cf):
    header = []
    magic = struct.unpack('!I', cf.read(4))
    minor, major = struct.unpack('!HH', cf.read(4))
    header.append(Header(magic, minor, major))
    return header


# cp_info {
#    u1 tag;
#    u1 info[];
# }
class ConstantPool():
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value
    def __str__(self) -> str:
        return f"{self.tag:>2}: {self.value}"


def parse_constant_pool(f):
    constant_pool = []
    constant_pool_count = struct.unpack("!H", f.read(2))[0]

    for i in range(1, constant_pool_count):
        # read a tag
        tag = struct.unpack("!B", f.read(1))[0]

        # CONSTANT_Utf8_info {
        #    u1 tag;
        #    u2 length;
        #    u1 bytes[length];
        # }
        if tag == 1:
            length = struct.unpack("!H", f.read(2))[0]
            value = struct.unpack('!{}s'.format(length), f.read(length))[0].decode('utf-8')
            constant_pool.append(ConstantPool(tag, value))

        # CONSTANT_Integer_info {
        #    u1 tag;
        #    u4 bytes;
        # }
        elif tag == 3:
            value = struct.unpack("!i", f.read(4))[0]
            constant_pool.append(ConstantPool(tag, value))


        # CONSTANT_Float_info {
        #    u1 tag;
        #    u4 bytes;
        # }
        elif tag == 4:
            value = struct.unpack("!f", f.read(4))[0]
            constant_pool.append(ConstantPool(tag, value))

        # CONSTANT_Long_info {
        #    u1 tag;
        #    u4 high_bytes;
        #    u4 low_bytes;
        # }
        elif tag == 5:
            value = struct.unpack("!q", f.read(8))[0]
            constant_pool.append(ConstantPool(tag, value))
            i += 1  # skip as "long" extend over 2 tags

        # CONSTANT_Double_info {
        #    u1 tag;
        #    u4 high_bytes;
        #    u4 low_bytes;
        # }
        elif tag == 6:
            value = struct.unpack("!d", f.read(8))[0]
            constant_pool.append(ConstantPool(tag, value))
            i += 1  # skip as "double" extend over 2 tags

        # Class
        #   u1 tag;
        #   u2 index;
        elif tag == 7:  # Class
            index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, index))

        # CONSTANT_String_info {
        #    u1 tag;
        #    u2 string_index;
        # }
        elif tag == 8:
            index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, index))

        # CONSTANT_Fieldref_info {
        #    u1 tag;
        #    u2 class_index;
        #    u2 name_and_type_index;
        # }
        elif tag == 9:
            class_index = struct.unpack("!H", f.read(2))[0]
            name_and_type_index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, (class_index, name_and_type_index)))

        # CONSTANT_Methodref_info {
        #    u1 tag;
        #    u2 class_index;
        #    u2 name_and_type_index;
        # }
        elif tag == 10:
            class_index = struct.unpack("!H", f.read(2))[0]
            name_and_type_index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, (class_index, name_and_type_index)))

        # CONSTANT_InterfaceMethodref_info {
        #    u1 tag;
        #    u2 class_index;
        #    u2 name_and_type_index;
        # }
        elif tag == 11:
            class_index = struct.unpack("!H", f.read(2))[0]
            name_and_type_index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, (class_index, name_and_type_index)))

        # CONSTANT_NameAndType_info {
        #    u1 tag;
        #    u2 name_index;
        #    u2 descriptor_index;
        # }
        elif tag == 12:
            name_index = struct.unpack("!H", f.read(2))[0]
            descriptor_index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, (name_index, descriptor_index)))

        # CONSTANT_MethodHandle_info {
        #    u1 tag;
        #    u1 reference_kind;
        #    u2 reference_index;
        # }
        elif tag == 15:
            reference_kind = struct.unpack("!B", f.read(1))[0]
            reference_index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, (reference_kind, reference_index)))

        # CONSTANT_MethodType_info {
        #    u1 tag;
        #    u2 descriptor_index;
        # }
        elif tag == 16:
            descriptor_index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, descriptor_index))

        # CONSTANT_InvokeDynamic_info {
        #    u1 tag;
        #    u2 bootstrap_method_attr_index;
        #    u2 name_and_type_index;
        # }
        elif tag == 18:
            bootstrap_method_attr_index = struct.unpack("!H", f.read(2))[0]
            name_and_type_index = struct.unpack("!H", f.read(2))[0]
            constant_pool.append(ConstantPool(tag, (bootstrap_method_attr_index, name_and_type_index)))

    return constant_pool


# 
def readclass(inputfile, verbose):

    with open(inputfile, "rb") as cf:

        # partial impl. marked by <--
        # ClassFile {
        #    u4             magic;                                  <--
        #    u2             minor_version;                          <--
        #    u2             major_version;                          <--
        #    u2             constant_pool_count;                    <--
        #    cp_info        constant_pool[constant_pool_count-1];   <--
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

        h = parse_header(cf)
        cp = parse_constant_pool(cf)
        cf.close()

        if verbose == 1:
            for i, v1 in enumerate(h):
                print(f"{v1}")
            for i, v2 in enumerate(cp):
                print(f"#{i+1:0>{2}} {v2}")

# 
def main(argv):
    inputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:",["ifile="])
    except getopt.GetoptError:
        print('classread-constant-pool.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: classread-constant-pool.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    if verbose == 1:
        print("reading ..")
    readclass(inputfile, verbose)
    if verbose == 1:
        print("done.")


if __name__ == "__main__":
   main(sys.argv[1:])
