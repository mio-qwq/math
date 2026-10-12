# GP2 stage three: improved all-parameter Ka4 upper bound

This stage uses reciprocal-class trace configurations to strengthen the
uniform upper bound, independently of fixed-alphabet optimization.
The full self-contained argument is [RECIPROCAL_TRACE_BOUND.md](RECIPROCAL_TRACE_BOUND.md).

Set

    delta = 1/[27(1+(3+2sqrt(2))^(1/3))^3].

For every finite alphabet, every probability distribution (zero weights
allowed), and every three-valued ordered-pair relation, the empty-rotation
probability is at least delta, hence at least 125/74088. Consequently

    beta <= lambda_4 <= (1-delta)/4
         = 0.249578038101911868...,
    lambda_4 <= 73963/296352 = 0.249578204297592052... .

The inherited lower bound remains
beta=0.224808115216882691.... The rational upper bound is below the former
182/729 by exactly 631/8001504. This is a modest interval improvement,
not an exact-value solution. The gap below 1/4 is enlarged by about 23%.
The theorem also gives

    gp(Ka(m,4)) <= floor(73963m^4/296352)+73m^3  (m>=3).

The universal proof consists of a disjoint six-class event decomposition,
two Frobenius Cauchy inequalities, a sixteen-term trace identity, two
weighted C4 Cauchy inequalities and a six-variable convexity inequality.
The rational coefficient has an exact tangent-polynomial certificate.
The two omitted off-diagonal directed-cycle patterns supply the improvement.

## Actual verification and scope

The primary standard-library checker passed 297 relation/weight cases,
80 nonnegative rational matrix cases and 12 full-entry negative controls.
The same checks passed under `python -O`. These are definition/formula
checks, not a computational proof by finite sampling of a universal optimum.
The all-parameter conclusion is the written argument. Independent acceptance,
input hashes, a separate checker and actual execution logs are under
[trace_review/](trace_review/).

From the repository root:

```sh
python workstreams/GP2-20261012/stage3/verify_reciprocal_trace_bound.py
python -O workstreams/GP2-20261012/stage3/verify_reciprocal_trace_bound.py
python workstreams/GP2-20261012/stage3/trace_review/check_trace_independent.py
python workstreams/GP2-20261012/recovery_review/run_ten_state_review.py
```

The last command remedies the inherited ten-state checker's absent entry
point while preserving its frozen source. The original 98 science files and
their manifests remain unchanged. Historical original sources, signature
preservation limitations and exact remote-delivery acceptance are documented
under `../recovery_review/`.

No complete Lean, axiom audit, external human peer review, exact lambda_4,
historical first discovery or globally best-known status is claimed.
`FORMALIZATION_STATUS.md` records the actual launcher failure, rather than
implying that Lean compilation succeeded. `NOVELTY_GATE.json` records the
bounded follow-up searches.

## Next structural step

Counting only one common unordered reciprocal class on the four cross pairs
still discards many configurations in the actual empty-orbit event. The next
analytic target is an exact mixed-class decomposition coupled to the pair
levels and triple choices, or a uniform forced-orbit loss certificate.
Simply tuning the scalar trace coefficient would give only a small further
gain. Neither a solver timeout nor a finite fixed-label cover can certify
that missing uniform bridge.

The follow-up file
[`ORIENTED_TRACE_COEFFICIENT_OBSTACLE.md`](ORIENTED_TRACE_COEFFICIENT_OBSTACLE.md)
now rules out one tempting shortcut exactly. Even with zero diagonal and no
digons, the proposed coefficient `1/4` fails: a certified 24-vertex
orientation has ratio `6385/26889<1/4`. Its standard-library checker expands
all `24^4` ordered quadruples and rejects two damaged inputs. This negative
result leaves the bound above unchanged and reinforces the mixed-class or
canonical-interface direction.

The subsequent
[`ORIENTED_FIFTH_REDUCTION.md`](ORIENTED_FIFTH_REDUCTION.md) isolates the
weaker candidate `2X<=T+L`, which would conditionally give reciprocal
coefficient `1/5`. It proves two exact equivalent trace/interface formulas
and supplies a five-vertex counterexample to pointwise interface positivity.
All 59,809 zero-one orientations through order five pass the global candidate,
but this finite evidence is explicitly not a proof and does not change the
displayed lambda bound.
