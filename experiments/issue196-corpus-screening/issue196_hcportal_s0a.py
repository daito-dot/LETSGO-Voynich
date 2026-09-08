#!/usr/bin/env python3
"""Issue #196 S0-A: score-free HCPortal structural schema inspection.

The script inspects only the externally preselected HCPortal record 1454 payload.
It computes no ciphertext transition, adjacency, R5, or Voynich statistic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

SCHEMA = "issue196-hcportal-s0a-v1"
RECORD_ID = 1454
KEYWORDS = (
    "transcript", "plaintext", "plain_text", "cleartext", "clear_text",
    "solution", "solved", "decrypt", "decipher", "cipher_key", "key_id",
    "line", "spacing", "space", "attachment", "data", "text",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_host_path(url: str | None):
    if not isinstance(url, str) or not url:
        return None
    try:
        p = urlsplit(url)
        return {"scheme": p.scheme, "host": p.netloc, "path": p.path, "has_query": bool(p.query)}
    except Exception:
        return {"unparsed": True, "length": len(url)}


def text_stats(value: str | None):
    if not isinstance(value, str):
        return None
    b = value.encode("utf-8")
    lines = value.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return {
        "chars": len(value),
        "utf8_bytes": len(b),
        "sha256_utf8": sha256(b),
        "line_count": len(lines),
        "nonempty_lines": sum(bool(x.strip()) for x in lines),
        "contains_newline": "\n" in value or "\r" in value,
        "contains_space": bool(re.search(r"[ \t]", value)),
        "wordlike_runs": len(re.findall(r"[^\W\d_]+", value, flags=re.UNICODE)),
    }


def unwrap_record(payload):
    candidates = [payload]
    if isinstance(payload, dict):
        if "data" in payload:
            candidates.append(payload["data"])
            if isinstance(payload["data"], dict) and "data" in payload["data"]:
                candidates.append(payload["data"]["data"])
    for x in reversed(candidates):
        if isinstance(x, dict) and ("id" in x or "name" in x or "datagroups" in x):
            return x
    return None


def summarize_paths(obj, path="$", depth=0, max_depth=6, out=None):
    if out is None:
        out = []
    if depth > max_depth:
        return out
    if isinstance(obj, dict):
        out.append({"path": path, "type": "object", "size": len(obj)})
        for key in sorted(obj, key=str):
            summarize_paths(obj[key], f"{path}.{key}", depth + 1, max_depth, out)
    elif isinstance(obj, list):
        out.append({"path": path, "type": "array", "size": len(obj)})
        # Schema-only: inspect at most first three elements and do not emit values.
        for i, value in enumerate(obj[:3]):
            summarize_paths(value, f"{path}[{i}]", depth + 1, max_depth, out)
    else:
        out.append({"path": path, "type": type(obj).__name__})
    return out


def find_keyword_fields(obj, path="$", out=None):
    if out is None:
        out = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            p = f"{path}.{key}"
            folded = str(key).casefold()
            if any(k in folded for k in KEYWORDS):
                item = {"path": p, "field": str(key), "type": type(value).__name__}
                if isinstance(value, (str, int, float, bool)) or value is None:
                    if isinstance(value, str):
                        item["text_stats"] = text_stats(value)
                        if len(value) <= 120 and not any(ch in value for ch in "\r\n"):
                            item["bounded_scalar"] = value
                    else:
                        item["bounded_scalar"] = value
                elif isinstance(value, (list, dict)):
                    item["size"] = len(value)
                out.append(item)
            find_keyword_fields(value, p, out)
    elif isinstance(obj, list):
        for i, value in enumerate(obj[:1000]):
            find_keyword_fields(value, f"{path}[{i}]", out)
    return out


def audit_datagroups(record):
    groups = record.get("datagroups") if isinstance(record, dict) else None
    if not isinstance(groups, list):
        return {"present": False, "group_count": 0, "groups": []}
    result = []
    total_items = 0
    text_items = 0
    link_items = 0
    image_items = 0
    for gi, group in enumerate(groups):
        if not isinstance(group, dict):
            continue
        items = group.get("data") if isinstance(group.get("data"), list) else []
        gout = {
            "index": gi,
            "description": group.get("description") if isinstance(group.get("description"), str) else None,
            "item_count": len(items),
            "items": [],
        }
        for ii, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            total_items += 1
            typ = item.get("type")
            text = item.get("text")
            link = item.get("link")
            image = item.get("image")
            if isinstance(text, str) and text:
                text_items += 1
            if isinstance(link, str) and link:
                link_items += 1
            if image:
                image_items += 1
            io = {
                "index": ii,
                "type": typ,
                "title": item.get("title") if isinstance(item.get("title"), str) else None,
                "text_stats": text_stats(text) if isinstance(text, str) else None,
                "link": safe_host_path(link),
                "has_image": bool(image),
                "field_names": sorted(str(k) for k in item.keys()),
            }
            if isinstance(image, dict):
                io["image_fields"] = sorted(str(k) for k in image.keys())
                io["image_urls"] = {
                    str(k): safe_host_path(v) for k, v in image.items() if isinstance(v, str)
                }
            gout["items"].append(io)
        result.append(gout)
    return {
        "present": True,
        "group_count": len(groups),
        "total_items": total_items,
        "text_items": text_items,
        "link_items": link_items,
        "image_items": image_items,
        "groups": result,
    }


def compact_metadata(record):
    if not isinstance(record, dict):
        return {}
    category = record.get("sub_category") or record.get("category")
    language = record.get("language")
    location = record.get("location")
    return {
        "id": record.get("id"),
        "name": record.get("name"),
        "date": record.get("date"),
        "date_around": record.get("date_around"),
        "availability": record.get("availability"),
        "used_chars": record.get("used_chars"),
        "cipher_key_id": record.get("cipher_key_id"),
        "category": category.get("name") if isinstance(category, dict) else category,
        "language": language.get("name") if isinstance(language, dict) else language,
        "location": {
            "continent": location.get("continent"),
            "name": location.get("name"),
        } if isinstance(location, dict) else location,
        "top_level_fields": sorted(str(k) for k in record.keys()),
    }


def run(a: Path, b: Path):
    result = {
        "schema": SCHEMA,
        "issue": 196,
        "record_id": RECORD_ID,
        "score_free": True,
        "r5_score_computed": False,
        "voynich_data_accessed": False,
    }
    if not a.exists() or not b.exists():
        result.update({
            "transport": {"available": False, "stable": False, "reason": "missing_download"},
            "classification": "SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE",
            "next_step": "MOVE_TO_PRIORITY_B",
        })
        return result
    ba, bb = a.read_bytes(), b.read_bytes()
    transport = {
        "available": bool(ba and bb),
        "stable": ba == bb and bool(ba),
        "bytes": len(ba),
        "bytes_repeat": len(bb),
        "sha256": sha256(ba),
        "sha256_repeat": sha256(bb),
    }
    result["transport"] = transport
    if not transport["available"] or not transport["stable"]:
        result.update({"classification": "SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE", "next_step": "MOVE_TO_PRIORITY_B"})
        return result
    try:
        text = ba.decode("utf-8-sig")
        payload = json.loads(text)
    except Exception as exc:
        result.update({
            "transport_parse_error": repr(exc),
            "classification": "SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE",
            "next_step": "MOVE_TO_PRIORITY_B",
        })
        return result
    record = unwrap_record(payload)
    result["payload_schema_paths"] = summarize_paths(payload)
    result["keyword_fields"] = find_keyword_fields(payload)
    if record is None:
        result.update({
            "classification": "SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE",
            "next_step": "MOVE_TO_PRIORITY_B",
            "reason": "json_but_no_record_object",
        })
        return result
    result["metadata"] = compact_metadata(record)
    result["datagroups"] = audit_datagroups(record)

    record_matches = int(record.get("id") == RECORD_ID)
    has_key = record.get("cipher_key_id") not in (None, "", 0, False)
    dg = result["datagroups"]
    has_structured_attachment = dg.get("total_items", 0) > 0
    has_text_or_link = dg.get("text_items", 0) > 0 or dg.get("link_items", 0) > 0
    relevant = result["keyword_fields"]
    relevant_content_field_count = sum(
        1 for x in relevant
        if any(k in x["field"].casefold() for k in ("transcript", "plaintext", "solution", "decrypt", "decipher"))
    )
    result["screening_flags"] = {
        "record_id_matches_1454": bool(record_matches),
        "paired_cipher_key_reference_present": bool(has_key),
        "structured_attachment_items_present": bool(has_structured_attachment),
        "attachment_text_or_link_present": bool(has_text_or_link),
        "relevant_content_field_count": relevant_content_field_count,
    }
    # This is a schema/access decision only, not a five-layer admission decision.
    if record_matches and (has_structured_attachment or relevant_content_field_count > 0):
        result["classification"] = "NEEDS_SCORE_FREE_SOURCE_INSPECTION"
        result["next_step"] = "FREEZE_POPULATION_SCHEMA_OR_LINK_INSPECTION"
    else:
        result["classification"] = "SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE" if not record_matches else "NEEDS_SCORE_FREE_SOURCE_INSPECTION"
        result["next_step"] = "MOVE_TO_PRIORITY_B" if not record_matches else "RECORD_METADATA_INSUFFICIENT_CHECK_POPULATION_SCHEMA"
    return result


def self_test():
    toy = {
        "data": {
            "data": {
                "id": 1454,
                "name": "toy",
                "cipher_key_id": 9,
                "datagroups": [{
                    "description": "Attachments",
                    "data": [
                        {"type": "text", "title": "Transcription", "text": "AB CD\nEF GH", "link": None},
                        {"type": "link", "title": "Solution", "text": "", "link": "https://example.org/solution.txt"},
                    ],
                }],
            }
        }
    }
    r = unwrap_record(toy)
    assert r["id"] == 1454
    dg = audit_datagroups(r)
    assert dg["text_items"] == 1 and dg["link_items"] == 1
    ks = find_keyword_fields(toy)
    assert any("cipher_key_id" in x["path"] for x in ks)
    assert text_stats("A B\nC")["line_count"] == 2
    print(json.dumps({"schema": SCHEMA, "self_test": "PASS"}, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--a")
    ap.add_argument("--b")
    ap.add_argument("--output")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.run or not args.a or not args.b or not args.output:
        ap.error("--run requires --a --b --output")
    out = run(Path(args.a), Path(args.b))
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out.get("classification"),
        "next_step": out.get("next_step"),
        "transport": out.get("transport"),
        "metadata": out.get("metadata"),
        "screening_flags": out.get("screening_flags"),
        "r5_score_computed": out.get("r5_score_computed"),
    }, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
