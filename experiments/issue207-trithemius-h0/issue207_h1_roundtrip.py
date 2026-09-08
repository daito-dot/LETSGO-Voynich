#!/usr/bin/env python3
"""Issue #207 external-only H1 round-trip for the frozen Trithemius prefix.

No Voynich data are read. The three consecutive historical alphabets were frozen
in the H0 artifact. This script deliberately stops after three code-bearing
positions: it does not cycle the excerpt, add filler, or exercise restart rules.
"""

import hashlib
import json

ALPHABETS = [
    {"A":"Deus","B":"Creator","C":"Conditor","D":"Opifex","E":"Dominus","F":"Dominator","G":"Consolator","H":"Arbiter","I":"Judex","K":"Illuminator","L":"Illustrator","M":"Rector","N":"Rex","O":"Imperator","P":"Gubernator","Q":"Factor","R":"Fabricator","S":"Conservator","T":"Redemptor","V":"Auctor","W":"Princeps","X":"Pastor","Y":"Moderator","Z":"Salvator"},
    {"A":"Clemens","B":"Clementissimus","C":"Pius","D":"Piissimus","E":"Magnus","F":"Excelsus","G":"Maximus","H":"Optimus","I":"Sapientissimus","K":"Invisibilis","L":"Immortalis","M":"Aeternus","N":"Sempiternus","O":"Gloriosus","P":"Fortissimus","Q":"Sanctissimus","R":"Incomprehensibilis","S":"Omnipotens","T":"Pacificus","V":"Misericors","W":"Misericordissimus","X":"Cunctipotens","Y":"Magnificus","Z":"Excellentissimus"},
    {"A":"Creans","B":"Regens","C":"Conservans","D":"Moderans","E":"Gubernans","F":"Ordinans","G":"Ornans","H":"Exornans","I":"Constituens","K":"Dirigens","L":"Producens","M":"Decorans","N":"Stabiliens","O":"Illustrans","P":"Intuens","Q":"Movens","R":"Confirmans","S":"Custodiens","T":"Cernens","V":"Discernens","W":"Illuminans","X":"Fabricans","Y":"Salvificans","Z":"Faciens"},
]

PLAINTEXT = "ABC"


def canonical_table_bytes() -> bytes:
    return json.dumps(
        ALPHABETS,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def main() -> None:
    assert len(PLAINTEXT) <= len(ALPHABETS)
    cipher_units = [ALPHABETS[i][letter] for i, letter in enumerate(PLAINTEXT)]
    inverses = [{word: letter for letter, word in alphabet.items()} for alphabet in ALPHABETS]
    assert all(len(inv) == len(ALPHABETS[i]) for i, inv in enumerate(inverses))
    recovered = "".join(inverses[i][word] for i, word in enumerate(cipher_units))

    table_bytes = canonical_table_bytes()
    result = {
        "issue": 207,
        "stage": "H1_EXTERNAL_ROUNDTRIP",
        "target_accessed": False,
        "input": PLAINTEXT,
        "cipher_units": cipher_units,
        "recovered": recovered,
        "roundtrip_pass": recovered == PLAINTEXT,
        "alphabet_count": len(ALPHABETS),
        "table_cells": sum(len(a) for a in ALPHABETS),
        "canonical_serialization": "UTF-8 JSON; ensure_ascii=false; sort_keys=true; separators=(comma,colon)",
        "serialized_table_bytes": len(table_bytes),
        "serialized_table_bits": len(table_bytes) * 8,
        "serialized_table_sha256": hashlib.sha256(table_bytes).hexdigest(),
        "cycling_used": False,
        "filler_used": False,
        "restart_used": False,
    }
    assert result["roundtrip_pass"]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
