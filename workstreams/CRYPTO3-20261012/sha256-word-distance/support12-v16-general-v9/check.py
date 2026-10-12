#!/usr/bin/env python3
"""Exact affine/carry classification for odd q <= 31 at D=q*2^16."""
import argparse
from collections import Counter
from functools import cache
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
N = 1 << 32
MASK = N - 1
WIDTH = 64
COEFF = (1 << WIDTH) - 1
QS = tuple(range(1, 32, 2))


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma_direct(x, kind):
    if kind == 0:
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def rows(kind):
    a, b, s = ((7, 18, 3), (17, 19, 10))[kind]
    return tuple(
        (1 << ((j + a) % 32))
        ^ (1 << ((j + b) % 32))
        ^ ((1 << (j + s)) if j + s < 32 else 0)
        for j in range(32)
    )


ROWS = (rows(0), rows(1))


def sigma_rows(x, kind):
    return sum(((r & x).bit_count() & 1) << j for j, r in enumerate(ROWS[kind]))


@cache
def input_classes(q):
    """Return exact affine cubes for upper-half addition by odd q."""
    groups = {}
    for u in range(1 << 16):
        alpha = (u ^ ((u + q) & 0xffff)) << 16
        groups.setdefault(alpha, []).append(u)
    out = []
    for alpha, us in sorted(groups.items()):
        equations = []
        for j in range(16):
            values = {u >> j & 1 for u in us}
            if len(values) == 1:
                equations.append((1 << (j + 16), next(iter(values))))
        need(len(us) == 1 << (16 - len(equations)), f'q={q}: non-cube class')
        need(all(all(((u << 16) & r).bit_count() & 1 == v
                     for r, v in equations) for u in us),
             f'q={q}: cube member violates equations')
        out.append((alpha, tuple(equations), len(us)))
    need(sum(z for _, _, z in out) == 1 << 16, f'q={q}: incomplete classes')
    return tuple(out)


def affine(allowed, size):
    equations = []
    for r in range(1, 1 << size):
        values = {(r & v).bit_count() & 1 for v in allowed}
        if len(values) == 1:
            equations.append((r, next(iter(values))))
    rebuilt = [v for v in range(1 << size)
               if all((r & v).bit_count() & 1 == b for r, b in equations)]
    need(rebuilt == allowed, 'inexact truth-table compression')
    return equations


