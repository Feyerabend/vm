#!/usr/bin/env python3
"""
Write files that are broken in every way the loader checks for.

    usage: badfiles.py directory
"""

import os
import struct
import sys

GOOD = b"SVM\x01" + struct.pack("<i", 1) + struct.pack("<i", 0)

BROKEN = {
    "empty": b"",
    "short": b"SVM\x01\x01",
    "magic": b"ELF\x01" + GOOD[4:],
    "version": b"SVM\x02" + GOOD[4:],
    "zero": b"SVM\x01" + struct.pack("<i", 0),
    "negative": b"SVM\x01" + struct.pack("<i", -1),
    "huge": b"SVM\x01" + struct.pack("<i", 1 << 30),
    "truncated": b"SVM\x01" + struct.pack("<i", 2) + struct.pack("<i", 0),
    "trailing": GOOD + b"\x00",
}


def main():
    directory = sys.argv[1]
    os.makedirs(directory, exist_ok=True)
    for name, data in BROKEN.items():
        with open(os.path.join(directory, name + ".vm"), "wb") as f:
            f.write(data)


if __name__ == "__main__":
    main()
