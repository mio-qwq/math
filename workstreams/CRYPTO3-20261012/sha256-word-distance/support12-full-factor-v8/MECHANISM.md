# Mechanism and failure boundary

This stage replaces the former selected three- and four-pair subsystem by
an exact normal form for every original support-12 difference row.

The mechanism is finite symbolic elimination over the integers using only
row swap, row negation and adding an integer multiple of another row.  It
does not invoke SAT, SMT, MILP, random search or a timeout.  Since all 25
pivots are units, the same operations are valid modulo `2^32` and prove a
14-scalar parametrisation with no division.

The final condition is thirteen membership tests in the actual joint
word-pair image `J`.  A membership always keeps `d`, `F` and `G` from one
oriented pair.  The checker deliberately rejects a damaged record that
replaces one pair's `G` equation by its `F` equation.

Failure boundary: no preimages for the thirteen memberships are supplied,
and even simultaneous independent preimages would not complete two common
SHA-256 base schedules.  Thus this stage is an exact reduction, not a
candidate message, a complete support exclusion, or evidence that distance
13 is reachable.

Rebuild and check:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-v8/build_certificate.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-v8/check.py --negative
```

Only Python's standard library is required.  The first command is a
generator and rewrites `CERTIFICATE.json`; the second is the definition
checker and imports no generator code.

