#!/usr/bin/env python3
"""Restore the SHA-256 RUP source file from the lossless GitHub upload encoding.

No network or third-party modules. Verifies original size and SHA256 before
atomically replacing a previous local copy. Does not change the compressed source.
"""
import hashlib
import lzma
import os
from pathlib import Path
import tempfile

DIRECTORY = Path(__file__).resolve().parent
SOURCE = DIRECTORY / "boundary.rup.jsonl.xz"
TARGET = DIRECTORY / "boundary.rup.jsonl"
EXPECTED_BYTES = 12_444_726
EXPECTED_SHA256 = "cd1845cdde5fca010b4b8557bcb27947eb5aef50b45856619cce7d54608540c5"

def verify_file(path):
    digest = hashlib.sha256()
    length = 0
    with path.open("rb") as inp:
        while chunk := inp.read(1024 * 1024):
            digest.update(chunk)
            length += len(chunk)
    return length == EXPECTED_BYTES and digest.hexdigest() == EXPECTED_SHA256

def main():
    if TARGET.exists() and verify_file(TARGET):
        print("PASS: original evidence already restored and verified")
        return
    fd, name = tempfile.mkstemp(prefix=".boundary-rup-", suffix=".tmp", dir=DIRECTORY)
    try:
        digest = hashlib.sha256()
        n = 0
        with os.fdopen(fd, "wb") as out, lzma.open(SOURCE, "rb") as inp:
            while chunk := inp.read(1024 * 1024):
                out.write(chunk)
                digest.update(chunk)
                n += len(chunk)
        if n != EXPECTED_BYTES or digest.hexdigest() != EXPECTED_SHA256:
            raise ValueError("decoded evidence does not match frozen SHA256 and size")
        os.replace(name, TARGET)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    assert verify_file(TARGET)
    print("PASS: boundary.rup.jsonl restored; SHA256 and size verified")

if __name__ == "__main__":
    main()
