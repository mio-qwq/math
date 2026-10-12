# Support-12 residual/endpoint merge

Status: complete written lemma with a definition-level checker; independent
review is not included here.

The accepted five-anchor chart leaves residual rows 33 and 57.  This package
shows that row 57 is not a genuine search equation once the active endpoint
at 57 is allowed to be chosen: its first endpoint is forced uniquely.  When
the chart is merged with the accepted ten-scalar endpoint factorisation, the
projected factor `PG(z,b)` at word 57 must consequently be replaced by the
pointwise condition

```
sigma1(H + z) - sigma1(H) = b,
```

where `H` is computed by the base chart.  Thus the exact joint search has one
base residual (`R33=0`), one forced word (`u57=H`), and one pointwise endpoint
condition at 57.  A projected `PG` witness at some unrelated base word is not
enough; `PROOF.md` gives an explicit counterexample.

This is a reduction, not a support witness or a distance-14 proof.

Run:

```
python -B verify_residual_merge.py --output CHECK.json
```