def transitions(kind, alpha_x, alpha_y, constant, bit, carry):
    ax = (sigma_rows(alpha_x, kind) >> bit) & 1
    ay = (sigma_rows(alpha_y, kind) >> bit) & 1
    funcs = []
    if ax:
        funcs.append(ROWS[kind][bit])
    if ay:
        funcs.append(ROWS[kind][bit] << 32)
    groups = {}
    for value in range(1 << len(funcs)):
        ux = (value & 1) if ax else 0
        uy = ((value >> ax) & 1) if ay else 0
        integer = carry + ((uy ^ ay) - uy) - ((ux ^ ax) - ux)
        integer -= (constant >> bit) & 1
        if integer % 2 == 0:
            groups.setdefault(integer // 2, []).append(value)
    out = []
    for nxt, allowed in sorted(groups.items()):
        eqs = []
        for little, rhs in affine(allowed, len(funcs)):
            coeff = 0
            for j, row in enumerate(funcs):
                if little >> j & 1:
                    coeff ^= row
            eqs.append((coeff, rhs))
        out.append((nxt, eqs))
    return out


def insert(basis, equations):
    basis = dict(basis)
    for coeff, rhs in equations:
        atom = (coeff, rhs)
        word = coeff | (rhs << WIDTH)
        receipt = frozenset((atom,))
        while word & COEFF:
            pivot = ((word & COEFF) & -(word & COEFF)).bit_length() - 1
            if pivot in basis:
                old, old_receipt = basis[pivot]
                word ^= old
                receipt = receipt.symmetric_difference(old_receipt)
            else:
                basis[pivot] = (word, receipt)
                break
        if word == 1 << WIDTH:
            frozen = tuple(sorted(receipt))
            total = 0
            for c, b in frozen:
                total ^= c | (b << WIDTH)
            need(total == 1 << WIDTH, 'bad contradiction receipt')
            return None, frozen
    return basis, None


def advance(states, kind, alpha_x, alpha_y, constant, bit, stats, receipts):
    follow = []
    for carry, basis in states:
        for nxt, equations in transitions(kind, alpha_x, alpha_y,
                                           constant, bit, carry):
            stats['truth_edges'] += 1
            new_basis, receipt = insert(basis, equations)
            if new_basis is None:
                stats['contradictions'] += 1
                receipts.add(receipt)
            else:
                follow.append((nxt, new_basis))
    return follow


def carry(states, kind, alpha_x, alpha_y, constant, first, last,
          stats, receipts):
    for bit in range(first, last):
        states = advance(states, kind, alpha_x, alpha_y, constant,
                         bit, stats, receipts)
    return states


def recover(basis):
    word = 0
    for pivot, (equation, _) in sorted(basis.items(), reverse=True):
        rhs = equation >> WIDTH
        coeff = equation & COEFF
        if (word & coeff).bit_count() & 1 != rhs:
            word |= 1 << pivot
    return word


def direct_fixture(q, packed):
    d = q << 16
    x = packed & MASK
    y = (packed >> 32) & MASK
    xp = (x + d) & MASK
    yp = (y + d) & MASK
    fx = (sigma_direct(xp, 0) - sigma_direct(x, 0)) & MASK
    fy = (sigma_direct(yp, 0) - sigma_direct(y, 0)) & MASK
    gx = (sigma_direct(xp, 1) - sigma_direct(x, 1)) & MASK
    gy = (sigma_direct(yp, 1) - sigma_direct(y, 1)) & MASK
    need(fx == fy, f'q={q}: recovered sigma0 mismatch')
    need((gy - gx) & MASK == (2 * d) & MASK,
         f'q={q}: recovered sigma1 mismatch')
    return {
        'x': f'{x:08x}', 'x_plus_D': f'{xp:08x}',
        'y': f'{y:08x}', 'y_plus_D': f'{yp:08x}',
        'xor_x': f'{x ^ xp:08x}', 'xor_y': f'{y ^ yp:08x}',
        'common_F': f'{fx:08x}', 'G_x': f'{gx:08x}',
        'G_y': f'{gy:08x}', 'G_gap': f'{(gy-gx)&MASK:08x}',
    }


def classify(q):
    d = q << 16
    stats = Counter()
    receipts = set()
    f_leaves = low31_leaves = full_leaves = 0
    fixtures = []
    class_data = input_classes(q)
    for alpha_x, eq_x, _ in class_data:
        for alpha_y, eq_y, _ in class_data:
            shifted_y = tuple((r << 32, b) for r, b in eq_y)
            basis, receipt = insert({}, eq_x + shifted_y)
            need(basis is not None and receipt is None, 'disjoint cubes conflict')
            states = [(0, basis)]
            states = carry(states, 0, alpha_x, alpha_y, 0, 0, 32,
                           stats, receipts)
            f_leaves += len(states)
            states = [(0, b) for _, b in states]
            states = carry(states, 1, alpha_x, alpha_y, 2 * d, 0, 31,
                           stats, receipts)
            low31_leaves += len(states)
            states = carry(states, 1, alpha_x, alpha_y, 2 * d, 31, 32,
                           stats, receipts)
            full_leaves += len(states)
            for _, surviving_basis in states:
                fixtures.append(direct_fixture(q, recover(surviving_basis)))
    for receipt in receipts:
        total = 0
        for c, b in receipt:
            total ^= c | (b << WIDTH)
        need(total == 1 << WIDTH, f'q={q}: damaged receipt')
    # Multiple affine paths may select the same free-zero representative.
    unique = {json.dumps(x, sort_keys=True): x for x in fixtures}
    fixtures = [unique[k] for k in sorted(unique)]
    return {
        'q': q, 'D': f'{d:08x}', 'input_classes': len(class_data),
        'class_sizes': [z for _, _, z in class_data],
        'sigma0_leaves': f_leaves, 'low31_twin_leaves': low31_leaves,
        'full32_twin_leaves': full_leaves,
        'unique_recovered_fixtures': fixtures,
        'truth_edges': stats['truth_edges'],
        'contradictions': stats['contradictions'],
        'distinct_contradiction_receipts': len(receipts),
    }


def damaged_fixture_rejected(q, fixture):
    keys = ('x_plus_D', 'y_plus_D', 'common_F', 'G_gap')
    rejected = 0
    d = q << 16
    for key in keys:
        bad = dict(fixture)
        bad[key] = f'{int(bad[key], 16) ^ 1:08x}'
        x = int(bad['x'], 16); xp = int(bad['x_plus_D'], 16)
        y = int(bad['y'], 16); yp = int(bad['y_plus_D'], 16)
        try:
            need((xp-x)&MASK == d and (yp-y)&MASK == d, 'difference')
            fx = (sigma_direct(xp,0)-sigma_direct(x,0))&MASK
            fy = (sigma_direct(yp,0)-sigma_direct(y,0))&MASK
            need(fx == fy == int(bad['common_F'],16), 'F')
            gx = (sigma_direct(xp,1)-sigma_direct(x,1))&MASK
            gy = (sigma_direct(yp,1)-sigma_direct(y,1))&MASK
            need((gy-gx)&MASK == int(bad['G_gap'],16) == (2*d)&MASK, 'G')
        except ValueError:
            rejected += 1
    need(rejected == len(keys), f'q={q}: damaged fixture accepted')
    return rejected


def run(negative=False):
    start = time.monotonic()
    for kind in (0, 1):
        for bit in range(32):
            need(sigma_rows(1 << bit, kind) == sigma_direct(1 << bit, kind),
                 'row construction differs from standard sigma')
    cases = [classify(q) for q in QS]
    excluded = [c['q'] for c in cases if c['full32_twin_leaves'] == 0]
    surviving = [c['q'] for c in cases if c['full32_twin_leaves'] != 0]
    controls = {'basis_rows_checked': 64}
    if negative:
        controls['damaged_fixture_fields_rejected'] = sum(
            damaged_fixture_rejected(c['q'], f)
            for c in cases for f in c['unique_recovered_fixtures'])
        controls['excluded_with_low31_frontier'] = [
            c['q'] for c in cases
            if c['low31_twin_leaves'] and not c['full32_twin_leaves']]
    result = {
        'schema': 'CRYPTO3-support12-v16-q1-31-v9',
        'status': 'PASS', 'q_domain': list(QS), 'cases': cases,
        'excluded_positive_q': excluded, 'surviving_positive_q': surviving,
        'negative_orientation': 'pair reversal gives the same classification for -D',
        'controls': controls,
        'scope': ('selected twin core only; survivor is a local pair fixture, '
                  'not the three-pair core, complete support, or message pair'),
        'elapsed_seconds': time.monotonic() - start,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    return result


def comparable(result):
    result = dict(result)
    result.pop('elapsed_seconds', None)
    result.pop('checker_sha256', None)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--write-certificate', action='store_true')
    args = parser.parse_args()
    output = run(args.negative)
    cert_path = HERE / 'CERTIFICATE.json'
    if args.write_certificate:
        cert_path.write_text(json.dumps(comparable(output), indent=2,
                                        sort_keys=True) + '\n')
    else:
        frozen = json.loads(cert_path.read_text())
        need(frozen == comparable(output), 'frozen certificate mismatch')
    print(json.dumps({
        'status': output['status'],
        'excluded_positive_q': output['excluded_positive_q'],
        'surviving_positive_q': output['surviving_positive_q'],
        'controls': output['controls'],
        'elapsed_seconds': output['elapsed_seconds'],
        'certificate_sha256': (hashlib.sha256(cert_path.read_bytes()).hexdigest()
                               if cert_path.exists() else None),
        'checker_sha256': output['checker_sha256'],
    }, sort_keys=True))
