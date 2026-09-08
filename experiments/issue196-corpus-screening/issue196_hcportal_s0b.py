#!/usr/bin/env python3
"""Issue #196 S0-B: score-free HCPortal postcard population metadata audit.

No attachment targets are fetched and no ciphertext/plaintext content is scored.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

SCHEMA = "issue196-hcportal-s0b-v1"
NAME_RE = re.compile(r"^pc_hcp_[0-9]+$")
PER_PAGE = 100
MAX_PAGES = 100
USER_AGENT = "LETSGO-Voynich-Issue196-score-free-source-audit/1.0"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(url: str, retries: int = 3) -> bytes:
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as exc:
            last = exc
            if attempt + 1 < retries:
                time.sleep(2)
    raise RuntimeError(f"fetch failed after {retries} attempts: {last!r}")


def page_url(base: str, page: int) -> str:
    q = urllib.parse.urlencode({"detailed": 1, "per_page": PER_PAGE, "page": page})
    return f"{base}?{q}"


def parse_page(raw: bytes):
    payload = json.loads(raw.decode("utf-8-sig"))
    outer = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(outer, dict):
        raise ValueError("missing object payload.data")
    records = outer.get("data")
    if not isinstance(records, list):
        raise ValueError("missing list payload.data.data")
    current = outer.get("current_page")
    last = outer.get("last_page")
    total = outer.get("total")
    per_page = outer.get("per_page")
    if not isinstance(current, int) or not isinstance(last, int):
        raise ValueError("pagination current_page/last_page missing or non-integer")
    return payload, records, {"current_page": current, "last_page": last, "total": total, "per_page": per_page}


def safe_link_meta(value):
    if not isinstance(value, str) or not value:
        return None
    p = urlsplit(value)
    return {"scheme": p.scheme, "host": p.netloc, "path": p.path, "has_query": bool(p.query)}


def text_meta(value):
    if not isinstance(value, str) or not value:
        return None
    b = value.encode("utf-8")
    norm = value.replace("\r\n", "\n").replace("\r", "\n")
    return {
        "utf8_bytes": len(b),
        "sha256_utf8": sha256(b),
        "line_count": len(norm.split("\n")),
        "contains_newline": "\n" in norm,
        "contains_horizontal_whitespace": bool(re.search(r"[ \t]", value)),
    }


def solution_label(record) -> str:
    s = record.get("solution")
    if s is None:
        return "<NULL>"
    if isinstance(s, dict):
        name = s.get("name")
        return str(name) if name is not None else "<OBJECT_WITHOUT_NAME>"
    return f"<{type(s).__name__.upper()}>"


def record_attachment_meta(record):
    descriptions = Counter()
    item_types = Counter()
    item_titles = Counter()
    has_text = False
    has_link = False
    has_image = False
    text_meta_items = []
    link_meta_items = []
    groups = record.get("datagroups")
    if not isinstance(groups, list):
        groups = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        desc = group.get("description")
        descriptions[str(desc) if desc is not None else "<NULL>"] += 1
        items = group.get("data")
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            typ = item.get("type")
            title = item.get("title")
            item_types[str(typ) if typ is not None else "<NULL>"] += 1
            item_titles[str(title) if title is not None else "<NULL>"] += 1
            t = text_meta(item.get("text"))
            if t:
                has_text = True
                text_meta_items.append({"title": title, **t})
            l = safe_link_meta(item.get("link"))
            if l:
                has_link = True
                link_meta_items.append({"title": title, **l})
            if item.get("image"):
                has_image = True
    return {
        "has_text": has_text,
        "has_link": has_link,
        "has_image": has_image,
        "group_descriptions": descriptions,
        "item_types": item_types,
        "item_titles": item_titles,
        "text_meta_items": text_meta_items,
        "link_meta_items": link_meta_items,
    }


def id_name(record):
    return {"id": record.get("id"), "name": record.get("name")}


def audit_records(records):
    postcards = [r for r in records if isinstance(r, dict) and isinstance(r.get("name"), str) and NAME_RE.fullmatch(r["name"])]
    solution_counts = Counter()
    group_descriptions = Counter()
    item_types = Counter()
    item_titles = Counter()
    category_counts = Counter()
    language_counts = Counter()
    availability_counts = Counter()
    state_counts = Counter()
    n_key = n_text = n_link = n_image = 0
    intersections = {
        "paired_key_and_text": [],
        "paired_key_and_link": [],
        "paired_key_and_text_or_link": [],
    }
    label_key = defaultdict(list)
    label_textlink = defaultdict(list)
    label_key_textlink = defaultdict(list)
    per_record = []
    for r in postcards:
        label = solution_label(r)
        solution_counts[label] += 1
        has_key = r.get("cipher_key_id") not in (None, "", 0, False)
        a = record_attachment_meta(r)
        text_or_link = a["has_text"] or a["has_link"]
        n_key += int(has_key)
        n_text += int(a["has_text"])
        n_link += int(a["has_link"])
        n_image += int(a["has_image"])
        group_descriptions.update(a["group_descriptions"])
        item_types.update(a["item_types"])
        item_titles.update(a["item_titles"])
        category = r.get("sub_category") or r.get("category")
        category_name = category.get("name") if isinstance(category, dict) else category
        language = r.get("language")
        language_name = language.get("name") if isinstance(language, dict) else language
        state = r.get("state")
        state_name = state.get("title") if isinstance(state, dict) else state
        category_counts[str(category_name)] += 1
        language_counts[str(language_name)] += 1
        availability_counts[str(r.get("availability"))] += 1
        state_counts[str(state_name)] += 1
        member = id_name(r)
        if has_key and a["has_text"]:
            intersections["paired_key_and_text"].append(member)
        if has_key and a["has_link"]:
            intersections["paired_key_and_link"].append(member)
        if has_key and text_or_link:
            intersections["paired_key_and_text_or_link"].append(member)
        if has_key:
            label_key[label].append(member)
        if text_or_link:
            label_textlink[label].append(member)
        if has_key and text_or_link:
            label_key_textlink[label].append(member)
        per_record.append({
            "id": r.get("id"),
            "name": r.get("name"),
            "solution_label": label,
            "cipher_key_id": r.get("cipher_key_id"),
            "has_text_attachment": a["has_text"],
            "has_link_attachment": a["has_link"],
            "has_image_attachment": a["has_image"],
            "text_attachment_metadata": a["text_meta_items"],
            "link_attachment_metadata": a["link_meta_items"],
        })
    n = len(postcards)
    return {
        "postcard_count": n,
        "solution_labels": dict(sorted(solution_counts.items())),
        "paired_cipher_key_count": n_key,
        "paired_cipher_key_share": n_key / n if n else 0.0,
        "text_attachment_record_count": n_text,
        "link_attachment_record_count": n_link,
        "image_attachment_record_count": n_image,
        "text_or_link_attachment_record_count": sum(1 for x in per_record if x["has_text_attachment"] or x["has_link_attachment"]),
        "group_description_counts": dict(sorted(group_descriptions.items())),
        "item_type_counts": dict(sorted(item_types.items())),
        "item_title_counts": dict(sorted(item_titles.items())),
        "category_counts": dict(sorted(category_counts.items())),
        "language_counts": dict(sorted(language_counts.items())),
        "availability_counts": dict(sorted(availability_counts.items())),
        "state_counts": dict(sorted(state_counts.items())),
        "predeclared_intersections": intersections,
        "solution_label_x_paired_key": {k: v for k, v in sorted(label_key.items()) if v},
        "solution_label_x_text_or_link": {k: v for k, v in sorted(label_textlink.items()) if v},
        "solution_label_x_paired_key_x_text_or_link": {k: v for k, v in sorted(label_key_textlink.items()) if v},
        "postcard_metadata_records": sorted(per_record, key=lambda x: (x["id"] is None, x["id"])),
    }


def run(base_url: str):
    result = {
        "schema": SCHEMA,
        "issue": 196,
        "score_free": True,
        "r5_score_computed": False,
        "voynich_data_accessed": False,
        "attachment_targets_fetched": False,
        "population_regex": NAME_RE.pattern,
        "transport_pages": [],
    }
    try:
        raw_a = fetch_bytes(page_url(base_url, 1))
        raw_b = fetch_bytes(page_url(base_url, 1))
        if raw_a != raw_b or not raw_a:
            raise RuntimeError("page 1 repeated payload mismatch or empty")
        _p, records1, meta1 = parse_page(raw_a)
        last_page = meta1["last_page"]
        if last_page < 1 or last_page > MAX_PAGES:
            raise RuntimeError(f"last_page outside frozen 1..{MAX_PAGES}: {last_page}")
        pages_records = []
        for page in range(1, last_page + 1):
            if page == 1:
                a, b, recs, meta = raw_a, raw_b, records1, meta1
            else:
                a = fetch_bytes(page_url(base_url, page))
                b = fetch_bytes(page_url(base_url, page))
                if a != b or not a:
                    raise RuntimeError(f"page {page} repeated payload mismatch or empty")
                _payload, recs, meta = parse_page(a)
            if meta["current_page"] != page or meta["last_page"] != last_page:
                raise RuntimeError(f"pagination metadata drift at page {page}: {meta}")
            result["transport_pages"].append({
                "page": page,
                "url": page_url(base_url, page),
                "bytes": len(a),
                "sha256": sha256(a),
                "repeat_identical": a == b,
                "record_count": len(recs),
                "pagination": meta,
            })
            pages_records.extend(recs)
        ids = [r.get("id") for r in pages_records if isinstance(r, dict)]
        nonnull_ids = [x for x in ids if x is not None]
        if len(nonnull_ids) != len(set(nonnull_ids)):
            raise RuntimeError("duplicate record IDs across pages")
        result["total_public_cryptograms_received"] = len(pages_records)
        result["api_reported_total"] = meta1.get("total")
        result["population"] = audit_records(pages_records)
        p = result["population"]
        if p["paired_cipher_key_count"] == 0 and p["text_or_link_attachment_record_count"] == 0:
            result["classification"] = "SOURCE_METADATA_INSUFFICIENT"
            result["next_step"] = "MOVE_TO_MARY_STUART"
        else:
            result["classification"] = "POPULATION_HAS_COMPOSABILITY_METADATA_CANDIDATES"
            result["next_step"] = "FREEZE_S0C_METADATA_FILTER_BEFORE_DETAIL_FETCH"
    except Exception as exc:
        result["transport_error"] = repr(exc)
        result["classification"] = "INVALID_TRANSPORT"
        result["next_step"] = "MOVE_TO_MARY_STUART"
    return result


def self_test():
    toy = [
        {
            "id": 1, "name": "pc_hcp_1", "solution": {"name": "Solved"}, "cipher_key_id": 9,
            "category": {"name": "Substitution"}, "language": {"name": "German"}, "availability": "Public",
            "state": {"title": "Published"},
            "datagroups": [{"description": "Files", "data": [{"type": "text", "title": "Transcription", "text": "AB CD\nEF"}]}],
        },
        {
            "id": 2, "name": "pc_hcp_2", "solution": {"name": "Not solved"}, "cipher_key_id": None,
            "category": {"name": "Substitution"}, "language": {"name": "Unknown"}, "availability": "Private",
            "state": {"title": "Published"},
            "datagroups": [{"description": "Cryptogram", "data": [{"type": "image", "title": "Side", "image": {"original": "https://x/y.jpg"}}]}],
        },
        {"id": 3, "name": "other_3", "solution": None, "datagroups": []},
    ]
    a = audit_records(toy)
    assert a["postcard_count"] == 2
    assert a["paired_cipher_key_count"] == 1
    assert a["text_attachment_record_count"] == 1
    assert a["solution_labels"] == {"Not solved": 1, "Solved": 1}
    assert a["predeclared_intersections"]["paired_key_and_text"] == [{"id": 1, "name": "pc_hcp_1"}]
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
    pop = out.get("population", {})
    print(json.dumps({
        "classification": out.get("classification"),
        "next_step": out.get("next_step"),
        "total_public_cryptograms_received": out.get("total_public_cryptograms_received"),
        "postcard_count": pop.get("postcard_count"),
        "solution_labels": pop.get("solution_labels"),
        "paired_cipher_key_count": pop.get("paired_cipher_key_count"),
        "text_attachment_record_count": pop.get("text_attachment_record_count"),
        "link_attachment_record_count": pop.get("link_attachment_record_count"),
        "text_or_link_attachment_record_count": pop.get("text_or_link_attachment_record_count"),
        "r5_score_computed": out.get("r5_score_computed"),
    }, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
