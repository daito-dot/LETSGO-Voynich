#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import platform
import sys
import urllib.request
import zlib
from pathlib import Path

PINNED_COMMIT = "370cbcd448eb7daf32f21a6be560b70e0b33c4e3"
PINNED_BLOB_SHA1 = "7dcb3a2d4cc3b48b6283dd46870bfeb78f88aac9"
EXPECTED_BYTES = 1115394
URL = f"https://raw.githubusercontent.com/karpathy/char-rnn/{PINNED_COMMIT}/data/tinyshakespeare/input.txt"
HERE = Path(__file__).resolve().parent


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def main() -> None:
    # P0 scientific firewall: this executable has no Voynich input path or import.
    with urllib.request.urlopen(URL, timeout=60) as response:
        plaintext = response.read()
    if len(plaintext) != EXPECTED_BYTES:
        raise RuntimeError(f"plaintext byte count mismatch: {len(plaintext)}")
    blob = git_blob_sha1(plaintext)
    if blob != PINNED_BLOB_SHA1:
        raise RuntimeError(f"Git blob mismatch: {blob}")

    compressed = zlib.compress(plaintext, level=9)
    if zlib.decompress(compressed) != plaintext:
        raise RuntimeError("zlib round-trip failed")

    payload_b64 = base64.b64encode(compressed).decode("ascii") + "\n"
    (HERE / "P0_PAYLOAD.zlib.b64").write_text(payload_b64, encoding="ascii")

    result = {
        "schema": "issue221-p0-v1",
        "issue": 221,
        "stage": "P0_TARGET_BLIND_EXTERNAL_PAYLOAD_FREEZE",
        "voynich_corpus_accessed": False,
        "target_probability_accessed": False,
        "r2_score_computed": False,
        "source": {
            "repository": "karpathy/char-rnn",
            "path": "data/tinyshakespeare/input.txt",
            "commit": PINNED_COMMIT,
            "git_blob_sha1": blob,
            "url": URL,
            "bytes": len(plaintext),
            "sha256": hashlib.sha256(plaintext).hexdigest(),
        },
        "compression": {
            "algorithm": "zlib.compress / DEFLATE",
            "level": 9,
            "bytes": len(compressed),
            "bits": 8 * len(compressed),
            "sha256": hashlib.sha256(compressed).hexdigest(),
            "base64_sha256": hashlib.sha256(payload_b64.encode("ascii")).hexdigest(),
            "roundtrip_exact": True,
        },
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "zlib_compile": zlib.ZLIB_VERSION,
            "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION,
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    result["canonical_without_self_hash_sha256"] = hashlib.sha256(canonical).hexdigest()
    (HERE / "P0_PAYLOAD.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
