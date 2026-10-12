#!/usr/bin/env python3
"""Check the four-word object from output-bit definitions; no solver imports."""
import argparse
import copy
import json
from pathlib import Path

MASK = (1 << 32) - 1
HERE = Path(__file__).resolve().parent


def sigma(word, r, s, shift):
    assert isinstance(word, int) and 0 <= word <= MASK
    result = 0
    for i in range(32):
        bit = ((word >> ((i + r) % 32)) ^
               (word >> ((i + s) % 32)) ^
               (word >> (i + shift) if i + shift < 32 else 0)) & 1
        result |= bit << i
    return result


def inspect(words, constants=(7, 18, 3, 17, 19, 10)):
    assert set(words) == {'p', 'pp', 'q', 'qp'}
    assert all(isinstance(v, str) and len(v) == 8 for v in words.values())
    values = {k: int(v, 16) for k, v in words.items()}
    outputs = {k: {'f': sigma(v, *constants[:3]), 'g': sigma(v, *constants[3:])}
               for k, v in values.items()}
    dp = (values['pp'] - values['p']) & MASK
    dq = (values['qp'] - values['q']) & MASK
    fp = (outputs['pp']['f'] - outputs['p']['f']) & MASK
    fq = (outputs['qp']['f'] - outputs['q']['f']) & MASK
    gq = (outputs['qp']['g'] - outputs['q']['g']) & MASK
    assert dp == dq != 0, 'unequal input differences'
    assert gq == (-dq & MASK), 'q cancellation'
    assert fp == (-fq & MASK), 'opposite sigma0 differences'
    valuation = (dq & -dq).bit_length() - 1
    assert valuation == 11, 'claimed valuation'
    return {'words': words, 'outputs': {k: {m: f'{v:08x}' for m, v in pair.items()}
                                      for k, pair in outputs.items()},
            'D': f'{dq:08x}', 'Fp': f'{fp:08x}', 'Fq': f'{fq:08x}',
            'Gq': f'{gq:08x}', 'valuation': valuation,
            'scope': 'four-word local witness, not a message-pair witness'}


def verify(obj, constants=(7, 18, 3, 17, 19, 10)):
    assert obj == inspect(obj['words'], constants)


def rejects(action):
    try:
        action()
    except (AssertionError, ValueError, KeyError):
        return True
    raise AssertionError('damaged control accepted')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    raw = json.loads((HERE/'RUN.json').read_text())
    assert raw['status'] == 'sat'
    obj = inspect(raw['words'])
    if args.build:
        (HERE/'WITNESS.json').write_text(json.dumps(obj, indent=2)+'\n')
    frozen = json.loads((HERE/'WITNESS.json').read_text())
    verify(frozen)
    controls = 0
    if args.negative:
        for word in ('p', 'pp', 'q', 'qp'):
            bad = copy.deepcopy(frozen)
            bad['words'][word] = f"{int(bad['words'][word], 16) ^ 1:08x}"
            rejects(lambda: verify(bad))
            controls += 1
        bad = copy.deepcopy(frozen)
        bad['D'] = f"{int(bad['D'], 16) ^ 2048:08x}"
        rejects(lambda: verify(bad))
        controls += 1
        rejects(lambda: verify(frozen, (8, 18, 3, 17, 19, 10)))
        controls += 1
        rejects(lambda: verify(frozen, (7, 18, 3, 17, 20, 10)))
        controls += 1
        bad = copy.deepcopy(frozen)
        bad['outputs']['qp']['f'] = f"{int(bad['outputs']['qp']['f'], 16) ^ 1:08x}"
        rejects(lambda: verify(bad))
        controls += 1
    print(json.dumps({'status': 'PASS', 'D': obj['D'], 'valuation': 11,
                      'negative_controls': controls, 'object': obj}, sort_keys=True))


if __name__ == '__main__':
    main()
