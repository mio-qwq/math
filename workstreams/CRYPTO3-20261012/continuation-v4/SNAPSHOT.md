# CRYPTO3 continuation checkpoint

Branch: `partner/dist-CRYPTO3-20261012`. Recovery base:
`b7eb3becacf474a6978b6acb2879fce3d505e395`.
The original stage-2 README, publication status, manifests and reviewed
proof bytes are preserved. This checkpoint describes later work.

## Exact object and present global boundary

Two arbitrary, distinct sixteen-word blocks are expanded by the original
32-bit modular-addition SHA-256 schedule. Distance counts unequal words at
all 64 positions, including the input. The universal lower bound remains
**13**. There is no actual distance-13 message pair or bound of 14 here.

## Evidence recovery and independent acceptance

- The XZ transport copy restores all 12,444,726 original RUP bytes with
  SHA256 `cd1845cdde5fca010b4b8557bcb27947eb5aef50b45856619cce7d54608540c5`.
  All 203 listed stage-2 files match; with their manifest, this is the
  documented 204-file frozen release. All 21 isolated replay commands pass.
- [The inherited global gate](sha256-word-distance/inherited-gate-v4/)
  newly checks all 5,308,416 transition inequalities, all 65,535 nonzero
  initial states, all 65,536 terminal zeros, and the entire equality-path
  traversal of 735 nodes and 15 supports. The universal no-singleton
  reduction and the two old support exclusions receive written independent
  reconstruction. This closes the prior bounded-review replay gap.
- [Independent window review](sha256-word-distance/shift-review-v4/REVIEW.md)
  accepts the exact seven left maps, three right maps and `3 -> 14`.
  Every sixteen-word window of the uniquely extended actual recurrence
  remains a legal, distinct input pair. With the now checked inherited
  dependencies, distance-13 existence reduces to the six representatives
  **5, 8, 9, 10, 11, 12**. This excludes no additional representative.

## New independently accepted local results

| Exact support scope | New restriction | Current acceptance |
|---|---|---|
| 12, and 6/7/13 by directly checked recurrence bridges | `v2(D)<=18`, with `D=d18=d34` on support 12 | [Independent acceptance](sha256-word-distance/support12-review-v4/REVIEW.md), 89,243 complete three-mask cases |
| 10 and 11 | `min(v2(d18),v2(d34))<=15` | [Independent acceptance](sha256-word-distance/supports10-11-review-v4/REVIEW.md), complete 65,536-mask cover and both actual local sharpness fixtures |

The first bound was previously 20. The second is a joint restriction;
neither individual valuation is asserted to be at most 15. These constrain
actual schedules having the named supports, but do not exclude a complete
support. Local sharpness fixtures are actual word pairs, not messages.

## Frozen failure and next mathematical step

[Full-pair probe](sha256-word-distance/full-pair-probe-v4/MECHANISM.md)
retained all 48 independent-active-pair difference equations of support 5
at `v2(d17)=11`, with 13,369 Boolean variables and 46,690 clauses.
Glucose3 returned `unknown` at its 50,000-conflict budget (50,147 conflicts).
That bounded mechanism stops; the result is neither SAT nor UNSAT and
contains no base completion. No timeout is extended.

The [independently accepted width lemma](sha256-word-distance/width-review-v5/REVIEW.md)
gives an additional useful support-12 stratum. If `2^18`
divides D, sigma1 output bits 22..30 agree within each pair. Its bit 31
changes precisely when input bit 18 changes, giving the same modular
half-word contribution for differences D and -D. It cancels in both
sigma1 derivative gaps. The same integer-width argument reduces this
stratum to `D=+/-q*2^18`, `1<=q<=15`. A separate candidate calculation of
the eight new odd quotients has empty exact carry branches; a stronger
ceiling of 17 is being prepared as a separate proof package, with its own
independent acceptance still required. It is not an accepted bound here.
The original support-12 equations
also retain `d26=-F18` and `F26=-D`, a further sigma0-chain constraint.

Other agents' paths and `main` are outside this workstream. Branch uploads
may be unsigned; final signatures and main integration belong to ROOT.
No paper, DOI, Release, human peer review, historical priority or Lean
certification is created by this continuation.

Reproduction of the frozen continuation uses only Python's standard library:

```sh
python -B workstreams/CRYPTO3-20261012/continuation-v4/replay.py
```

Add `--full-stage2` only when the original 21 checks need another replay.
The default checks the restored stage-2 hashes and all listed new proof,
comparison and damage-control gates in a temporary copy. The living
checkpoint is not a frozen proof artifact; the snapshot and manifest in
`continuation-v4/` bind the exact accepted phase.
