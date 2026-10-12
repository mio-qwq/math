#!/usr/bin/env python3
"""Read-only finite dependency audit for the universal written width lemma."""
import hashlib
import json
from pathlib import Path


def rows():
    return [(1 << ((j+17) % 32)) ^ (1 << ((j+19) % 32))
            ^ ((1 << (j+10)) if j+10 < 32 else 0) for j in range(32)]


def audit(input_boundary=18, output_boundary=22, top_row=None, highest_q=15):
    r = rows()
    for j in range(output_boundary, 31):
        assert r[j] == (1 << (j-15)) ^ (1 << (j-13))
        assert r[j] >> input_boundary == 0
    assert r[31] == (1 << 16) ^ (1 << 18)
    assert (r[31] if top_row is None else top_row) == (1 << 16) ^ (1 << 18)
    high_differences = []
    for i in range(input_boundary, 32):
        image = sum(((row >> i) & 1) << j for j, row in enumerate(r))
        assert (image >> output_boundary) & 0x1ff == 0
        assert image >> 31 == int(i == 18)
        high_differences.append({'input_basis_bit': i, 'sigma1_image': f'{image:08x}'})
    N, width = 1 << 32, 1 << 22
    assert 3 * 2 * width < N
    assert ((width-1) >> input_boundary) == highest_q
    assert highest_q == 15
    # The signs of H are the same modular residue.
    assert ((1 << 31) - (-(1 << 31))) % N == 0
    return {'input_divisibility': input_boundary, 'sigma1_shared_output_bits': [22, 30],
            'top_changed_bit_identity': [16, 18], 'remaining_low_bits': 22,
            'integer_quotients': list(range(1, 16)), 'high_basis_images': high_differences}


def main():
    result = {'status': 'PASS', 'dependency_audit': audit(), 'negative_controls': []}
    for name, args in [('input_boundary_17', {'input_boundary': 17}),
                       ('output_boundary_21', {'output_boundary': 21}),
                       ('wrong_top_bit', {'top_row': (1 << 16) ^ (1 << 17)}),
                       ('omitted_quotient_15', {'highest_q': 14})]:
        try:
            audit(**args)
        except AssertionError:
            result['negative_controls'].append({'case': name, 'rejected': True})
        else:
            raise AssertionError('accepted damaged width premise '+name)
    here = Path(__file__).resolve().parent
    result['source_sha256'] = {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                               for name in ['PROOF.md', 'check.py']}
    result['scope'] = 'written width reduction with finite row audit; independent review pending'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
