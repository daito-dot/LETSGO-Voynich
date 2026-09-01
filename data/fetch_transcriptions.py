#!/usr/bin/env python3
"""Fetch the third-party Voynich transcriptions used by this repository and
verify them against the frozen identities recorded in the experiments.

Files are downloaded from voynich.nu into the target directory. They are
third-party material and must not be committed to this repository.

usage: python3 data/fetch_transcriptions.py TARGET_DIR [ZL3b IT2a GC2a ...]
"""
from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

BASE = "https://www.voynich.nu/data/"
EXPECTED = {
    # label: (filename, git blob sha1, sha256, bytes)
    "ZL3b": ("ZL3b-n.txt", "2a4533ab9bdfa85db9bad602d590978953055df1",
             "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc", 411671),
    "IT2a": ("IT2a-n.txt", "4d6d3f2537b1f507a257529b49c94af7d6e03446",
             "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5", 342104),
    "GC2a": ("GC2a-n.txt", "8417a644fbd9c11cdaf85224f29cafee9ba1bdb0",
             "b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f", 314916),
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    target = Path(argv[1])
    target.mkdir(parents=True, exist_ok=True)
    labels = argv[2:] or list(EXPECTED)
    ok = True
    for label in labels:
        name, blob, sha, size = EXPECTED[label]
        path = target / name
        if not path.exists():
            with urllib.request.urlopen(BASE + name, timeout=120) as r:
                path.write_bytes(r.read())
        data = path.read_bytes()
        got = (git_blob_sha1(data), hashlib.sha256(data).hexdigest(), len(data))
        good = got == (blob, sha, size)
        ok &= good
        print(f"{label:5s} {name:12s} {'OK ' if good else 'MISMATCH'} blob={got[0]} sha256={got[1]} bytes={got[2]}")
    if not ok:
        raise SystemExit("identity mismatch: do not use these files for frozen experiments")


if __name__ == "__main__":
    main(sys.argv)
