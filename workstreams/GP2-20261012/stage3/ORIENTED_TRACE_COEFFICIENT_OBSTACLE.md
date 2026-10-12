# An exact obstruction to the tempting oriented-matrix coefficient 1/4

GP2-20261012, 2026-10-13. This is a rigorous negative result about one
possible strengthening of the accepted reciprocal trace proof. It does not
change the certified Ka4 bound.

## 1. The proposed shortcut and its exact failure

For an entrywise nonnegative matrix `M`, retain the notation

    T=tr((MM^t)^2), L=tr(M^4),
    Y=tr(M^2(M^t)^2), X=tr(M^3M^t), R=M+M^t.

The off-diagonal reciprocal kernels in the accepted proof have the additional
orientation property

    M_xx=0 and M_xy M_yx=0.

Random orientations suggest the asymptotically sharp-looking inequality

    2(T+L) >= (1/4) tr(R^4).                         (Q)

Using `tr(R^4)=2L+8X+4Y+2T`, (Q) is equivalent to

    4X+2Y <= 3(T+L).                                 (Q')

Both statements are false even for an unweighted zero-one orientation.
The 24 by 24 matrix in `oriented_quarter_counterexample.json` has zero
diagonal and no pair of opposite nonzero entries. Direct enumeration gives

    T=5505, L=880, Y=4654, X=2799, tr(R^4)=53778.

Consequently

    2(T+L)/tr(R^4) = 12770/53778 = 6385/26889
                    = 0.2374576964... < 1/4,

or, in integral gap form,

    tr(R^4)-8(T+L)=2698>0.

Equivalently the left side of (Q') exceeds its right side by 1349. Thus the
coefficient `1/4` cannot replace `3-2sqrt(2)` in the current proof solely from
the no-digon support condition. Any valid improvement must use a smaller
coefficient or additional canonical-level structure.

## 2. Exact verification and provenance

The checker uses only the Python standard library and independently expands
all five quantities as four-index integer sums over all `24^4` ordered
quadruples. It verifies the orientation conditions, the sixteen-term trace
identity, the reduced fraction and both strict gaps. Two negative controls
alter the claimed trace and insert a digon; both must be rejected.

Run from the repository root:

```sh
python workstreams/GP2-20261012/stage3/verify_oriented_quarter_counterexample.py
python -O workstreams/GP2-20261012/stage3/verify_oriented_quarter_counterexample.py
```

The witness was found by a seeded local search over finite orientations and
then frozen as an exact integer object. The search is not used in the proof:
the displayed matrix and exhaustive four-index reconstruction are the full
certificate. This is not a strict-window code, a canonical level relation,
an optimizer, a lower bound on the best possible trace coefficient, or a
historical-priority claim.

## 3. Research consequence

Small exact enumeration through five vertices had misleadingly given ratios
at least `5/16`, while random complete orientations approach `1/4` from
above. The 24-vertex witness shows why neither observation licenses a theorem.
The next useful step is therefore one of:

1. prove a weaker coefficient strictly above `3-2sqrt(2)` with a genuine
   sum-of-squares or flag certificate; or
2. abandon scalar coefficient tuning and exploit mixed reciprocal classes or
   the actual 10/6/3 canonical interface constraints.

The second route remains more likely to affect the main asymptotic gap.
