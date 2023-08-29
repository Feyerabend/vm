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