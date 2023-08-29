# reading sample Java class
# classread-sample.py

import struct

with open("Sample.class", "rb") as f:
    # CAFEBABE and version
    magic = struct.unpack('!I', cf.read(4))
    minor, major = struct.unpack('!HH', cf.read(4))
    print(f"version: {major}.{minor}")
