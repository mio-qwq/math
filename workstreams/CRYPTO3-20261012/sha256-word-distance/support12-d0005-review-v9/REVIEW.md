# Independent review: fixed `D=00050000` branch

## Verdicts

| Claim | Verdict | Independent basis |
|---|---|---|
| Candidate sign/orientation correction | **ACCEPT** | Direct evaluation gives `Q=(D,A,T)` and hence `reverse(Q)=(-D,-A,-T)`, not the required `R=(-D,+A,+T)`.  The equivalent required forward image is `(D,-A,-T)`. |
| Fixed third-image UNSAT | **ACCEPT** | An independently designed 349-variable/2,158-clause CNF for `F_D(z)=-A, G_D(z)=-T` is UNSAT with a separately checked 288-line DRUP proof.  The author's independent 355-variable/2,203-clause encoding was rebuilt exactly as a clause multiset and all 7,662 DRUP additions passed the reviewer checker. |
| Fixed reciprocal UNSAT | **ACCEPT** | An independently designed 222-variable/1,292-clause CNF for `F_A(u)=D` is UNSAT with a separately checked 1,371-line DRUP stream (1,360 additions, 11 deletions).  The author's independent 226-variable/1,322-clause encoding was rebuilt exactly as a clause multiset and all 1,810 DRUP additions passed the reviewer checker. |

## Frozen orientation

All values are modulo `2^32`.  Direct standard-library evaluation gives

```
X: (d,F,G) = (00050000,40406e02,1ff8913e) = (D,A,T-D)
Y: (d,F,G) = (00050000,40406e02,2002913e) = (D,A,T+D)
Q: (d,F,G) = (00050000,40406e02,1ffd913e) = (D,A,T)
```

Reversal negates all three coordinates, so the displayed `Q` cannot supply
the required `R=(-D,+A,+T)`.  A valid `R`, if one existed, would reverse to
the exact forward query

```
(D,-A,-T) = (00050000,bfbf91fe,e0026ec2).
```

The reciprocal pair has original orientation `P=(-A,-D,*)`; reversing it
gives `Q=(A,D,*)`, so its exact equation is `F_A(u)=D`.

## Certificate audit

The author's 11 manifest-covered files match every recorded byte count and
SHA-256 digest.  Certificate metadata agree with the parsed DIMACS and DRUP
files:

| Artifact | Variables | Original clauses | DRUP additions | SHA-256 |
|---|---:|---:|---:|---|
| author `third_image.cnf` | 355 | 2,203 | — | `fd679370c44887373eb8e8c2e682414d9dede63d77011831250518260f0497c4` |
| author `third_image.drup` | — | — | 7,662 | `aa9b486ed83bea41436979c375ab50b904f1fff592bec364f1c07354317b25f2` |
| author `reciprocal.cnf` | 226 | 1,322 | — | `c9aabd080d90748ad977a6e76c1a0c7bcc5dab6fac7428cdaf30069f2eddaaeb` |
| author `reciprocal.drup` | — | — | 1,810 | `d2f197e04bc34d21cb07c2d05756ec9dda54b6918f3078f6ffd9ec50890dd1ab` |

The reviewer's clause generator uses truth-table full adders and parity
relations, and matches each author CNF as a normalized clause multiset.  A
separate forward-RUP engine checks every author proof clause through the
final empty clause.  It rejects both deletion of the final empty clause and
flipping the first literal of the first proof addition.  Independent SAT
controls recover the exact X and Y joint derivatives.

The independent CNFs deliberately use a different carry layout, explaining
their smaller counts; their distinct hashes and proof shapes provide a
second proof of the same two fixed statements rather than a replay of the
author generator.

## Scope

These verdicts concern only fixed
`D=00050000, A=40406e02, T=1ffd913e`.  They do **not** infer exclusion for
all q=5 choices of `A`, full support-12 infeasibility, any message pair or
message exclusion, or distance at least 14.

Machine-readable evidence is in `PRE-AUTHOR-FREEZE.json`,
`INDEPENDENT_RUN.json`, and `COMPARISON.json`.
