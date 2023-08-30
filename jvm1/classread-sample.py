# reading sample Java class
# classread-sample.py

import struct

with open("Sample.class", "rb") as cf:
    # cafebabe
    magic = struct.unpack('!I', cf.read(4))
    print(f"magic: {hex(magic[0])}")
    # version
    minor, major = struct.unpack('!HH', cf.read(4))
    print(f"version: {major}.{minor}")
