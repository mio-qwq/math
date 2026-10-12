# Independent review of the bounded valuation-16 twin classification

## Verdict

**ACCEPT**, bound to author certificate SHA-256
`f74dd80590b0e6b9c3f2ccb4841e9c39b94dd03a53c065dd16f3e48252854bd5`
and author checker SHA-256
`a58fc79b82edce8c82d8838a0d197bdd77b9dc42a4d91c4250b0d3ae4d6d1d60`.

For each

```text
q in {1,3,7,9,11,17,19,29,31},  D=q*2^16,
```

there are no 32-bit words `x,y` satisfying the selected twin condition

```text
F_D(x)=F_D(y),
G_D(y)-G_D(x)=2D                 (mod 2^32).
```

Reversing both directed pairs proves the same statement for `-D`.  The other
seven tested positive quotients `q={5,13,15,21,23,25,27}` have 21 actual
surviving affine leaves in total, so no uniform exact-valuation-16 obstruction
is proved.

## Independence protocol

Before reading the author certificate or checker, the reviewer read only the
author's frozen `PRECOMMIT.md` plus the accepted v8 fixed-`D=2^16` materials.
The reviewer then wrote a separate standard-library classifier using:

- basis evaluation, rather than the author's closed-form expressions, to
  construct all small-sigma output rows;
- exhaustive regeneration of every upper-half affine cube from its fixed
  coordinates;
- a highest-pivot GF(2) eliminator, rather than the author's lowest-pivot
  eliminator;
- exact per-bit signed carry transitions with exhaustive truth-table recovery;
- direct word evaluation for one representative of every surviving leaf.

The independent run and source were frozen in `PRE_AUTHOR_RUN.json`,
`PRE_AUTHOR_FREEZE.json`, and `PRE_AUTHOR_FREEZE.md` before comparison.  It
took 461.37 seconds and checked all sixteen odd q values, both 31- and 32-bit
sigma1 endpoints, 21 positive-orientation survivors, their 21 reversed
negative orientations, and 126 damaged-witness controls.

## Exact comparison

The independent and author computations agree for every q on:

- the number and complete size histogram of input affine cubes;
- all sigma0 affine-leaf counts;
- all low-31-bit and full-32-bit twin-leaf counts;
- the excluded and surviving q sets;
- the multiset of surviving input-XOR class pairs.

The complete shared count table is:

| q | classes | sigma0 leaves | low31 twins | full32 twins |
|---:|---:|---:|---:|---:|
| 1 | 16 | 414 | 0 | 0 |
| 3 | 29 | 3,123 | 0 | 0 |
| 5 | 41 | 3,495 | 3 | 3 |
| 7 | 40 | 2,310 | 0 | 0 |
| 9 | 51 | 3,277 | 0 | 0 |
| 11 | 63 | 10,057 | 0 | 0 |
| 13 | 62 | 10,054 | 2 | 2 |
| 15 | 49 | 2,345 | 4 | 4 |
| 17 | 59 | 3,983 | 0 | 0 |
| 19 | 82 | 31,014 | 0 | 0 |
| 21 | 93 | 33,495 | 4 | 4 |
| 23 | 81 | 28,467 | 2 | 2 |
| 25 | 80 | 28,634 | 2 | 2 |
| 27 | 91 | 47,541 | 4 | 4 |
| 29 | 79 | 45,225 | 0 | 0 |
| 31 | 56 | 9,874 | 0 | 0 |

Different free-variable conventions produced different actual representatives
for some leaves, as expected.  Nevertheless, every author fixture was directly
re-evaluated independently, and the surviving affine class-pair multisets agree
exactly.  The reviewer also replayed the author's frozen checker successfully in
190.35 seconds.  The author package's 14-file manifest was independently checked
for both byte size and SHA-256.

## Coverage argument

For each q, every one of the 65,536 upper-half values is assigned to exactly one
mask `u xor (u+q mod 2^16)`.  Regenerating each class from all fixed coordinates
proves it is exactly that affine cube, while the low half remains unrestricted.
The Cartesian square therefore covers all ordered `(x,y)`, not a sample.

On each class pair, the two small-sigma derivatives are affine Boolean rows plus
integer carries.  Exhausting the at-most-four row-value assignments at every bit
and checking the affine reconstruction loses no cases.  The independent
eliminator verifies every contradiction as an XOR equal to `0=1`, and every
surviving leaf supplies an actual word fixture.  Consequently a zero leaf count
is a complete finite exclusion for that fixed q.

## Exact scope

This acceptance is only for the selected **two-pair twin local condition** over
the sixteen positive odd quotients `q<=31` and the negative residues obtained by
pair reversal.  It is not a classification of every odd 16-bit quotient, the
required third pair, the reciprocal edge, the complete support-12 equations,
base completion, or a 16-word message pair.  The author's 42 solver UNSAT
observations remain uncertified observations and are not premises.  This is
independent AI review, not Lean formalization or human peer review, and proves
neither distance-13 attainability nor distance at least 14.

## Replay

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-review-v9/check_independent.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-review-v9/compare_author.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-general-v9/check.py --negative
```

