#!/usr/bin/env python3
"""Issue #84 Phase C — frozen historical genre controls.

Scientific authority:
  experiments/cross-linguistic-baselines/PLAN_C.md
  experiments/cross-linguistic-baselines/REPORT_C0_SOURCE_AUDIT.md

Usage:
  python experiments/cross-linguistic-baselines/phase84c.py CACHE_DIR OUT.json
  python experiments/cross-linguistic-baselines/phase84c.py CACHE_DIR --preflight

`--preflight` performs source fetch/hash/extraction/count checks only and MUST NOT
call Phase-A Q1/Q2 scoring.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import phase84a as a84  # noqa: E402

PHASE = "84C"
CAP = 32570
PHASE_A_SHA256 = "86d18560b5999836b7c0d22fa9c3d8dbfd9f11ba246613fd0c2527d5ed5ffe1c"
VOYNICH_LABELS = ("ZL3b", "IT2a", "VT0e", "RF1b", "GC2a", "CD2a", "FG2a")
PRIMARY_KEYS = ("MI1", "z1_2", "z21_40")
WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)
UA = {"User-Agent": "LETSGO-Voynich-Issue84-PhaseC/1.0"}

SOURCES = {
    "C-REC-1": {
        "txt_url": "https://www.gutenberg.org/cache/epub/8102/pg8102.txt",
        "txt_sha256": "87d1a2819214526a7410c8b864f39a217e9bf93816a26736e01e8df25447c7eb",
    },
    "C-REC-2": {
        "txt_url": "https://archive.org/download/twofifteenthcent00aust/twofifteenthcent00aust_djvu.txt",
        "txt_sha256": "6ffbad0b4b0b09e6c41d35c3edb019df42ecc649e0ef24e31bbd9b01d7d4bb6b",
        "xml_url": "https://archive.org/download/twofifteenthcent00aust/twofifteenthcent00aust_djvu.xml",
        "xml_sha256": "15cb66dbd33d123f40a79ec3797702f3b866fcc1b1f92121cb3833896e6acb64",
    },
    "C-HERB-1": {
        "txt_url": "https://archive.org/download/deviribusherbaru00mace/deviribusherbaru00mace_djvu.txt",
        "txt_sha256": "1baed87fec67e0c7d785fc7c92452bba8185f03e18b1b02b6b0378717161d8e3",
        "xml_url": "https://archive.org/download/deviribusherbaru00mace/deviribusherbaru00mace_djvu.xml",
        "xml_sha256": "eb97444b606bb45b17d36fa3fa3635735c8eeb25537e78721105df3ddd6d1792",
        "c0_status": "FAIL_NOT_SCORED",
    },
    "C-MED-1": {
        "txt_url": "https://archive.org/download/leechdomswortcun01cock/leechdomswortcun01cock_djvu.txt",
        "txt_sha256": "47797f08159dee1e1b94d72b909fd9c9d03a057fd539f3e74ac7c88af8b92a1c",
        "xml_url": "https://archive.org/download/leechdomswortcun01cock/leechdomswortcun01cock_djvu.xml",
        "xml_sha256": "df7eb45022acdc1bc822713d46f6b7a04c6350cef9743c7698db2bef3ea17fd5",
    },
    "C-ACC-1": {
        "txt_url": "https://archive.org/download/cu31924027939820/cu31924027939820_djvu.txt",
        "txt_sha256": "0394af1ff19c72736be92e39bb459287c6290909ce85b8dbe65752d055b238e6",
        "xml_url": "https://archive.org/download/cu31924027939820/cu31924027939820_djvu.xml",
        "xml_sha256": "21124d8e190191cfa3ae1da52d50742e1af97d14a462545332e4c51739329036",
    },
    "C-ACC-2": {
        "txt_url": "https://archive.org/download/cu31924027939861/cu31924027939861_djvu.txt",
        "txt_sha256": "01b3c016358f12e1e7137ce978dd40f9f34085bb176c22bad1dde6b72ac3e261",
        "xml_url": "https://archive.org/download/cu31924027939861/cu31924027939861_djvu.xml",
        "xml_sha256": "9e08a2dd2cab4273d3e5a2f90b69e3f77aa4f57db15556bd15b505435dc47552",
    },
    "C-LIT-1": {
        "txt_url": "https://archive.org/download/manualeetp00cath/manualeetp00cath_djvu.txt",
        "txt_sha256": "5724b4e59b8ece94252c7197ffb19f08651e152273f3086ec80553916b1fd059",
        "xml_url": "https://archive.org/download/manualeetp00cath/manualeetp00cath_djvu.xml",
        "xml_sha256": "c99a531fff3cf2de1210f301066ff9853dd8f5eeb6735922eb278587defac1ee",
    },
}

EXPECTED_COUNTS = {
    "REC1_FormeOfCury": 11850,
    "REC2_Harl279": 26210,
    "REC2_Harl4016": 19334,
    "MED1_Herbarium_OE": 25012,
    "ACC1_Countess1265": 22109,
    "ACC1_Executors1291": 9588,
    "ACC1_Howard1462_69": 147864,
    "ACC2_HouseholdBook1": 57203,
    "ACC2_HouseholdBook2": 69847,
    "LIT1_YorkManualProcessional": 41689,
}

GENRES = {
    "GENRE_RECIPE": ("REC1_FormeOfCury", "REC2_Harl279", "REC2_Harl4016"),
    "GENRE_MEDICAL": ("MED1_Herbarium_OE",),
    "GENRE_ACCOUNT": (
        "ACC1_Countess1265", "ACC1_Executors1291", "ACC1_Howard1462_69",
        "ACC2_HouseholdBook1", "ACC2_HouseholdBook2",
    ),
    "GENRE_LITURGY": ("LIT1_YorkManualProcessional",),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        if getattr(r, "status", 200) != 200:
            raise RuntimeError(f"HTTP {r.status}: {url}")
        return r.read()


def ensure_source(cache: Path, sid: str, kind: str) -> Path:
    spec = SOURCES[sid]
    key = f"{kind}_url"
    skey = f"{kind}_sha256"
    if key not in spec:
        raise KeyError(f"{sid} has no {kind}")
    ext = ".xml" if kind == "xml" else ".txt"
    path = cache / f"{sid}{ext}"
    if not path.exists() or sha256_file(path) != spec[skey]:
        data = fetch(spec[key])
        if sha256_bytes(data) != spec[skey]:
            raise RuntimeError(f"{sid} {kind} SHA-256 mismatch")
        path.write_bytes(data)
    if sha256_file(path) != spec[skey]:
        raise RuntimeError(f"{sid} cached {kind} SHA-256 mismatch")
    return path


def decode_text(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    raise RuntimeError(f"cannot decode {path}")


def normalize_tokens(text: str) -> List[str]:
    text = unicodedata.normalize("NFC", text).casefold()
    return WORD_RE.findall(text)


def xml_pages(path: Path):
    root = ET.parse(path).getroot()
    return root.findall(".//OBJECT")


def line_record(line):
    words = []
    for wd in line.findall(".//WORD"):
        txt = "".join(wd.itertext()).strip()
        coords = wd.attrib.get("coords") or wd.attrib.get("COORDS") or ""
        if txt and coords:
            words.append((txt, list(map(int, coords.split(",")))))
    if not words:
        return None
    xmin = min(c[0] for _, c in words)
    xmax = max(c[2] for _, c in words)
    ymax = max(c[1] for _, c in words)
    ymin = min(c[3] for _, c in words)
    return {
        "text": " ".join(t for t, _ in words),
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "height": ymax - ymin,
        "mid_y": (ymin + ymax) / 2.0,
    }


def extract_xml_span(pages, start: int, end: int, step: int, lo: float, hi: float, min_height: int | None = None, liturgy_filter: bool = False) -> List[str]:
    lines: List[str] = []
    for pi in range(start, end + 1, step):
        obj = pages[pi]
        height = int(obj.attrib.get("height") or obj.attrib.get("HEIGHT") or 0)
        if height <= 0:
            raise RuntimeError(f"invalid page height at {pi}")
        for line in obj.findall(".//LINE"):
            rec = line_record(line)
            if rec is None:
                continue
            if not (lo * height <= rec["mid_y"] <= hi * height):
                continue
            if min_height is not None and rec["height"] < min_height:
                continue
            text = rec["text"]
            if liturgy_filter:
                wt = WORD_RE.findall(text)
                chars = [c for c in text if not c.isspace()]
                alpha_n = sum(c.isalpha() for c in chars)
                alpha_fraction = alpha_n / max(1, len(chars))
                hyphen_density = text.count("-") / max(1, alpha_n)
                one_char_fraction = sum(len(t) == 1 for t in wt) / max(1, len(wt))
                if len(wt) < 3:
                    continue
                if alpha_fraction < 0.70:
                    continue
                if hyphen_density > 0.03:
                    continue
                if one_char_fraction > 0.25:
                    continue
            lines.append(text)
    return lines


def extract_documents(cache: Path, verify_all_source_hashes: bool = True) -> Dict[str, List[str]]:
    cache.mkdir(parents=True, exist_ok=True)
    if verify_all_source_hashes:
        # Assert both C0 TXT and XML authorities, including excluded Macer.
        for sid, spec in SOURCES.items():
            ensure_source(cache, sid, "txt")
            if "xml_url" in spec:
                ensure_source(cache, sid, "xml")

    docs: Dict[str, List[str]] = {}

    # C-REC-1
    rec1 = decode_text(ensure_source(cache, "C-REC-1", "txt"))
    start = rec1.index("FOR TO MAKE GRONDEN BENES [1]. I.")
    end = rec1.index("[1]XPLICIT.", start)
    paras = re.split(r"\n\s*\n", rec1[start:end])
    body = "\n\n".join(p for p in paras if not re.match(r"^\s*\[\d+\]", p))
    docs["REC1_FormeOfCury"] = normalize_tokens(body)

    # C-REC-2
    pages = xml_pages(ensure_source(cache, "C-REC-2", "xml"))
    docs["REC2_Harl279"] = normalize_tokens("\n".join(extract_xml_span(pages, 24, 83, 1, 0.10, 0.90)))
    docs["REC2_Harl4016"] = normalize_tokens("\n".join(extract_xml_span(pages, 86, 126, 1, 0.10, 0.90)))

    # C-MED-1
    pages = xml_pages(ensure_source(cache, "C-MED-1", "xml"))
    docs["MED1_Herbarium_OE"] = normalize_tokens("\n".join(extract_xml_span(pages, 123, 445, 2, 0.12, 0.68)))

    # C-ACC-1
    pages = xml_pages(ensure_source(cache, "C-ACC-1", "xml"))
    docs["ACC1_Countess1265"] = normalize_tokens("\n".join(extract_xml_span(pages, 112, 194, 1, 0.12, 0.76, min_height=40)))
    docs["ACC1_Executors1291"] = normalize_tokens("\n".join(extract_xml_span(pages, 202, 248, 1, 0.12, 0.76, min_height=40)))
    docs["ACC1_Howard1462_69"] = normalize_tokens("\n".join(extract_xml_span(pages, 258, 730, 1, 0.12, 0.76, min_height=40)))

    # C-ACC-2
    pages = xml_pages(ensure_source(cache, "C-ACC-2", "xml"))
    docs["ACC2_HouseholdBook1"] = normalize_tokens("\n".join(extract_xml_span(pages, 40, 276, 1, 0.12, 0.76, min_height=40)))
    docs["ACC2_HouseholdBook2"] = normalize_tokens("\n".join(extract_xml_span(pages, 320, 559, 1, 0.12, 0.76, min_height=40)))

    # C-LIT-1
    pages = xml_pages(ensure_source(cache, "C-LIT-1", "xml"))
    docs["LIT1_YorkManualProcessional"] = normalize_tokens("\n".join(extract_xml_span(pages, 34, 235, 1, 0.10, 0.85, liturgy_filter=True)))

    if set(docs) != set(EXPECTED_COUNTS):
        raise RuntimeError(f"document set mismatch: {sorted(docs)}")
    for name, expected in EXPECTED_COUNTS.items():
        actual = len(docs[name])
        if actual != expected:
            raise RuntimeError(f"{name}: C0 extraction token mismatch {actual} != {expected}")
        if actual < 2000:
            raise RuntimeError(f"{name}: below C0 2,000-token floor")
    if "C-HERB-1" in docs or any("Macer" in k for k in docs):
        raise RuntimeError("C-HERB-1/Macer must remain excluded")
    return docs


def to_unit_docs(tokens_by_name: Dict[str, List[str]]) -> Dict[str, List[Tuple[str, ...]]]:
    return {name: [tuple(t) for t in toks[:CAP]] for name, toks in tokens_by_name.items()}


def target_intervals(phase_a: dict) -> dict:
    vals = {k: [] for k in PRIMARY_KEYS}
    for label in VOYNICH_LABELS:
        if label not in phase_a.get("voynich", {}):
            raise RuntimeError(f"Phase-A target missing {label}")
        v = phase_a["voynich"][label]
        vals["MI1"].append(float(v["Q1"]["d1"]["corrected"]))
        vals["z1_2"].append(float(v["Q2"]["z"][0]))
        vals["z21_40"].append(float(v["Q2"]["z"][4]))
    out = {k: [min(v), max(v)] for k, v in vals.items()}
    expected = {
        "MI1": [0.05287300267140527, 0.11095606169252736],
        "z1_2": [2.7963710506633936, 8.455834173591136],
        "z21_40": [-0.7700738340053305, 3.434624139155326],
    }
    for k in PRIMARY_KEYS:
        if not all(math.isclose(out[k][i], expected[k][i], rel_tol=0, abs_tol=1e-14) for i in (0, 1)):
            raise RuntimeError(f"target interval mismatch for {k}: {out[k]} != {expected[k]}")
    return out


def score_docs(label: str, docs: Sequence[Tuple[str, Sequence[Tuple[str, ...]]]]) -> dict:
    ids, doc_id, V = a84.to_ids(docs)
    q1 = a84.q1(ids, doc_id, label)
    q2 = a84.q2(ids, doc_id, label)
    q3 = a84.q3(docs) if len(docs) >= 2 else None
    return {
        "label": label,
        "n_tokens": int(len(ids)),
        "n_types": int(V),
        "n_docs": len(docs),
        "mean_doc_tokens": float(len(ids) / len(docs)),
        "mean_token_units": float(sum(len(t) for _n, ts in docs for t in ts) / len(ids)),
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
    }


def primary_values(score: dict) -> dict:
    return {
        "MI1": float(score["Q1"]["d1"]["corrected"]),
        "z1_2": float(score["Q2"]["z"][0]),
        "z21_40": float(score["Q2"]["z"][4]),
    }


def interval_distance(x: float, interval: Sequence[float]) -> float:
    lo, hi = map(float, interval)
    if x < lo:
        return float(x - lo)
    if x > hi:
        return float(x - hi)
    return 0.0


def classify(score: dict, intervals: dict) -> dict:
    p = primary_values(score)
    resp = {
        "R_MI": intervals["MI1"][0] <= p["MI1"] <= intervals["MI1"][1],
        "R_SHORT": intervals["z1_2"][0] <= p["z1_2"] <= intervals["z1_2"][1],
        "R_MID": intervals["z21_40"][0] <= p["z21_40"] <= intervals["z21_40"][1],
    }
    n = sum(bool(v) for v in resp.values())
    label = {
        3: "VOYNICH INTER-TOKEN REGIME SOURCE HIT",
        2: "PARTIAL SOURCE HIT (2/3)",
        1: "PARTIAL SOURCE HIT (1/3)",
        0: "NO SOURCE HIT",
    }[n]
    return {
        "primary": p,
        "responsibilities": resp,
        "n_responsibilities_passed": n,
        "signed_distance_to_target_interval": {k: interval_distance(p[k], intervals[k]) for k in PRIMARY_KEYS},
        "classification": label,
    }


def preflight(cache: Path) -> dict:
    docs = extract_documents(cache, verify_all_source_hashes=True)
    capped = {name: min(len(toks), CAP) for name, toks in docs.items()}
    if any(capped[name] != min(EXPECTED_COUNTS[name], CAP) for name in docs):
        raise RuntimeError("prefix cap mismatch")
    return {
        "status": "PASS",
        "target_score_calls": 0,
        "c0_counts": {k: len(v) for k, v in docs.items()},
        "capped_counts": capped,
        "excluded_source": "C-HERB-1 Macer",
        "source_hashes_verified": True,
    }


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (3, 4):
        print(f"usage: {argv[0]} CACHE_DIR OUT.json | {argv[0]} CACHE_DIR --preflight", file=sys.stderr)
        return 2
    cache = Path(argv[1]).resolve()
    if argv[2] == "--preflight":
        print(json.dumps(preflight(cache), ensure_ascii=False, indent=1))
        print("TARGET_SCORE_CALLS=0")
        return 0

    out_path = Path(argv[2]).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # All source/hash/extraction gates complete before Phase-A target authority is loaded.
    pf = preflight(cache)
    phase_a_path = HERE / "first-reveal" / "phase84a_results.json"
    if sha256_file(phase_a_path) != PHASE_A_SHA256:
        raise RuntimeError("Phase-A result SHA-256 mismatch")
    phase_a = json.loads(phase_a_path.read_text(encoding="utf-8"))
    intervals = target_intervals(phase_a)

    raw_docs = extract_documents(cache, verify_all_source_hashes=False)
    docs = to_unit_docs(raw_docs)

    source_results = {}
    for name in EXPECTED_COUNTS:
        print(f"score source {name}", file=sys.stderr, flush=True)
        score = score_docs(f"Phase84C:{name}", [(name, docs[name])])
        source_results[name] = {
            "source_tokens_before_cap": len(raw_docs[name]),
            "tokens_scored": len(docs[name]),
            "prefix_cap": CAP,
            "score": score,
            "classification": classify(score, intervals),
        }

    genre_results = {}
    for genre, names in GENRES.items():
        print(f"score genre {genre}", file=sys.stderr, flush=True)
        gdocs = [(name, docs[name]) for name in names]
        score = score_docs(f"Phase84C:{genre}", gdocs)
        genre_results[genre] = {
            "documents": list(names),
            "descriptive_only": True,
            "score": score,
            "classification_against_same_interval_descriptive": classify(score, intervals),
        }

    hits = [name for name, r in source_results.items() if r["classification"]["n_responsibilities_passed"] == 3]
    partial2 = [name for name, r in source_results.items() if r["classification"]["n_responsibilities_passed"] == 2]
    partial1 = [name for name, r in source_results.items() if r["classification"]["n_responsibilities_passed"] == 1]
    panel_class = "SOME FROZEN HISTORICAL SOURCE IN VOYNICH REGIME" if hits else "NO FROZEN HISTORICAL SOURCE IN FULL VOYNICH REGIME"

    out = {
        "schema": "issue84-phaseC-v1",
        "phase": PHASE,
        "plan": "experiments/cross-linguistic-baselines/PLAN_C.md",
        "c0_report": "experiments/cross-linguistic-baselines/REPORT_C0_SOURCE_AUDIT.md",
        "preflight": pf,
        "source_authority": {
            sid: {k: v for k, v in spec.items() if k.endswith("sha256") or k == "c0_status"}
            for sid, spec in SOURCES.items()
        },
        "phaseA_authority": {
            "sha256": sha256_file(phase_a_path),
            "voynich_labels": list(VOYNICH_LABELS),
            "target_intervals": intervals,
            "far_bins_decisive": False,
        },
        "normalization": {
            "unicode": "NFC then casefold",
            "word_regex": WORD_RE.pattern,
            "prefix_cap_tokens": CAP,
            "ocr_correction": False,
            "spelling_modernization": False,
            "line_end_dehyphenation": False,
        },
        "sources": source_results,
        "genre_aggregates": genre_results,
        "panel": {
            "n_sources": len(source_results),
            "full_hits": hits,
            "partial_2_of_3": partial2,
            "partial_1_of_3": partial1,
            "classification": panel_class,
        },
        "claim_limit": (
            "Historical source-genre control only. A hit is an existence result for a frozen source organization, not "
            "a Voynich plaintext/genre identification; a miss does not reject all medieval genres."
        ),
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    compact = {
        "target_intervals": intervals,
        "sources": {name: row["classification"] for name, row in source_results.items()},
        "genre_aggregates": {name: row["classification_against_same_interval_descriptive"] for name, row in genre_results.items()},
        "panel": out["panel"],
    }
    print(json.dumps(compact, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
