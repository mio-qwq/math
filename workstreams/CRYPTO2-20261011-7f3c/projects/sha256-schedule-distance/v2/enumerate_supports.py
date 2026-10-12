#!/usr/bin/env python3
"""Discovery: depth-first traversal of tight edges of the frozen v1 potential."""
import argparse
import base64
import json
from pathlib import Path
import zlib


def enumerate_supports(cert):
    raw = zlib.decompress(base64.b64decode(cert['potentials_zlib_base64']))
    v = [raw[i*65536:(i+1)*65536] for i in range(49)]
    starts = [q for q in range(1, 65536) if q.bit_count()+v[0][q] == 13]
    supports, visits = [], 0

    def visit(t, q, support):
        nonlocal visits
        visits += 1
        if t == 64:
            supports.append(support)
            return
        n = sum((q >> j) & 1 for j in (0, 1, 9, 14))
        for b in (0, 1):
            nxt = (q >> 1) | (b << 15)
            if n+b != 1 and v[t-16][q] == b+v[t-15][nxt]:
                visit(t+1, nxt, support+([t] if b else []))

    for q in starts:
        visit(16, q, [j for j in range(16) if (q >> j) & 1])
    return dict(schema='sha256-minimum-supports-v2', bound=13,
                start_states=starts, visited_nodes=visits, supports=supports)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    cert = json.loads((Path(__file__).resolve().parent.parent/'certificate.json').read_text())
    args.output.write_text(json.dumps(enumerate_supports(cert), indent=2)+'\n')
