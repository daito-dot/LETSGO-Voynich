#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
from lxml import etree

NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
XML_ID = '{http://www.w3.org/XML/1998/namespace}id'

ap = argparse.ArgumentParser()
ap.add_argument('xml', type=Path)
args = ap.parse_args()
parser = etree.XMLParser(load_dtd=True, resolve_entities=True, no_network=True, recover=False, huge_tree=True)
tree = etree.parse(str(args.xml), parser)
root = tree.getroot()

def q(expr):
    return tree.xpath(expr, namespaces=NS)

all_texts = q('//tei:text')
all_divs = q('//tei:div')
all_bodies = q('//tei:body')
summary = {
    'root_tag': root.tag,
    'root_child_tags': [c.tag for c in list(root)[:20] if isinstance(c.tag, str)],
    'text_count_anywhere': len(all_texts),
    'body_count_anywhere': len(all_bodies),
    'div_count_anywhere': len(all_divs),
    'first_text_descriptors': [
        {
            'n': t.get('n'),
            'xml_id': t.get(XML_ID),
            'type': t.get('type'),
            'child_tags': [c.tag for c in list(t)[:10] if isinstance(c.tag, str)],
        }
        for t in all_texts[:12]
    ],
    'first_body_descriptors': [
        {
            'n': b.get('n'),
            'xml_id': b.get(XML_ID),
            'type': b.get('type'),
            'child_tags': [c.tag for c in list(b)[:10] if isinstance(c.tag, str)],
        }
        for b in all_bodies[:12]
    ],
    'first_div_descriptors': [
        {
            'n': d.get('n'),
            'xml_id': d.get(XML_ID),
            'type': d.get('type'),
            'corresp': d.get('corresp'),
            'facs': d.get('facs'),
            'child_tags': [c.tag for c in list(d)[:10] if isinstance(c.tag, str)],
        }
        for d in all_divs[:20]
    ],
    'text_attribute_keys': sorted({k for t in all_texts for k in t.attrib}),
    'body_attribute_keys': sorted({k for b in all_bodies for k in b.attrib}),
    'div_attribute_keys': sorted({k for d in all_divs for k in d.attrib}),
}
print(json.dumps(summary, ensure_ascii=False, indent=2))
