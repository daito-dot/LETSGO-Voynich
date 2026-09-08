#!/usr/bin/env python3
"""Issue #196 S0-D: score-free public source locator for Mary Stuart/Castelnau.

Looks only for reproducible machine-readable corpus/transcription/key/alignment
artifacts. It does not inspect ciphertext statistics or Voynich data.
"""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SCHEMA = "issue196-mary-stuart-s0d-v1"
DOI = "10.1080/01611194.2022.2160677"
TITLE_ASCII = "Deciphering Mary Stuart's lost letters from 1578-1584"
CTTS_COMMIT = "d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b"
USER_AGENT = "LETSGO-Voynich-Issue196-score-free-source-locator/1.0"
SOURCE_TERMS = [
    "mary stuart", "mary-castelnau", "mary castelnau", "castelnau",
    "f38", "fr. 2988", "2988 f.38", "20506",
]
ROLE_TERMS = [
    "transcription", "transcript", "ciphertext", "cipher text", "corpus",
    "dataset", "data", "nomenclator", "alignment", "aligned", "ctts project",
]
DATA_EXTS = {".txt", ".csv", ".tsv", ".json", ".xml", ".tei", ".zip", ".tar", ".gz", ".7z", ".ctts", ".dat"}
EXCLUDED_EXTS = {".pdf", ".html", ".htm", ".epub", ".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".svg", ".md", ".java", ".class", ".jar"}
TEXT_SCAN_EXTS = {".md", ".txt", ".java", ".xml", ".properties", ".json", ".csv", ".tsv", ".yml", ".yaml", ".html", ".htm"}
GITHUB_QUERIES = ["Castelnau", '"Mary Stuart"', "F38", "2988", "20506"]
ZENODO_QUERIES = [DOI, TITLE_ASCII, "Mary Castelnau cipher"]
PUBLISHER_URL = f"https://www.tandfonline.com/doi/full/{DOI}"
CROSSREF_URL = f"https://api.crossref.org/works/{urllib.parse.quote(DOI, safe='')}"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, headers=None, timeout=60):
    h = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            return {"ok": True, "status": getattr(r, "status", 200), "url": r.geturl(), "headers": {"content-type": r.headers.get("content-type"), "content-length": r.headers.get("content-length")}, "data": data}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "url": url, "error": f"HTTPError:{exc.code}"}
    except Exception as exc:
        return {"ok": False, "status": None, "url": url, "error": repr(exc)}


def is_source_relevant(text: str) -> bool:
    s = text.casefold()
    return any(t in s for t in SOURCE_TERMS)


def has_role(text: str) -> bool:
    s = text.casefold()
    if re.search(r"(?:^|[^a-z])key(?:$|[^a-z])", s):
        return True
    return any(t in s for t in ROLE_TERMS)


def extension_from(value: str) -> str:
    try:
        path = urllib.parse.urlsplit(value).path
    except Exception:
        path = value
    name = Path(path).name.casefold()
    for ext in sorted(DATA_EXTS | EXCLUDED_EXTS, key=len, reverse=True):
        if name.endswith(ext):
            return ext
    return Path(name).suffix.casefold()


def data_like_candidate(source: str, locator: str, context: str, inherited_source=False):
    combined = f"{locator} {context}"
    relevant = inherited_source or is_source_relevant(combined)
    ext = extension_from(locator)
    data_like = ext in DATA_EXTS
    excluded = ext in EXCLUDED_EXTS
    role = has_role(combined)
    return {
        "source": source,
        "locator": locator,
        "context": context[:500],
        "source_relevant": relevant,
        "role_relevant": role,
        "extension": ext,
        "data_like": data_like,
        "excluded": excluded,
        "positive_candidate": bool(relevant and role and data_like and not excluded),
    }


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        if tag.casefold() == "a":
            d = dict(attrs)
            self._href = d.get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.casefold() == "a" and self._href is not None:
            self.links.append((self._href, " ".join("".join(self._text).split())))
            self._href = None
            self._text = []


def audit_ctts(root: Path):
    out = {"ok": False, "expected_commit": CTTS_COMMIT, "actual_commit": None, "path_hits": [], "content_hits": [], "candidate_checks": []}
    if not root.exists():
        out["error"] = "missing_root"
        return out
    try:
        actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        out["actual_commit"] = actual
        if actual != CTTS_COMMIT:
            out["error"] = "commit_mismatch"
            return out
        for p in sorted(root.rglob("*")):
            if not p.is_file() or ".git" in p.parts:
                continue
            rel = p.relative_to(root).as_posix()
            if is_source_relevant(rel):
                out["path_hits"].append(rel)
                out["candidate_checks"].append(data_like_candidate("CTTS_path", rel, rel))
            if p.suffix.casefold() not in TEXT_SCAN_EXTS or p.stat().st_size > 2_000_000:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="strict")
            except Exception:
                continue
            folded = text.casefold()
            for term in SOURCE_TERMS:
                idx = folded.find(term)
                if idx >= 0:
                    a = max(0, idx - 120)
                    b = min(len(text), idx + len(term) + 120)
                    context = " ".join(text[a:b].split())[:240]
                    hit = {"path": rel, "term": term, "context": context}
                    out["content_hits"].append(hit)
                    out["candidate_checks"].append(data_like_candidate("CTTS_content", rel, context))
                    break
        out["ok"] = True
    except Exception as exc:
        out["error"] = repr(exc)
    return out


