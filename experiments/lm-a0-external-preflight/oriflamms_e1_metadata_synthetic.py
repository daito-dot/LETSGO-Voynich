#!/usr/bin/env python3
from pathlib import Path
from oriflamms_e1_metadata_inventory import inventory

base = Path('/tmp/oriflamms_e1_synth_literal')
(base / 'texts').mkdir(parents=True, exist_ok=True)
meta = '''<?xml version="1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><group><text n="1"><body><listWit><witness><msDesc><msIdentifier><settlement>X</settlement><repository>Y</repository><idno>Z</idno></msIdentifier><physDesc><scriptDesc><scriptNote script="Cursiva"/></scriptDesc></physDesc><history><origin><date when="1410"/></origin></history></msDesc></witness></listWit></body></text></group></text></TEI>'''
words = '''<?xml version="1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><group><text n="1"><body><p><lb/><w><choice><abbr>x</abbr><expan>xyz</expan></choice></w></p></body></text></group></text></TEI>'''
(base / 'mss-dates.xml').write_text(meta, encoding='utf-8')
(base / 'texts' / 'mss-dates-w.xml').write_text(words, encoding='utf-8')
r = inventory(base / 'mss-dates.xml', base / 'texts' / 'mss-dates-w.xml')
assert r['eligible_manuscript_count'] == 1, r
assert r['eligible_roster'][0]['earliest'] == 1410
assert r['effect_statistics_computed'] is False
print('SYNTHETIC_METADATA_PREFLIGHT_OK')
