"""
Reading and writing .vm files, as described in ch05-files/FORMAT.md.
"""

import struct

MAGIC = b"SVM"
VERSION = 1
MAX_CODE = 65536


class FormatError(Exception):
    pass


def write(path, code):
    with open(path, "wb") as f:
        f.write(MAGIC + bytes([VERSION]))
        f.write(struct.pack("<i", len(code)))
        f.write(struct.pack(f"<{len(code)}i", *code))


def read(path):
    """Return the code in a .vm file, making the same checks as the machine."""
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 8:
        raise FormatError("too short to be a program")
    if data[:3] != MAGIC:
        raise FormatError("not a program (wrong magic number)")
    if data[3] != VERSION:
        raise FormatError("unknown format version")
    (n,) = struct.unpack("<i", data[4:8])
    if not 1 <= n <= MAX_CODE:
        raise FormatError("bad code length")
    if len(data) < 8 + 4 * n:
        raise FormatError("code ends early")
    if len(data) > 8 + 4 * n:
        raise FormatError("extra bytes after the code")
    return list(struct.unpack(f"<{n}i", data[8:]))