def audit_crossref():
    responses = [fetch(CROSSREF_URL, {"Accept": "application/json"}) for _ in range(2)]
    out = {"ok": False, "url": CROSSREF_URL, "attempts": [{k: v for k, v in r.items() if k != "data"} for r in responses], "candidate_checks": []}
    if not all(r["ok"] for r in responses):
        return out
    try:
        objs = [json.loads(r["data"].decode("utf-8"))["message"] for r in responses]
        dois = [str(x.get("DOI", "")).casefold() for x in objs]
        titles = [" ".join(x.get("title") or []) for x in objs]
        if any(x != DOI.casefold() for x in dois) or titles[0] != titles[1]:
            out["error"] = "doi_or_title_instability"
            return out
        x = objs[0]
        out["doi"] = x.get("DOI")
        out["title"] = titles[0]
        out["relation"] = x.get("relation") or {}
        out["links"] = [{k: z.get(k) for k in ("URL", "content-type", "content-version", "intended-application")} for z in (x.get("link") or [])]
        for z in x.get("link") or []:
            url = z.get("URL") or ""
            context = json.dumps({k: z.get(k) for k in z}, sort_keys=True)
            out["candidate_checks"].append(data_like_candidate("Crossref_link", url, context, inherited_source=True))
        # Related identifiers are recorded but only data-like explicit links can be positive here.
        out["ok"] = True
    except Exception as exc:
        out["error"] = repr(exc)
    return out


def audit_publisher():
    attempts = [fetch(PUBLISHER_URL, {"Accept": "text/html,application/xhtml+xml"}) for _ in range(2)]
    out = {"optional_channel": True, "ok": False, "url": PUBLISHER_URL, "attempts": [{k: v for k, v in r.items() if k != "data"} for r in attempts], "interesting_links": [], "candidate_checks": []}
    if not all(r["ok"] for r in attempts):
        return out
    try:
        texts = [r["data"].decode("utf-8", errors="replace") for r in attempts]
        parser = LinkParser(); parser.feed(texts[0])
        kws = tuple(["supp", "data", "dataset", "transcript", "download", "github", "zenodo", "figshare", "osf", "decrypt", "cryptiana"] + SOURCE_TERMS)
        for href, text in parser.links:
            absolute = urllib.parse.urljoin(attempts[0].get("url") or PUBLISHER_URL, href)
            joined = f"{absolute} {text}".casefold()
            if any(k in joined for k in kws):
                item = {"url": absolute, "text": text[:240]}
                out["interesting_links"].append(item)
                out["candidate_checks"].append(data_like_candidate("publisher_link", absolute, text, inherited_source=True))
        out["html_sha256"] = [sha256(r["data"]) for r in attempts]
        out["ok"] = True
    except Exception as exc:
        out["error"] = repr(exc)
    return out


def audit_github():
    token = os.environ.get("GH_DISCOVERY_TOKEN")
    out = {"ok": False, "queries": [], "candidate_checks": []}
    if not token:
        out["error"] = "missing_GH_DISCOVERY_TOKEN"
        return out
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"}
    success = True
    for q in GITHUB_QUERIES:
        query = f"{q} user:GeorgeLasry"
        url = "https://api.github.com/search/code?" + urllib.parse.urlencode({"q": query, "per_page": 100})
        r = fetch(url, headers)
        qout = {"query": query, "ok": r["ok"], "status": r.get("status"), "items": []}
        if not r["ok"]:
            qout["error"] = r.get("error")
            success = False
        else:
            try:
                obj = json.loads(r["data"].decode("utf-8"))
                for item in obj.get("items") or []:
                    repo = (item.get("repository") or {}).get("full_name")
                    path = item.get("path") or ""
                    html_url = item.get("html_url") or ""
                    ent = {"repository": repo, "path": path, "html_url": html_url}
                    qout["items"].append(ent)
                    out["candidate_checks"].append(data_like_candidate("GitHub_code", f"{repo}/{path}", f"query={q}"))
            except Exception as exc:
                qout["error"] = repr(exc)
                qout["ok"] = False
                success = False
        out["queries"].append(qout)
        time.sleep(1)
    out["ok"] = success
    return out


