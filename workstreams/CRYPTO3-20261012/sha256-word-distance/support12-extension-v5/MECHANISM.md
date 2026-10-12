# The valuation-18 boundary of the support-12 core

This is a new bounded mechanism, recorded before computation. The v4
source and certificate remain frozen and are read-only dependencies.

## Mathematical question

For three actual 32-bit pairs X,Y,R, all sigmas evaluated on the actual
members of each pair, require

    d(X)=d(Y)=D!=0, d(R)=-D,
    F(X)=F(Y)=F(R),
    G(Y)-G(X)=2D, G(Y)-G(R)=D.

The parent `width-reduction-v5/PROOF.md` shows that if 2^18 divides D,
its complete residue list is `+/-q*2^18`, 1<=q<=15: the shared top-bit
sigma1 contribution cancels in both gaps. The v4 result already excludes
the even q values. This stage therefore concerns only q=1,3,5,7,9,11,13,15,
and their negatives by simultaneously reversing all three pairs.

Determine whether the three-pair core itself has a genuine local witness
at valuation exactly 18. Any witness must be checked from the original
word formulas and must be reported as local, not as an actual 13-word
expanded-message support or message blocks. If all eight values are
excluded, a complete finite proof replay and independent review are
required before a stronger support ceiling is claimed.

## Initial computation budget and evidence discipline

The first budget is at most eight fixed-D SMT discovery queries of at
most 2,000 ms each. Stop at the first actual six-word witness and verify
it without the solver. Solver UNSAT or unknown is only a discovery or
failure record. It cannot establish a mathematical exclusion by itself.
An empty core, if suggested, will instead be certified by the existing
exact carry-mask method in this new directory with frozen parameters.

If the core is sharp, a separate question can add the original support-12
fourth pair Z at index 26. Recurrence t33 and t41 imply

    d(Z)=-F(X), F(Z)=-D.

That further query must retain X,Y,R and be scoped separately. No
unrestricted full-schedule timeout is extended, no initial word is
fixed to zero, and no base-completion equation is discarded in a claim
about actual messages.

Current status: pre-computation research question; no result assumed.

## First bounded outcome and proof obligation

All eight fixed-D SMT queries returned UNSAT in the recorded discovery
run. This is not a proof or a scope change. The next bounded calculation
therefore runs the frozen v4 exact carry-mask traversal on precisely the
eight new odd representatives. Its budget is a 55-second process limit;
completed cases are saved immediately. No old even representative is
rerun. If all are empty, construct an explicit finite certificate and
separately written definition-based checker in this directory, then
combine with the separately reviewed width lemma and v4 exclusion.

## Finite outcome

The entire eight-value discovery traversal finished within the recorded
55-second budget, taking 10.98 seconds. All final branches were empty.
It found 15 twin branches at q=5,13,15, so the third pair is retained
in the proof rather than assuming the twin relaxation is empty. The
definition-based certificate/replay in this directory uses an explicitly
hash-pinned v4 kernel and covers all 12,245 new mask pairs plus 612
third-mask tests. See `PROOF.md` and `CHECK-RUN.json` for the author
finite-proof result; independent-agent acceptance remains separate.
