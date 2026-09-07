#!/usr/bin/env python3
"""Pre-effect schema recovery for ORIFLAMMS E1 metadata roster.

The word-aligned authority is a teiCorpus with 102 immediate TEI children. Its
per-document <text> nodes carry no @n, while the metadata authority has 102
numbered <text> records. We permit ordinal association only after every paired
document with a first <pb> has the same IRHT image stem (extension ignored).
No abbreviation counts or positional effects are computed here.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import oriflamms_e1_metadata_inventory as base

NS = base.NS


def pb_stem(text) -> str | None:
    xs = text.xpath('.//tei:pb[@facs]', namespaces=NS)
    if not xs:
        return None
    v = xs[0].get('facs') or ''
    v = v.rsplit('/', 1)[-1]
    return re.sub(r'\.(?:tif|tiff|png|jpe?g)$', '', v, flags=re.I)


def inventory(metadata_path: Path, word_path: Path) -> dict:
    mtree = base.parse_xml(metadata_path)
    wtree = base.parse_xml(word_path)
    meta_texts = base.top_texts(mtree)
    word_teis = wtree.xpath('/tei:teiCorpus/tei:TEI', namespaces=NS)
    if len(meta_texts) != len(word_teis):
        raise RuntimeError(f'authority count mismatch: metadata={len(meta_texts)} word_teis={len(word_teis)}')

    word_texts = []
    pb_pairs = []
    for i, (m, wtei) in enumerate(zip(meta_texts, word_teis), 1):
        ws = wtei.xpath('./tei:text', namespaces=NS)
        if len(ws) != 1:
            raise RuntimeError(f'word TEI ordinal {i} has {len(ws)} direct text nodes')
        wt = ws[0]
        ms = pb_stem(m)
        ws_stem = pb_stem(wt)
        if ms is None or ws_stem is None:
            raise RuntimeError(f'missing first-pb authority at ordinal {i}: metadata={ms} words={ws_stem}')
        if ms != ws_stem:
            raise RuntimeError(f'first-pb mismatch at ordinal {i}: metadata={ms} words={ws_stem}')
        pb_pairs.append({'ordinal_1based': i, 'metadata_text_n': m.get('n'), 'pb_stem': ms})
        word_texts.append(wt)

    records = []
    for ordinal, (m, wt) in enumerate(zip(meta_texts, word_texts), 1):
        rec = base.metadata_record(m)
        rec['ordinal_1based'] = ordinal
        rec['metadata_text_unique'] = True
        rec['word_text_unique'] = True
        rec['association_rule'] = 'ordinal after all-102 first-pb stem identity assertion'
        rec['association_pb_stem'] = pb_stem(m)
        rec['has_lb'] = bool(wt.xpath('.//tei:lb', namespaces=NS))
        rec['has_w'] = bool(wt.xpath('.//tei:w', namespaces=NS))
        rec['has_valid_choice'] = bool(wt.xpath('.//tei:choice[tei:abbr and tei:expan]', namespaces=NS))

        reasons = []
        if not rec['manuscript_identity_unambiguous']:
            reasons.append('AMBIGUOUS_MANUSCRIPT_IDENTITY')
        if rec['date_status'] not in {'OK', 'OK_DUPLICATE_SAME_DATE'}:
            reasons.append(rec['date_status'])
        if rec['earliest'] is not None and rec['latest'] is not None:
            if not (rec['earliest'] >= 1375 and rec['latest'] <= 1450):
                reasons.append('OUTSIDE_FROZEN_1375_1450_INTERVAL')
        else:
            if not any(x in reasons for x in ('NO_USABLE_DATE', 'DATE_AMBIGUOUS', 'OPEN_ENDED_DATE')):
                reasons.append('NO_CLOSED_DATE_INTERVAL')
        if not rec['has_lb']:
            reasons.append('NO_LB')
        if not rec['has_w']:
            reasons.append('NO_W')
        if not rec['has_valid_choice']:
            reasons.append('NO_VALID_CHOICE')
        rec['eligible'] = not reasons
        rec['exclusion_reasons'] = reasons
        records.append(rec)

    roster = [r for r in records if r['eligible']]
    return {
        'experiment': 'LM-A0 ORIFLAMMS E1 metadata-only inventory — ordinal schema recovery',
        'selection_rule': 'closed date interval fully contained in 1375-1450 plus unique manuscript identity and structural presence of lb/w/valid choice',
        'effect_statistics_computed': False,
        'association_authority': {
            'metadata_count': len(meta_texts),
            'word_tei_count': len(word_teis),
            'all_first_pb_stems_match': True,
            'matched_pair_count': len(pb_pairs),
        },
        'eligible_manuscript_count': len(roster),
        'eligible_roster': roster,
        'all_records': records,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('metadata', type=Path)
    ap.add_argument('words', type=Path)
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    r = inventory(args.metadata, args.words)
    s = json.dumps(r, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.write_text(s, encoding='utf-8')
    else:
        print(s)


if __name__ == '__main__':
    main()
