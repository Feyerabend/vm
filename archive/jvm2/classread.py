# reading a given sample Java class
# prints a "raw" representation of some content
# classread.py

import struct
import getopt
import sys
import io

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
def parse_header(f):
    header = []
    magic = struct.unpack('!I', f.read(4))
    minor, major = struct.unpack('!HH', f.read(4))
    header.append(Header(magic, minor, major))
    return header

# constant pool tags
TAG_TEXT = {7: 'CLASS',
            9: 'FIELDREF',
            10: 'METHODREF',
            11: 'INTERFACEMETHODREF',
            8: 'STRING',
            3: 'INTEGER',
            4: 'FLOAT',
            5: 'LONG',
            6: 'DOUBLE',
            12: 'NAMEANDTYPE',
            1: 'UTF8',
            15: 'METHODHANDLE',
            16: 'METHODTYPE',
            18: 'INVOKEDYNAMIC'}

# cp_info {
#    u1 tag;
#    u1 info[];
# }
class ConstantPool():
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value
    def __str__(self) -> str:
        tag = TAG_TEXT[self.tag]
        return f"{tag:>20}:  {self.value}"

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
            i += 1  # Doubles take up two entries in the constant pool

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


# Flag              Name	Value	Interpretation
# ACC_PUBLIC	    0x0001	Declared public; may be accessed from outside its package.
# ACC_FINAL 	    0x0010	Declared final; no subclasses allowed.
# ACC_SUPER 	    0x0020	Treat superclass methods specially when invoked by the invokespecial instruction.
# ACC_INTERFACE	    0x0200	Is an interface, not a class.
# ACC_ABSTRACT	    0x0400	Declared abstract; must not be instantiated.
# ACC_SYNTHETIC	    0x1000	Declared synthetic; not present in the source code.
# ACC_ANNOTATION	0x2000	Declared as an annotation type.
# ACC_ENUM	        0x4000	Declared as an enum type.

class Access():
    def __init__(self, flags):
        self.flags = flags
    def __str__(self) -> str:
        return f"flags: 0x{'{:04x}'.format(self.flags[0])}"

def parse_flags(f):
    access_flags = struct.unpack('!H', f.read(2))
    access = Access(access_flags)
    return access


# this class name
class This():
    def __init__(self, class_name):
        self.class_name = class_name
    def __str__(self) -> str:
        return f"this class name: {self.class_name}"

def parse_this(f, constant_pool):
    this_class = struct.unpack('!H', f.read(2))
    ref = constant_pool[this_class[0] - 1].value
    class_name = constant_pool[ref - 1].value
    this = This(class_name)
    return this

# the super class name
class Super():
    def __init__(self, super_name):
        self.super_name = super_name
    def __str__(self) -> str:
        return f"super class name: {self.super_name}"

def parse_super(f, constant_pool):
    super_class = struct.unpack('!H', f.read(2))
    ref = constant_pool[super_class[0] - 1].value
    super_name = constant_pool[ref - 1].value
    super = Super(super_name)
    return super


# interfaces
class Interface():
    def __init__(self, interface_name):
        self.interface_name = interface_name
    def __str__(self) -> str:
        return f"interface name: {self.interface_name}"

def parse_interfaces(f, constant_pool):
    interfaces = []
    interface_count = struct.unpack("!H", f.read(2))[0]
    for _ in range(interface_count):
        interface_index = struct.unpack("!H", f.read(2))[0]
        ref = constant_pool[interface_index - 1].value
        name = constant_pool[ref - 1].value
        interfaces.append(Interface(name))
    return interfaces



# attribute_info {
#    u2 attribute_name_length;
#    u4 attribute_length;
#    u1 info[attribute_length];
# }

class AttributeInfo():
    def __init__(self, name, info):
        self.name = name
        self.info = info
    def __str__(self) -> str:
        return f"attribute: {self.name}: {self.info}"

def parse_attribute_info(f, constant_pool):
    attribute_name_length = struct.unpack("!H", f.read(2))[0]
    length = struct.unpack("!I", f.read(4))[0]
    info = f.read(length)
    name = constant_pool[attribute_name_length - 1].value
    attr = AttributeInfo(name, info)
    return attr



# field_info {
#    u2             access_flags;
#    u2             name_index;
#    u2             descriptor_index;
#    u2             attributes_count;
#    attribute_info attributes[attributes_count];
# }

class Field():
    def __init__(self, access_flags, name, desc, attributes):
        self.access_flags = access_flags
        self.name = name
        self.desc = desc
        self.attributes = attributes
    def __str__(self) -> str:
        return f"field: 0x{'{:04x}'.format(self.access_flags)} {self.name} {self.desc}"

def parse_fields(f, constant_pool):
    fields = []
    field_count = struct.unpack("!H", f.read(2))[0]
    for _ in range(field_count):
        access_flags = struct.unpack("!H", f.read(2))[0]
        name_index = struct.unpack("!H", f.read(2))[0]
        descriptor_index = struct.unpack("!H", f.read(2))[0]

        attributes = []
        attributes_count = struct.unpack("!H", f.read(2))[0]
        for _ in range(attributes_count):
            attr = parse_attribute_info(f, constant_pool)
            attributes.append(attr)

        name = constant_pool[name_index - 1].value
        desc = constant_pool[descriptor_index - 1].value
        field = Field(access_flags, name, desc, attributes)
        fields.append(field)
    return fields


# method_info {
#    u2             access_flags;
#    u2             name_index;
#    u2             descriptor_index;
#    u2             attributes_count;
#    attribute_info attributes[attributes_count];
# }

class Method():
    def __init__(self, access_flags, name, desc, attributes):
        self.access_flags = access_flags
        self.name = name
        self.desc = desc
        self.attributes = attributes
    def __str__(self) -> str:
        return f"method: 0x{'{:04x}'.format(self.access_flags)} {self.name} {self.desc}"

def parse_methods(f, constant_pool):
    methods = []
    method_count = struct.unpack("!H", f.read(2))[0]
    for i in range(method_count):
        access_flags = struct.unpack("!H", f.read(2))[0]
        name_index = struct.unpack("!H", f.read(2))[0]
        descriptor_index = struct.unpack("!H", f.read(2))[0]

        attributes = []
        attributes_count = struct.unpack("!H", f.read(2))[0]
        for _ in range(attributes_count):
            attr = parse_attribute_info(f, constant_pool)
            attributes.append(attr)

        name = constant_pool[name_index - 1].value
        desc = constant_pool[descriptor_index - 1].value
        method = Method(access_flags, name, desc, attributes)
        methods.append(method)
    return methods


# attribute_info {
#    u2 attribute_name_index;
#    u4 attribute_length;
#    u1 info[attribute_length];
# }

class Attribute():
    def __init__(self, name, attribute_bytes):
        self.name = name
        self.attribute_bytes = attribute_bytes
    def __str__(self) -> str:
        return f"attribute: {self.name} {self.attribute_bytes}"

def parse_attributes(f, constant_pool):
    attributes = []
    attribute_count = struct.unpack("!H", f.read(2))[0]
    for _ in range(attribute_count):
        name_index = struct.unpack("!H", f.read(2))[0]
        attribute_length = struct.unpack("!I", f.read(4))[0]
        attribute_bytes = f.read(attribute_length)
        name = constant_pool[name_index - 1].value 
        attribute = Attribute(name, attribute_bytes)
        attributes.append(attribute)
    return attributes


