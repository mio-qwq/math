#!/usr/bin/env python3
"""One bounded local sharpness query; solver output is not a proof premise."""
import json
from pathlib import Path
import sys
import time

import z3


def f(x):
    return z3.RotateRight(x, 7) ^ z3.RotateRight(x, 18) ^ z3.LShR(x, 3)


def g(x):
    return z3.RotateRight(x, 17) ^ z3.RotateRight(x, 19) ^ z3.LShR(x, 10)


def main():
    p, pp, q, qp = z3.BitVecs('p pp q qp', 32)
    delta = qp - q
    solver = z3.SolverFor('QF_BV')
    solver.set(timeout=15000)
    solver.add(pp - p == delta,
               g(qp) - g(q) == -delta,
               f(pp) - f(p) == -(f(qp) - f(q)),
               z3.Extract(11, 0, delta) == z3.BitVecVal(2048, 12))
    started = time.monotonic()
    status = solver.check()
    record = {'schema': 'crypto3-coupled-local-sharpness-v1',
              'solver': 'Z3 ' + z3.get_version_string(),
              'timeout_ms': 15000, 'status': str(status),
              'seconds': time.monotonic() - started,
              'scope': 'four actual words only; no schedule or message pair',
              'statistics': str(solver.statistics())}
    if status == z3.sat:
        model = solver.model()
        record['words'] = {str(v): '%08x' % model.eval(v).as_long()
                           for v in (p, pp, q, qp)}
    elif status == z3.unknown:
        record['reason'] = solver.reason_unknown()
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
