#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
from lxml import etree

NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
XML_ID = '{http://www.w3.org/XML/1998/namespace}id'

ap = argparse.ArgumentParser()
ap.add_argument('metadata', type=Path)
ap.add_argument('words', type=Path)
args = ap.parse_args()
parser = etree.XMLParser(load_dtd=True, resolve_entities=True, no_network=True, recover=False, huge_tree=True)
mt = etree.parse(str(args.metadata), parser)
parser2 = etree.XMLParser(load_dtd=True, resolve_entities=True, no_network=True, recover=False, huge_tree=True)
wt = etree.parse(str(args.words), parser2)

meta = mt.xpath('/tei:TEI/tei:text/tei:group/tei:text', namespaces=NS)
word_teis = wt.xpath('/tei:teiCorpus/tei:TEI', namespaces=NS)

def one_text(el):
    if el is None:
        return None
    s=' '.join(''.join(el.itertext()).split())
    return s or None

def first_attr(el, xpath, attr):
    xs=el.xpath(xpath, namespaces=NS)
    return xs[0].get(attr) if xs else None

pairs=[]
for i,(m,w) in enumerate(zip(meta, word_teis)):
    ms=m.xpath('.//tei:listWit/tei:witness/tei:msDesc', namespaces=NS)
    ms=ms[0] if len(ms)==1 else None
    pairs.append({
        'ordinal_1based': i+1,
        'metadata_text_n': m.get('n'),
        'metadata_settlement': one_text(ms.find('tei:msIdentifier/tei:settlement', NS)) if ms is not None else None,
        'metadata_repository': one_text(ms.find('tei:msIdentifier/tei:repository', NS)) if ms is not None else None,
        'metadata_idno': one_text(ms.find('tei:msIdentifier/tei:idno', NS)) if ms is not None else None,
        'metadata_first_pb_facs': first_attr(m, './/tei:pb', 'facs'),
        'word_tei_xml_id': w.get(XML_ID),
        'word_tei_n': w.get('n'),
        'word_first_pb_facs': first_attr(w, './/tei:pb', 'facs'),
        'word_first_lb_facs': first_attr(w, './/tei:lb', 'facs'),
        'word_first_w_facs': first_attr(w, './/tei:w', 'facs'),
        'word_header_title': one_text((w.xpath('./tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title', namespaces=NS) or [None])[0]),
    })

print(json.dumps({
    'metadata_count': len(meta),
    'word_tei_count': len(word_teis),
    'counts_equal': len(meta)==len(word_teis),
    'first_20_ordinal_pairs': pairs[:20],
}, ensure_ascii=False, indent=2))
