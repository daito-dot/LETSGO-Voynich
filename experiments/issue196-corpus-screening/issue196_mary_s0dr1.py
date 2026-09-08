#!/usr/bin/env python3
"""Issue #196 Mary Stuart/Castelnau S0-D-R1 transport-only recovery.

Repairs failed GitHub/Zenodo discovery transports without changing frozen
identifiers, candidate semantics, or source boundaries. No R5/Voynich score.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import time
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "issue196_mary_s0d.py"
spec = importlib.util.spec_from_file_location("mary_s0d_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

SCHEMA = "issue196-mary-stuart-s0dr1-v1"
REPO_API = "https://api.github.com/users/GeorgeLasry/repos"
MAX_REPO_PAGES = 5
PER_PAGE = 100
MAX_SCAN_BYTES = 2_000_000
FROZEN_IDENTIFIERS = [
    "Mary Stuart",
    "Castelnau",
    "Mary-Castelnau",
    "F38",
    "fr. 2988",
    "2988 f.38",
    "20506",
]
SCAN_EXTS = set(base.TEXT_SCAN_EXTS) | set(base.DATA_EXTS)
ZENODO_IDENTIFIERS = [base.DOI, base.TITLE_ASCII, "Mary Castelnau cipher"]


def github_headers():
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    tok = os.environ.get("GH_DISCOVERY_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def fetch_repo_population():
    repos = []
    pages = []
    for page in range(1, MAX_REPO_PAGES + 1):
        qs = urllib.parse.urlencode({
            "type": "owner",
            "sort": "full_name",
            "direction": "asc",
            "per_page": PER_PAGE,
            "page": page,
        })
        url = f"{REPO_API}?{qs}"
        r = base.fetch(url, github_headers())
        entry = {"page": page, "url": url, "ok": r.get("ok"), "status": r.get("status")}
        if not r.get("ok"):
            entry["error"] = r.get("error")
            pages.append(entry)
            return {"ok": False, "pages": pages, "repos": repos, "error": f"repo_list_page_{page}_failed"}
        try:
            arr = json.loads(r["data"].decode("utf-8"))
            if not isinstance(arr, list):
                raise ValueError("repository list response is not an array")
        except Exception as exc:
            entry["error"] = repr(exc)
            pages.append(entry)
            return {"ok": False, "pages": pages, "repos": repos, "error": f"repo_list_page_{page}_parse_failed"}
        entry["count"] = len(arr)
        pages.append(entry)
        repos.extend(arr)
        if len(arr) < PER_PAGE:
            return {"ok": True, "pages": pages, "repos": repos}
    return {"ok": False, "pages": pages, "repos": repos, "error": "repository_page_cap_reached"}


def bounded_context(text: str, idx: int, term: str) -> str:
    a = max(0, idx - 120)
    b = min(len(text), idx + len(term) + 120)
    return " ".join(text[a:b].split())[:240]


def scan_repo(repo: dict, work_root: Path):
    full_name = repo.get("full_name")
    default_branch = repo.get("default_branch")
    size = repo.get("size")
    out = {
        "full_name": full_name,
        "fork": bool(repo.get("fork")),
        "archived": bool(repo.get("archived")),
        "size_kb_api": size,
        "default_branch": default_branch,
        "status": None,
        "head_commit": None,
        "path_hits": [],
        "content_hits": [],
        "candidate_checks": [],
    }
    if size == 0 or not default_branch:
        out["status"] = "EMPTY_REPOSITORY"
        return out
    clone_url = repo.get("clone_url") or f"https://github.com/{full_name}.git"
    dest = work_root / str(repo.get("id") or full_name.replace("/", "__"))
    if dest.exists():
        shutil.rmtree(dest)
    proc = subprocess.run(
        ["git", "clone", "--depth", "1", "--single-branch", "--branch", str(default_branch), "--quiet", str(clone_url), str(dest)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=300,
    )
    if proc.returncode != 0:
        out["status"] = "CLONE_FAILED"
        out["clone_stderr"] = proc.stderr[-1000:]
        return out
    try:
        head = subprocess.check_output(["git", "-C", str(dest), "rev-parse", "HEAD"], text=True).strip()
        out["head_commit"] = head
    except Exception as exc:
        out["status"] = "HEAD_FAILED"
        out["error"] = repr(exc)
        return out

    folded_terms = [(term, term.casefold()) for term in FROZEN_IDENTIFIERS]
    for p in sorted(dest.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = p.relative_to(dest).as_posix()
        rel_fold = rel.casefold()
        for term, folded in folded_terms:
            if folded in rel_fold:
                hit = {"path": rel, "identifier": term}
                out["path_hits"].append(hit)
                out["candidate_checks"].append(base.data_like_candidate(
                    "GitHub_repo_path", f"{full_name}/{rel}", f"identifier={term}"
                ))
        try:
            stat = p.stat()
        except OSError:
            continue
        if stat.st_size > MAX_SCAN_BYTES or p.suffix.casefold() not in SCAN_EXTS:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except Exception:
            continue
        text_fold = text.casefold()
        for term, folded in folded_terms:
            idx = text_fold.find(folded)
            if idx >= 0:
                context = bounded_context(text, idx, term)
                hit = {"path": rel, "identifier": term, "context": context}
                out["content_hits"].append(hit)
                out["candidate_checks"].append(base.data_like_candidate(
                    "GitHub_repo_content", f"{full_name}/{rel}", context
                ))
    out["status"] = "SCANNED"
    shutil.rmtree(dest, ignore_errors=True)
    return out


def audit_github_recovery(work_root: Path):
    pop = fetch_repo_population()
    out = {
        "ok": False,
        "population_pages": pop.get("pages", []),
        "repository_count": len(pop.get("repos", [])),
        "repositories": [],
        "candidate_checks": [],
    }
    if not pop.get("ok"):
        out["error"] = pop.get("error")
        return out
    work_root.mkdir(parents=True, exist_ok=True)
    all_ok = True
    for repo in pop["repos"]:
        r = scan_repo(repo, work_root)
        out["repositories"].append(r)
        out["candidate_checks"].extend(r.get("candidate_checks") or [])
        if r.get("status") not in {"SCANNED", "EMPTY_REPOSITORY"}:
            all_ok = False
    out["ok"] = all_ok
    if not all_ok:
        out["error"] = "one_or_more_nonempty_repositories_failed"
    return out


def zenodo_url(q: str):
    return "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": q, "size": 25})


def retriable(r):
    status = r.get("status")
    return status == 429 or (isinstance(status, int) and status >= 500)


def fetch_zenodo_identifier(identifier: str, is_doi: bool):
    attempts = []
    success = None
    plain_url = zenodo_url(identifier)
    delays = [5, 15]
    for i in range(3):
        r = base.fetch(plain_url, {"Accept": "application/json"})
        attempts.append({"mode": "plain", "attempt": i + 1, "url": plain_url, "ok": r.get("ok"), "status": r.get("status"), "error": r.get("error")})
        if r.get("ok"):
            success = r
            break
        if not retriable(r):
            return {"ok": False, "attempts": attempts, "error": "non_retriable_plain_failure"}
        if i < 2:
            time.sleep(delays[i])
    if success is None:
        quoted = f'"{identifier}"'
        qurl = zenodo_url(quoted)
        r = base.fetch(qurl, {"Accept": "application/json"})
        attempts.append({"mode": "quoted", "attempt": 1, "url": qurl, "ok": r.get("ok"), "status": r.get("status"), "error": r.get("error")})
        if r.get("ok"):
            success = r
        elif not retriable(r):
            return {"ok": False, "attempts": attempts, "error": "non_retriable_quoted_failure"}
        elif is_doi:
            fielded = f'doi:"{identifier}"'
            furl = zenodo_url(fielded)
            r2 = base.fetch(furl, {"Accept": "application/json"})
            attempts.append({"mode": "doi_field", "attempt": 1, "url": furl, "ok": r2.get("ok"), "status": r2.get("status"), "error": r2.get("error")})
            if r2.get("ok"):
                success = r2
            else:
                return {"ok": False, "attempts": attempts, "error": "doi_field_failure"}
        else:
            return {"ok": False, "attempts": attempts, "error": "quoted_failure"}
    try:
        obj = json.loads(success["data"].decode("utf-8"))
        hits = (obj.get("hits") or {}).get("hits") or []
    except Exception as exc:
        return {"ok": False, "attempts": attempts, "error": f"json_parse:{exc!r}"}
    return {"ok": True, "attempts": attempts, "hits": hits}


def audit_zenodo_recovery():
    out = {"ok": True, "queries": [], "records": [], "candidate_checks": []}
    seen = set()
    for identifier in ZENODO_IDENTIFIERS:
        res = fetch_zenodo_identifier(identifier, identifier == base.DOI)
        qout = {"identifier": identifier, "ok": res.get("ok"), "attempts": res.get("attempts", [])}
        if not res.get("ok"):
            qout["error"] = res.get("error")
            out["ok"] = False
            out["queries"].append(qout)
            continue
        hits = res.get("hits") or []
        qout["hit_count_returned"] = len(hits)
        for rec in hits:
            rid = rec.get("id")
            meta = rec.get("metadata") or {}
            title = meta.get("title") or ""
            doi = rec.get("doi") or meta.get("doi")
            resource = meta.get("resource_type") or {}
            files = rec.get("files") or []
            if rid in seen:
                continue
            seen.add(rid)
            rout = {"id": rid, "title": title, "doi": doi, "resource_type": resource, "files": []}
            for f in files:
                key = f.get("key") or ""
                links = f.get("links") or {}
                locator = links.get("self") or links.get("download") or key
                rout["files"].append({"key": key, "size": f.get("size"), "checksum": f.get("checksum"), "url": locator})
                out["candidate_checks"].append(base.data_like_candidate(
                    "Zenodo_file", locator or key, f"{title} {key}"
                ))
            out["records"].append(rout)
        out["queries"].append(qout)
    return out


def run(ctts_root: Path, work_root: Path):
    result = {
        "schema": SCHEMA,
        "issue": 196,
        "score_free": True,
        "r5_score_computed": False,
        "voynich_data_accessed": False,
        "manuscript_ocr_performed": False,
        "recovery_scope": "transport_only",
        "channels": {},
    }
    result["channels"]["ctts"] = base.audit_ctts(ctts_root)
    result["channels"]["crossref"] = base.audit_crossref()
    result["channels"]["github"] = audit_github_recovery(work_root / "github")
    result["channels"]["zenodo"] = audit_zenodo_recovery()
    checks = []
    for ch in result["channels"].values():
        checks.extend(ch.get("candidate_checks") or [])
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
    assert base.data_like_candidate("toy", "Mary-Castelnau-transcription.zip", "corpus transcription")["positive_candidate"]
    assert not base.data_like_candidate("toy", "Mary-Castelnau-paper.pdf", "article transcription discussion")["positive_candidate"]
    assert retriable({"status": 429}) and retriable({"status": 500}) and not retriable({"status": 404})
    assert len(FROZEN_IDENTIFIERS) == 7
    print(json.dumps({"schema": SCHEMA, "self_test": "PASS"}, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--ctts-root")
    ap.add_argument("--work-root", default="issue196_mary_s0dr1_work")
    ap.add_argument("--output")
    args = ap.parse_args()
    if args.self_test:
        self_test(); return
    if not args.run or not args.ctts_root or not args.output:
        ap.error("--run requires --ctts-root and --output")
    out = run(Path(args.ctts_root), Path(args.work_root))
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    g = out.get("channels", {}).get("github", {})
    z = out.get("channels", {}).get("zenodo", {})
    print(json.dumps({
        "classification": out.get("classification"),
        "next_step": out.get("next_step"),
        "required_channel_success": out.get("required_channel_success"),
        "positive_candidate_count": len(out.get("positive_candidates", [])),
        "github_repository_count": g.get("repository_count"),
        "github_path_hit_count": sum(len(r.get("path_hits", [])) for r in g.get("repositories", [])),
        "github_content_hit_count": sum(len(r.get("content_hits", [])) for r in g.get("repositories", [])),
        "zenodo_record_count": len(z.get("records", [])),
        "r5_score_computed": out.get("r5_score_computed"),
    }, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
