# Non-delay optimum bridge checkpoint

Base local commit: `0ddd4ba34ad7554ea32e487c18aea92bc28e9cf9`.
Parent authorized continuation of this proof route after separate Ready
and Continuation deliveries. All prior sources and receipts are unchanged.

New `formal/ROBNonDelay.lean` has eleven actually compiled audited primary
statements. The missing action-extension premise is now proved from actual
readiness and BatchWidth. Every finite completing actual continuation is
normalized to a non-delay one with the same horizon, using the already
verified actual continuation replay rather than an assumed value inequality.

Strong induction on N-|D| constructs a finishing non-delay continuation
from every coherent state of a finite forward program with positive B,W.
Hence an optimal finite continuation exists and has a non-delay witness,
with horizon bounded by N-|D|. An actual ROBTrace-state endpoint is included.

Important exact boundary: the optimum is `OptimalFrom`, over finite chains
of the original ROBStep relation. No splice back into the original infinite
time-assignment ROBTrace, no original-Optimal representation iff, and no
prefix-macro recurrence/complexity/Python proof is claimed. This scope is
explained prominently in `formal/ROB_NONDELAY.md`.

Fresh replay:

```sh
python workstreams/ILP1-20261014/formal/verify_nondelay.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-nondelay-root-check
```

Next important bridge: extract a legal time assignment from any initial
finite completing transition chain, or equivalently splice finite paths
into full traces. After that, formalize stopping at the first later clear
prefix and combine non-delay optimum with uniqueness of non-prefix actions.
Those are concrete remaining steps toward the exact prefix DP theorem.
