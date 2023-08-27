# reading sample Java class
# classread-sample.py

import struct

with open("Sample.class", "rb") as f:
    magic = f.read(4)
    if magic != b"\xCA\xFE\xBA\xBE":
        raise ValueError("Invalid class file")
    minor_version = struct.unpack("<H", f.read(2))[0]
    major_version = struct.unpack("<H", f.read(2))[0]
    print(f"version: {major_version}.{minor_version}")

    constant_pool_count = struct.unpack("<H", f.read(2))[0]
    print(f"constant pool count: {constant_pool_count}")
    constant_pool = f.read()
    print("constant pool:")
    for i, entry in enumerate(constant_pool):
        print(f"  > {i+1}: {entry}")
