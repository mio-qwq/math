# CRYPTO3 stage-9 checkpoint

Recovery base: `e2a81b71bcc83ab72f325934c449d27ef198efb3` on
`partner/dist-CRYPTO3-20261012`.  The global theorem remains a lower bound
of **13** for the real 32-bit modular-addition SHA-256 message expansion.
This stage contains neither a distance-13 message pair nor a proof that the
distance is at least 14.

## Accepted base/factor composition

The accepted five-anchor base chart originally left residual rows 33 and 57.
The new author proof and blind independent reconstruction show that the active
first endpoint `u57` affects exactly coordinates `{57,59,61,63}`.  In
particular `R33` is independent of `u57`, while

```text
H = sigma1(C55) + C50 + sigma0(C42) + C41,
R57 = u57 - H.
```

Thus row 57 has the unique solution `u57=H`.  Composition with the accepted
ten-scalar endpoint factorisation must replace its projected condition
`PG(z,b)` by the pointwise condition

```text
sigma1(H+z)-sigma1(H)=b.
```

An existential witness at another base word is insufficient; the frozen
negative control demonstrates this directly.  The exact remaining base
obligations are `R33=0`, the forced endpoint `u57=H`, and this pointwise
sigma1 condition.  Their solvability is not asserted.

## Exact valuation-16 finite window

For `D=q*2^16`, an exact affine/carry classification covers every positive
odd `q` in `1..31`.  It retains actual 32-bit word pairs and both sigma
derivatives on the same pair.  The selected twin condition is impossible for

```text
q={1,3,7,9,11,17,19,29,31}
```

and has 21 frozen full-word local fixtures over

```text
q={5,13,15,21,23,25,27}.
```

This disproves a uniform twin obstruction at exact valuation 16.  The first
failed certificate run is preserved: classification completed, but an
unjustified control required a nonempty low-31-only frontier.  The repair only
removed that nonemptiness assertion.  The independent reviewer rebuilt the
complete input-class cover and classification before comparing author bytes.

The twin survivors do not extend to the required third joint-image point in
this finite window.  Deletion-free DRUP certificates, with independently
rebuilt CNFs and standard-library RUP checkers, exclude the exact selected
three-pair core for all seven surviving positive q values.  The `q=15`
certificate and review were developed separately; a batch covers
`q={5,13,21,23,25,27}`.  Pair reversal supplies the corresponding negative
residues.  Consequently the selected three-pair core is excluded for

```text
D=+/-q*2^16, every odd q in 1..31.
```

This is a finite numerical window, not the whole exact-valuation-16 layer:
up to sign that layer still has odd quotients through 32767.

## Corrected q=5 branch record

For `D=00050000`, the words labelled X and Y are a valid twin candidate with
`A=40406e02` and `T=1ffd913e`.  The earlier proposed third word Q has
`(+D,+A,+T)`.  Reversing it gives `(-D,-A,-T)`, not the required
`(-D,+A,+T)`.  The prior informal three-pair claim therefore had an
orientation/sign error and is explicitly withdrawn.

Separate author and independent certificates prove both that the correct
fixed third point `(+D,-A,-T)` is absent and that the fixed reciprocal edge
`F_A(u)=D` is absent.  These fixed-branch results are retained as a diagnostic
even though the later universal `q=5` three-pair certificate is stronger.

## Accepted failure boundaries for local relaxations

The complete corrected thirteen-factor graph has a satisfying assignment in
its exact quotient modulo `2^26` at `b=00010000`.  Every full `J` factor uses
one real 32-bit pair for its simultaneous `(d,F,G)` residues; the witness is
not assembled from independent masks.  It retains all scalar carries through
bit 25.  Therefore valuation signatures, joint three-way mask signatures and
even exact low-26 numerical factor constraints cannot exclude this stratum.

Separately, factors 34 and 43 have a full 32-bit actual-pair witness with
`b=bfbf0000` and `v2(b)=16`.  Their anti-symmetric two-factor fragment alone
also cannot exclude the layer.  Neither positive witness is a full 32-bit
thirteen-factor solution or a pair of common-base message schedules.

## Evidence classes and remaining target

All theorem statements above are backed by frozen author artifacts and
separate AI review packages.  The original q=5 sign mistake, the first failed
valuation run, discovery solver timeouts, and uncertified solver observations
remain recorded as failures or candidates rather than proofs.  No Lean
formalisation or external human review is claimed.

The highest-value next step is no longer another valuation-only relaxation.
One route is to extend the certified three-pair exclusion beyond odd
`q<=31`; another is to solve or exclude the full 32-bit ten-scalar/thirteen-
factor system while binding word 57 to the base value `H` and satisfying
`R33=0`.  A local factor assignment remains strictly weaker than a genuine
16-word message pair.

Replay the stage checkpoint with Python's standard library:

```sh
python -B workstreams/CRYPTO3-20261012/continuation-v9/replay.py
```

The default replay checks prior and stage manifests, reruns the short exact
author checkers, and validates frozen independent acceptance receipts.  It
does not repeat the several-minute complete q-class enumeration; that heavy
replay is available explicitly in its author and review packages.
