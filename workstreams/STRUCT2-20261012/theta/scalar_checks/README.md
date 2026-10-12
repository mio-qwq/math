# Finite exact regression for the theta maximizer formulas

## Result and scope

The executed run checks every legal unordered path triple at vertex orders
`4 <= n <= 40`: **1,942 triples**. All tested compression comparisons,
strictness conditions, short-path formulas, balancing steps, parity
exclusions, maximizing triples, and closed maximum values agree.

This is a bounded arithmetic regression. It does not certify a universal
theorem, duplicate the separate mathematical review, or enlarge the original
paper's much larger finite enumeration. No graph facet enumeration or Lean
compilation was performed in this run. The pre-existing graph-label checker
was not imported or rerun.

The target expressions were taken from `theta/MAXIMIZERS.md`, 14,079 bytes,
SHA256:

```
c0c02847ae525260d65dd5b11c1ee940b4b63aec6e2167c39fa8a9c12fc12fab
```

This binding records the compared formulas, not acceptance of that
manuscript's universal proof.

## Independent count implementation

The source is Braun--Bruegge, *Journal of Integer Sequences* **26** (2023),
Article 23.7.2, [original PDF](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf):
Proposition 22, Corollary 25 on p. 15, Definition 12 on p. 7, and
Conjecture 33 on p. 24. The downloaded PDF has 360,657 bytes and SHA256:

```
52e4b28b4e4106af07768940e60bb06fdd76f638b288e0139ec7bc5c05dd397a
```

`check_scalar.py` uses only Python's standard library. It imports no
project code or discovery data. For positive same-parity rows, sorted
as `a >= b >= c`, it implements the original shortest-path sum

\[
F(a,b,c)=\sum_{j=0}^{c}\binom cj
 \binom b{(b-c)/2+j}\binom a{(a-c)/2+j}.
\]

Facet counts then use Corollary 25(i)--(iv), with separate clauses for
the path of length one. No zero row is passed to this implementation of
`F`. The centered binomial function `B` is implemented separately for
the target short-path expressions. All arithmetic uses arbitrary-precision
integers or exact `Fraction` values.

The domain is three positive integer lengths with at most one length one,
total length `n + 1`. Each accepted triple also builds its actual edge set
to verify `|V| = n` and `|E| = n + 1` after edge deduplication. This graph
construction checks the parameter domain; it does not count facets.

The cycle formula in the source's boundary clauses is used down to its
length-two, single-edge auxiliary value. No graph meaning is assigned to
`C_1`. Original Definition 12 is evaluated only for `n >= 5`; at `n = 4`
the direct theta maximum is 12 and the `M` field is null.

## What was checked

| Check | Executed instances |
|---|---:|
| Legal unordered triples | 1,942 |
| Even-order compression, both distinct orientations | 1,330 |
| Even-order compression with `z > 1`, all strict | 1,140 |
| Odd-order compression with `x >= 3` | 1,140 |
| Odd-order compression with `z > 2`, all strict | 969 |
| Short odd-path formula `N(p,q,1)` | 100 |
| Short even-path formula `N(x,y,2)` | 99 |
| Strict inward balancing, odd path length one | 81 |
| Strict inward balancing, even path length two | 81 |
| Same-parity triples strictly below the mixed maximum | 531 |
| Orders with the predicted unique unordered maximizer | 37 |
| Closed maximum values | 37 |
| Exact maximum-to-`M` ratios, `n >= 5` | 36 |

Compression counts include both distinct assignments of the same-parity
pair where the asserted conditions allow them. Boundary compressions are
also checked for equality. Inward balancing is tested only when the two
lengths differ by at least four; a difference of two would merely exchange
their unordered values.

For each order, the checker finds the maximum over the entire legal
unordered domain, checks that exactly one triple attains it, and compares
it with the four formulas in the target manuscript. Original Conjecture 33
asks for the maximizing examples only at `n >= 10`; the checks at orders
4 through 9 are explicitly additional finite cases.

| `n` | Unique maximizing unordered triple | Exact maximum |
|---:|---|---:|
| 4 | `(1,2,2)` | 12 |
| 5 | `(1,2,3)` | 24 |
| 6 | `(1,2,4)` | 60 |
| 7 | `(2,3,3)` | 126 |
| 8 | `(1,4,4)` | 324 |
| 9 | `(2,3,5)` | 600 |
| 10 | `(1,4,6)` | 1,560 |
| 20 | `(1,10,10)` | 3,238,704 |
| 30 | `(1,14,16)` | 4,991,191,920 |
| 40 | `(1,20,20)` | 6,861,090,686,736 |

## Targeted damage controls

All three deliberate errors are detected:

1. On `(2,3,3)`, replacing the short even-path coefficient `xy + 5`
   with `xy + 4` gives 117, against the original formula's 126.
2. On the same graph, deleting the `xy` multiplier in Corollary 25(ii)
   gives 46, against 126.
3. `(1,1,4)` is rejected. Its attempted six path edges deduplicate to
   five edges on five vertices, so it is outside the simple bicyclic
   theta domain.

These controls identify specific plausible errors; they do not constitute
a general verification of the implementation.

## Execution and reproducibility

The actual run began at `2026-10-12T09:13:22.805318+00:00`, using
CPython 3.12.14 on Linux x86-64. Its measured arithmetic/checking phase
took 0.035160 seconds. The actual stdout is `actual_run.log`; environment,
per-check counts, target and source hashes, damage witnesses, and all
37 per-order maxima are in `RESULTS.json`. The complete 1,942-row count
table is `exact_counts.jsonl`, one JSON object per legal triple.

From the repository root, with a local copy of the cited PDF:

```sh
python workstreams/STRUCT2-20261012/theta/scalar_checks/check_scalar.py \
  --min-n 4 --max-n 40 \
  --source-pdf /path/to/braun6.pdf \
  --target workstreams/STRUCT2-20261012/theta/MAXIMIZERS.md \
  --target-sha256 c0c02847ae525260d65dd5b11c1ee940b4b63aec6e2167c39fa8a9c12fc12fab \
  --output-dir /tmp/struct2-theta-scalar
```

The checker rejects an unexpected PDF or target hash. Runtime metadata
changes on another run; the exact count table is deterministic. File
hashes for this recorded execution are listed in `SHA256SUMS`.
