#!/usr/bin/env python3
"""Check that the explicit Lean source rows match the attributed fixed data.

This is a provenance cross-check, not a replacement for the Lean kernel.
"""
import json
import re
from pathlib import Path

proof = Path(__file__).resolve().parent
data = json.loads((proof.parent / 'data' / 'arc-core.json').read_text(encoding='utf-8'))
basis = data['lower_basis'] + data['lower_basis'].upper()
index = {letter: i for i, letter in enumerate(basis)}


def section(source, name, next_name):
    return source.split('def ' + name, 1)[1].split('def ' + next_name, 1)[0]


def require(condition, message):
    if not condition:
        raise ValueError(message)


c_source = (proof / 'FiniteCore.lean').read_text(encoding='utf-8')
for function, data_name in [('cLeft', 'left_corners'), ('cRight', 'right_corners')]:
    following = 'cRight' if function == 'cLeft' else 'cNonunit'
    rows = section(c_source, function, following)
    actual = {int(a): int(b) for a, b in re.findall(r'\| (\d+) => (\d+)', rows)}
    expected = {index[a]: index[b] for a, b in data[data_name].items()}
    require(actual == expected, f'{function} corner transcription differs')

nonunit_rows = section(c_source, 'cNonunit', 'cTerms')
actual_products = {}
for a, b, values in re.findall(r'\| (\d+), (\d+) => \[([^\]]+)\]', nonunit_rows):
    actual_products[int(a), int(b)] = {
        int(v): int(coefficient)
        for v, coefficient in re.findall(r'\((\d+), (\d+)\)', values)
    }
expected_products = {
    (index[word[0]], index[word[1]]): {
        index[v]: sum(1 << exponent for exponent in powers)
        for v, powers in outputs.items()
    }
    for word, outputs in data['nonunit_products'].items()
}
require(actual_products == expected_products, 'C product transcription differs')

p_source = (proof / 'CochainData.lean').read_text(encoding='utf-8')
p_rows = section(p_source, 'pTerms', 'radicalIndex')
actual_p = [tuple(map(int, row)) for row in re.findall(
    r'\| (\d+), (\d+), (\d+) => \[\((\d+), (\d+)\)\]', p_rows)]
expected_p = [tuple(index[a] for a in word) + (1 << exponent,)
              for word, exponent in data['cochain_entries']]
require(actual_p == expected_p, '179-entry cochain transcription differs')
require('| _, _, _ => []' in p_rows, 'Unlisted cochain entries are not explicitly zero')

entry_rows = p_source.split('def pEntries', 1)[1].split('theorem p_entry_count', 1)[0]
actual_entries = [tuple(map(int, row)) for row in re.findall(
    r'\((\d+), (\d+), (\d+), (\d+), (\d+)\)', entry_rows)]
require(actual_entries == expected_p, 'Lean pEntries transcription differs')
print('Lean corner tables, all C products, and all 179 cochain source rows match the fixed data.')
