# Independent review of the six-q selected-core batch

## Verdict

**ACCEPT**, separately for

```text
q in {5,13,21,23,25,27},  D=q*2^16.
```

For each listed `D`, the exact selected three-pair core has no 32-bit
solution.  Pair reversal gives the same exclusion for `-D`.  This verdict is
limited to these twelve signed numerical residues.

## Independence and certificate audit

Before reading the author batch, the reviewer froze the equations and a
separately written Boolean construction in `PRE_AUTHOR_FREEZE.md` and
`independent.py`.  After author contact, that builder reproduced every author
CNF byte-for-byte: each formula has 1,259 variables and 9,683 clauses.

The reviewer then used a separately written occurrence-driven RUP checker.
All six deletion-free proofs pass and end in the empty clause:

| q | RUP additions |
|---:|---:|
| 5 | 9,205 |
| 13 | 6,720 |
| 21 | 5,879 |
| 23 | 7,365 |
| 25 | 4,637 |
| 27 | 7,319 |

`AUDIT.json` freezes the exact CNF and proof digests, per-q run times, and all
controls.  For every q, direct word evaluation checks a near miss satisfying
the first five defining identities and failing only `G_D(z)=-T`.  Reversal of
the three actual pairs preserves the equation vector for `-D`.

Three proof/formula controls reject independently for every q: truncating the
proof, flipping a literal in an actual proof addition, and deleting a single
clause from the final sigma1 equation.  Deleting all 64 clauses of that final
equation also makes the original proof fail RUP, consistent with the concrete
near miss.

The author 18-file manifest matches.  No solver status without a checked proof
is used as evidence.

## Scope

Combined with the separately accepted twin classification and the separately
reviewed `q=15` certificate, this proves selected-three-pair exclusion only
for odd `q<=31`.  It does not cover every exact-valuation-16 residue, the full
thirteen-factor system, base completion, two actual message blocks, distance
13 attainability, or a distance-at-least-14 theorem.  There is no Lean or
external human verification.
