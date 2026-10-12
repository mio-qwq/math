# Independent review: selected core for odd q=33..63

## Verdict

**ACCEPT**, independently, for

```
q in {33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63},
D = q*2^16.
```

For each listed positive `D`, the exact selected three-pair core frozen in
`EQUATIONS.md` is UNSAT.  The elementary change of variables `w -> w+D`
maps derivatives at `D` to their negatives at `-D`, so the same local
exclusion holds for the sixteen corresponding negative residues.

## Independent reconstruction and proof audit

`independent_review.py` imports no author code.  It independently encodes the
32-bit modular additions, SHA-256 small-sigma maps and six selected-core
identities, then compares its DIMACS output with the author files.  All
sixteen reconstructions agree byte-for-byte and as clause multisets.  Every
formula has 1,259 variables and 9,683 clauses.

The same script parses each deletion-free DRUP trace and independently checks
every addition by reverse unit propagation.  All 87,220 additions pass and
each trace ends in the empty clause.

| q | RUP additions | q | RUP additions |
|---:|---:|---:|---:|
| 33 | 6,686 | 49 | 4,536 |
| 35 | 6,591 | 51 | 5,081 |
| 37 | 5,309 | 53 | 4,678 |
| 39 | 4,772 | 55 | 5,104 |
| 41 | 7,630 | 57 | 5,911 |
| 43 | 6,177 | 59 | 5,118 |
| 45 | 3,183 | 61 | 6,372 |
| 47 | 4,979 | 63 | 5,093 |

For every q, three fresh-database negative controls reject: removal of the
terminal empty clause, deletion of one actually used clause in the final
definition block, and a literal flip in proof addition 2.  For q=37,39,41,43,
direct 32-bit evaluation additionally checks concrete near misses satisfying
the first three derived equations and failing only `G_D(z)=-T`.  The reversal
identity is checked directly on three words for every q, in addition to its
one-line algebraic derivation in `EQUATIONS.md`.

`AUDIT.json` contains exact file digests, per-instance timings, negative-control
failure locations, near-miss values and symmetry checks.  `RUN.json` freezes
the successful invocation.  No unverified solver status is used as evidence.

## Scope

This accepts only the selected local three-pair core at the 32 signed residues
`D=+/-q*2^16` with odd `33<=q<=63`.  It is not a classification of all
exact-valuation-16 differences, not a complete support-12 exclusion, not two
SHA-256 message blocks, not a distance-13 construction, not a proof that the
distance is at least 14, and not a Lean formalization.
