#!/usr/bin/env python3
"""Issue #196 S0-C: score-free detail audit of all solved HCPortal postcards
with text attachments selected prospectively from S0-B metadata.

No attachment URL or image is fetched. No ciphertext statistic is computed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import unicodedata
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

SCHEMA = "issue196-hcportal-s0c-v1"
FROZEN_RECORDS = {
    1324: "pc_hcp_5",
    1473: "pc_hcp_154",
    1510: "pc_hcp_191",
    1789: "pc_hcp_470",
}
USER_AGENT = "LETSGO-Voynich-Issue196-score-free-source-audit/1.0"

CIPHER_ROLE_RE = re.compile(
    r"(?:^|[^a-z])(transcript(?:ion)?|cipher\s*text|ciphertext|cryptogram\s*text|encoded\s*text)(?:$|[^a-z])",
    re.IGNORECASE,
)
PLAIN_ROLE_RE = re.compile(
    r"(?:^|[^a-z])(solution|plain\s*text|plaintext|clear\s*text|cleartext|decipher(?:ment|ed)?|decrypt(?:ion|ed)?)(?:$|[^a-z])",
    re.IGNORECASE,
)
KEY_ROLE_RE = re.compile(
    r"(?:^|[^a-z])(cipher\s*key|cipherkey|key\s*map|mapping|alphabet\s*key|substitution\s*key)(?:$|[^a-z])",
    re.IGNORECASE,
)
ALIGN_ROLE_RE = re.compile(
    r"(?:^|[^a-z])(alignment|aligned|parallel\s*text|correspondence)(?:$|[^a-z])",
    re.IGNORECASE,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(url: str, retries: int = 3) -> bytes:
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as exc:
            last = exc
            if attempt + 1 < retries:
                time.sleep(2)
    raise RuntimeError(f"fetch failed after {retries} attempts: {last!r}")


def unwrap_record(payload):
    x = payload
    if isinstance(x, dict) and isinstance(x.get("data"), dict):
        x = x["data"]
    if isinstance(x, dict) and isinstance(x.get("data"), dict) and not {"id", "name", "datagroups"}.intersection(x):
        x = x["data"]
    return x if isinstance(x, dict) else None


def bounded_escaped(s: str, n: int = 120) -> dict:
    if not isinstance(s, str):
        return {}
    raw = s.encode("utf-8")
    norm = s.replace("\r\n", "\n").replace("\r", "\n")
    escaped = norm.encode("unicode_escape").decode("ascii")
    categories = {}
    for ch in s:
        cat = unicodedata.category(ch)
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "utf8_bytes": len(raw),
        "sha256_utf8": sha256(raw),
        "line_count": len(norm.split("\n")),
        "nonempty_line_count": sum(bool(x.strip()) for x in norm.split("\n")),
        "contains_newline": "\n" in norm,
        "contains_horizontal_whitespace": bool(re.search(r"[ \t]", s)),
        "alphabetic_run_count": len(re.findall(r"[^\W\d_]+", s, flags=re.UNICODE)),
        "unicode_categories": dict(sorted(categories.items())),
        "first_120_escaped": escaped[:n],
        "last_120_escaped": escaped[-n:] if escaped else "",
    }


def safe_url_meta(value):
    if not isinstance(value, str) or not value:
        return None
    p = urlsplit(value)
    return {"scheme": p.scheme, "host": p.netloc, "path": p.path, "has_query": bool(p.query)}


def role_from_label(label: str) -> set[str]:
    roles = set()
    if CIPHER_ROLE_RE.search(label):
        roles.add("ciphertext")
    if PLAIN_ROLE_RE.search(label):
        roles.add("plaintext")
    if KEY_ROLE_RE.search(label):
        roles.add("key")
    if ALIGN_ROLE_RE.search(label):
        roles.add("alignment")
    return roles


def scan_explicit_string_fields(record: dict):
    """Inspect only explicitly role-labeled scalar fields, not arbitrary prose semantics."""
    out = []
    for key, value in record.items():
        if not isinstance(value, str) or not value:
            continue
        roles = role_from_label(str(key))
        if roles:
            out.append({
                "field": str(key),
                "roles": sorted(roles),
                "stats": bounded_escaped(value),
            })
    return out


def scan_datagroups(record: dict):
    out = []
    explicit_texts = []
    groups = record.get("datagroups") if isinstance(record.get("datagroups"), list) else []
    for gi, group in enumerate(groups):
        if not isinstance(group, dict):
            continue
        desc = group.get("description") if isinstance(group.get("description"), str) else ""
        items_out = []
        items = group.get("data") if isinstance(group.get("data"), list) else []
        for ii, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            title = item.get("title") if isinstance(item.get("title"), str) else ""
            typ = item.get("type")
            label = f"{desc} {title}".strip()
            roles = role_from_label(label)
            text = item.get("text") if isinstance(item.get("text"), str) else None
            entry = {
                "index": ii,
                "type": typ,
                "title": title,
                "roles_from_group_and_title": sorted(roles),
                "has_text": bool(text),
                "text_stats": bounded_escaped(text) if text else None,
                "link": safe_url_meta(item.get("link")),
                "has_image": bool(item.get("image")),
                "field_names": sorted(str(k) for k in item.keys()),
            }
            if isinstance(item.get("image"), dict):
                entry["image_fields"] = sorted(str(k) for k in item["image"].keys())
                entry["image_url_meta"] = {
                    str(k): safe_url_meta(v) for k, v in item["image"].items() if isinstance(v, str)
                }
            items_out.append(entry)
            if text and roles:
                explicit_texts.append({
                    "source": f"datagroups[{gi}].data[{ii}]",
                    "label": label,
                    "roles": sorted(roles),
                    "text": text,
                    "stats": entry["text_stats"],
                })
        out.append({"index": gi, "description": desc, "item_count": len(items_out), "items": items_out})
    return out, explicit_texts


def has_explicit_key_field(record: dict) -> bool:
    if record.get("cipher_key_id") not in (None, "", 0, False):
        return True
    for key, value in record.items():
        if value in (None, "", [], {}, False):
            continue
        if "key" in role_from_label(str(key)):
            return True
    return False


def has_explicit_alignment_field(record: dict) -> bool:
    for key, value in record.items():
        if value in (None, "", [], {}, False):
            continue
        if "alignment" in role_from_label(str(key)):
            return True
    return False


def group_boundary_evidence(cipher_text: str) -> dict:
    """Describe only explicit text separators. Does not infer atomization semantics."""
    if not cipher_text:
        return {"explicit_boundary": False, "channels": {}}
    channels = {
        "pipe": cipher_text.count("|"),
        "slash_surrounded_by_space": len(re.findall(r"(?<=\s)/(?=\s)", cipher_text)),
        "double_space": len(re.findall(r"(?<=\S) {2,}(?=\S)", cipher_text)),
        "tab": len(re.findall(r"(?<=\S)\t+(?=\S)", cipher_text)),
    }
    return {"explicit_boundary": any(channels.values()), "channels": channels}


def audit_one(raw_a: bytes, raw_b: bytes, expected_id: int, expected_name: str):
    transport = {
        "bytes": len(raw_a),
        "bytes_repeat": len(raw_b),
        "sha256": sha256(raw_a),
        "sha256_repeat": sha256(raw_b),
        "repeat_identical": bool(raw_a == raw_b and raw_a),
    }
    if not transport["repeat_identical"]:
        return {"transport": transport, "valid": False, "reason": "unstable_or_empty"}
    try:
        payload = json.loads(raw_a.decode("utf-8-sig"))
    except Exception as exc:
        return {"transport": transport, "valid": False, "reason": f"json_decode:{exc!r}"}
    record = unwrap_record(payload)
    if not isinstance(record, dict):
        return {"transport": transport, "valid": False, "reason": "no_record_object"}
    if record.get("id") != expected_id or record.get("name") != expected_name:
        return {
            "transport": transport,
            "valid": False,
            "reason": "identity_mismatch",
            "actual_id": record.get("id"),
            "actual_name": record.get("name"),
        }
    solution = record.get("solution")
    solution_name = solution.get("name") if isinstance(solution, dict) else None
    scalar_roles = scan_explicit_string_fields(record)
    groups, explicit_texts = scan_datagroups(record)

    cipher_texts = [x for x in explicit_texts if "ciphertext" in x["roles"]]
    plain_texts = [x for x in explicit_texts if "plaintext" in x["roles"]]
    # Explicit role-labeled top-level scalar strings also count.
    for x in scalar_roles:
        pseudo = {"source": f"top.{x['field']}", "label": x["field"], "roles": x["roles"], "stats": x["stats"]}
        value = record[x["field"]]
        pseudo["text"] = value
        if "ciphertext" in x["roles"]:
            cipher_texts.append(pseudo)
        if "plaintext" in x["roles"]:
            plain_texts.append(pseudo)

    machine_cipher = bool(cipher_texts)
    cipher_multiline = any(x["stats"].get("nonempty_line_count", 0) >= 2 for x in cipher_texts)
    boundaries = [group_boundary_evidence(x["text"]) for x in cipher_texts]
    explicit_group_boundary = any(x["explicit_boundary"] for x in boundaries)
    plaintext_lexical = any(
        x["stats"].get("alphabetic_run_count", 0) >= 2
        and x["stats"].get("contains_horizontal_whitespace", False)
        for x in plain_texts
    )
    key_present = has_explicit_key_field(record)
    align_present = has_explicit_alignment_field(record)
    deterministic_alignment = bool(machine_cipher and plaintext_lexical and (key_present or align_present))
    layers = {
        "CIPHERTEXT_SYMBOLS": machine_cipher,
        "PHYSICAL_LINES": bool(machine_cipher and cipher_multiline),
        "CIPHER_UNIT_BOUNDARIES": bool(machine_cipher and explicit_group_boundary),
        "PLAINTEXT_LEXICAL_BOUNDARIES": plaintext_lexical,
        "CIPHER_PLAINTEXT_ALIGNMENT": deterministic_alignment,
    }
    sanitized_explicit = []
    for x in explicit_texts:
        sanitized_explicit.append({k: v for k, v in x.items() if k != "text"})
    return {
        "valid": True,
        "transport": transport,
        "identity": {"id": expected_id, "name": expected_name},
        "solution_label": solution_name,
        "cipher_key_id": record.get("cipher_key_id"),
        "top_level_fields": sorted(str(k) for k in record.keys()),
        "explicit_scalar_role_fields": scalar_roles,
        "datagroups": groups,
        "explicit_role_texts": sanitized_explicit,
        "cipher_text_source_count": len(cipher_texts),
        "plaintext_source_count": len(plain_texts),
        "key_or_mapping_field_present": key_present,
        "alignment_field_present": align_present,
        "cipher_group_boundary_diagnostics": boundaries,
        "layers": layers,
    }


def run(base_url: str):
    result = {
        "schema": SCHEMA,
        "issue": 196,
        "score_free": True,
        "r5_score_computed": False,
        "voynich_data_accessed": False,
        "attachment_targets_fetched": False,
        "image_pixels_accessed": False,
        "frozen_records": [{"id": k, "name": v} for k, v in FROZEN_RECORDS.items()],
        "records": [],
    }
    try:
        for rid, name in FROZEN_RECORDS.items():
            url = f"{base_url.rstrip('/')}/{rid}"
            a = fetch_bytes(url)
            b = fetch_bytes(url)
            x = audit_one(a, b, rid, name)
            x["url"] = url
            result["records"].append(x)
        if not all(x.get("valid") for x in result["records"]):
            result["classification"] = "INVALID_TRANSPORT"
            result["stage1_gate0_candidate_ids"] = []
            result["next_step"] = "MOVE_TO_MARY_STUART"
            return result
        passers = [x["identity"]["id"] for x in result["records"] if all(x["layers"].values())]
        result["stage1_gate0_candidate_ids"] = passers
        any_machine_cipher = any(x["layers"]["CIPHERTEXT_SYMBOLS"] for x in result["records"])
        any_alignment = any(x["layers"]["CIPHER_PLAINTEXT_ALIGNMENT"] for x in result["records"])
        if passers:
            result["classification"] = "ADMIT_FOR_PROSPECTIVE_R5_GATE0"
            result["next_step"] = "FREEZE_ONE_CANDIDATE_SELECTION_IF_MULTIPLE"
        elif not any_machine_cipher:
            result["classification"] = "HCPORTAL_POSTCARDS_NO_MACHINE_READABLE_CIPHERTEXT"
            result["next_step"] = "MOVE_TO_MARY_STUART"
        elif not any_alignment:
            result["classification"] = "HCPORTAL_POSTCARDS_ALIGNMENT_INSUFFICIENT"
            result["next_step"] = "MOVE_TO_MARY_STUART"
        else:
            result["classification"] = "HCPORTAL_POSTCARDS_OTHER_LAYER_FAILURE"
            result["next_step"] = "MOVE_TO_MARY_STUART"
    except Exception as exc:
        result["transport_error"] = repr(exc)
        result["classification"] = "INVALID_TRANSPORT"
        result["stage1_gate0_candidate_ids"] = []
        result["next_step"] = "MOVE_TO_MARY_STUART"
    return result


def self_test():
    toy = {
        "data": {
            "id": 1324,
            "name": "pc_hcp_5",
            "solution": {"id": 1, "name": "Solved"},
            "cipher_key_id": 7,
            "datagroups": [{
                "description": "Transcriptions and solutions",
                "data": [
                    {"type": "text", "title": "Transcription", "text": "AA BB | CC\nDD EE | FF"},
                    {"type": "text", "title": "Solution", "text": "two words here"},
                ],
            }],
        }
    }
    raw = json.dumps(toy).encode()
    x = audit_one(raw, raw, 1324, "pc_hcp_5")
    assert x["valid"]
    assert x["layers"]["CIPHERTEXT_SYMBOLS"]
    assert x["layers"]["PHYSICAL_LINES"]
    assert x["layers"]["CIPHER_UNIT_BOUNDARIES"]
    assert x["layers"]["PLAINTEXT_LEXICAL_BOUNDARIES"]
    assert x["layers"]["CIPHER_PLAINTEXT_ALIGNMENT"]
    toy["data"]["cipher_key_id"] = None
    toy["data"]["datagroups"][0]["data"] = [{"type": "text", "title": "Solution", "text": "two words"}]
    raw2 = json.dumps(toy).encode()
    y = audit_one(raw2, raw2, 1324, "pc_hcp_5")
    assert not y["layers"]["CIPHERTEXT_SYMBOLS"]
    assert y["layers"]["PLAINTEXT_LEXICAL_BOUNDARIES"]
    print(json.dumps({"schema": SCHEMA, "self_test": "PASS"}, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--base-url", default="https://api.hcportal.eu/api/cryptograms")
    ap.add_argument("--output")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.run or not args.output:
        ap.error("--run requires --output")
    out = run(args.base_url)
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out.get("classification"),
        "next_step": out.get("next_step"),
        "stage1_gate0_candidate_ids": out.get("stage1_gate0_candidate_ids"),
        "record_layers": {str(x.get('identity',{}).get('id')): x.get('layers') for x in out.get('records',[]) if x.get('identity')},
        "r5_score_computed": out.get("r5_score_computed"),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