def audit_zenodo():
    out = {"ok": True, "queries": [], "records": [], "candidate_checks": []}
    seen = set()
    for q in ZENODO_QUERIES:
        url = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": q, "size": 25})
        r = fetch(url, {"Accept": "application/json"})
        qout = {"query": q, "url": url, "ok": r["ok"], "status": r.get("status")}
        if not r["ok"]:
            qout["error"] = r.get("error")
            out["ok"] = False
            out["queries"].append(qout)
            continue
        try:
            obj = json.loads(r["data"].decode("utf-8"))
            hits = (obj.get("hits") or {}).get("hits") or []
            qout["hit_count_returned"] = len(hits)
            for rec in hits:
                rid = rec.get("id")
                meta = rec.get("metadata") or {}
                title = meta.get("title") or ""
                doi = rec.get("doi") or meta.get("doi")
                resource = meta.get("resource_type") or {}
                files = rec.get("files") or []
                if rid not in seen:
                    rout = {"id": rid, "title": title, "doi": doi, "resource_type": resource, "files": []}
                    for f in files:
                        key = f.get("key") or ""
                        links = f.get("links") or {}
                        fileurl = links.get("self") or links.get("download") or key
                        rout["files"].append({"key": key, "size": f.get("size"), "checksum": f.get("checksum"), "url": fileurl})
                        out["candidate_checks"].append(data_like_candidate("Zenodo_file", fileurl or key, f"{title} {key}"))
                    out["records"].append(rout)
                    seen.add(rid)
        except Exception as exc:
            qout["error"] = repr(exc)
            qout["ok"] = False
            out["ok"] = False
        out["queries"].append(qout)
    return out


def run(ctts_root: Path):
    result = {
        "schema": SCHEMA,
        "issue": 196,
        "score_free": True,
        "r5_score_computed": False,
        "voynich_data_accessed": False,
        "manuscript_ocr_performed": False,
        "channels": {},
    }
    result["channels"]["ctts"] = audit_ctts(ctts_root)
    result["channels"]["crossref"] = audit_crossref()
    result["channels"]["publisher"] = audit_publisher()
    result["channels"]["github"] = audit_github()
    result["channels"]["zenodo"] = audit_zenodo()
    checks = []
    for name, ch in result["channels"].items():
        for c in ch.get("candidate_checks") or []:
            checks.append(c)
    positives = [x for x in checks if x.get("positive_candidate")]
    result["candidate_checks"] = checks
    result["positive_candidates"] = positives
    required = {k: bool(result["channels"][k].get("ok")) for k in ("ctts", "crossref", "github", "zenodo")}
    result["required_channel_success"] = required
    if positives:
        result["classification"] = "PUBLIC_MACHINE_READABLE_MARY_CASTELNAU_SOURCE_LOCATED"
        result["next_step"] = "FREEZE_FIVE_LAYER_STRUCTURAL_GATE0"
    elif all(required.values()):
        result["classification"] = "SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE"
        result["next_step"] = "MOVE_TO_DECRYPT_HISTOCRYPT_SHARED_TASK_SCREEN"
    else:
        result["classification"] = "SOURCE_ACCESS_SCREEN_INDETERMINATE"
        result["next_step"] = "DO_NOT_SCORE_R5"
    return result


def self_test():
    a = data_like_candidate("toy", "Mary-Castelnau-transcription.zip", "corpus transcription")
    assert a["positive_candidate"]
    b = data_like_candidate("toy", "Mary-Castelnau-paper.pdf", "article transcription discussion")
    assert not b["positive_candidate"]
    c = data_like_candidate("toy", "software.zip", "CTTS software release", inherited_source=True)
    assert not c["positive_candidate"]
    print(json.dumps({"schema": SCHEMA, "self_test": "PASS"}, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--ctts-root")
    ap.add_argument("--output")
    args = ap.parse_args()
    if args.self_test:
        self_test(); return
    if not args.run or not args.ctts_root or not args.output:
        ap.error("--run requires --ctts-root and --output")
    out = run(Path(args.ctts_root))
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out.get("classification"),
        "next_step": out.get("next_step"),
        "required_channel_success": out.get("required_channel_success"),
        "positive_candidate_count": len(out.get("positive_candidates", [])),
        "publisher_ok": out.get("channels", {}).get("publisher", {}).get("ok"),
        "ctts_path_hits": out.get("channels", {}).get("ctts", {}).get("path_hits"),
        "ctts_content_hit_count": len(out.get("channels", {}).get("ctts", {}).get("content_hits", [])),
        "github_hit_count": sum(len(q.get("items", [])) for q in out.get("channels", {}).get("github", {}).get("queries", [])),
        "zenodo_record_count": len(out.get("channels", {}).get("zenodo", {}).get("records", [])),
        "r5_score_computed": out.get("r5_score_computed"),
    }, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
