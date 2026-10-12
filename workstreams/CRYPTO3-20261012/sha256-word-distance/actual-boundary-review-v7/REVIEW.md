# Independent AI review of the actual-word inverse-boundary package

**ACCEPT, with the exact local scope below.** The sigma0 anti-cycle
forbids either additive member from being +/-2^k for 22<=k<=31. All
48 original support12 difference rows, including the 25 nonzero rows,
are reconstructed correctly. The four actual-word-pair fixture is a
valid counterexample to the weaker conservation submechanism forcing
a zero inverse-boundary target. It is **not** a complete support12
model or a counterexample to the actual inverse-shift implication.

Accepted author directory: `actual-boundary-v6/`. Its manifest SHA256 is
`614d7c5fbf2994da2de9593efcbd8a09ee1f4b46dfe419e91a37d742d8073aad`.
Accepted proof, checker and data hashes are respectively

    572aed96c813c8f388802a70a80fd312ad23dc234424e49f898480ee209f5ace
    0ed1ce41bbf4a4775eb385c360ab060b2e988cfedd1a263a9124fec176e5a3af
    0a4f6572eacd775de46fb8dc87a8dc76364171ab098c460b10c811ed321babc7

The reviewer independently reconstructed a shorter proof and checker
before reading any new author bytes. It uses the complete original
sigma0 rows, reconstructs a two-sided inverse, and checks all 55 high
contiguous output masks. Each inverse mask has a changed bit below
the common-low-bit range forced by the other actual derivative. Both
signs, both anti-cycle members, and top-bit carry wraparound are covered.
The inverse proof does not use an old stored inverse as a premise.

Keep the symbol mapping explicit:

| Symbol | Actual support12 quantity | Other notation |
|---|---|---|
| Reviewer a | d26=d42 | Author b=-checkpoint A |
| Reviewer b | d18=d34=d11 | Author a=checkpoint D |

The independent proof uses P at18 and Q at26. The author applies the
symmetric theorem with P at26 and Q at18; this is the same anti-cycle.

The subsequent comparison checks all seven author manifest entries,
all 32 inverse columns and the 55 high-mask values, the exact original
25-row table and 23 zero rows, every one of the eight fixture words,
their actual d/F/G values, and the complement-and-reverse construction.
Its nonzero inverse-boundary target is `ffd519ca`.

Only original rows29 and42 in the fixture are verified entirely by
provided actual-pair differences. Rows28,31,41,44,57 additionally use
explicitly defined auxiliary scalar interfaces. The actual pairs at
10,11,15,18,20,28,34,43,57 remain absent. Neither all25 actual-pair
conditions nor original base-message completion is realized. The
review does not assert that the missing conditions are compatible.

The accepted structure-v7 reciprocal signature filter also has a
valuation<=23 ceiling. It already covers powers at k>=24 in author
b=reviewer a. The exact powers at k=22,23 are additional restrictions.
For author a=reviewer b=checkpoint D, the already accepted valuation
ceiling16 covers all these high powers. The structure table's 1024
cases are not rerun here; its separate frozen independent review is
hash-bound as overlap context, not a premise of the new short proof.

The lower-k endpoint candidates and the old 11440-comparison discovery
screen are not independently replayed or accepted by this receipt.
They are not premises of the high-power exclusion or fixture. No author
checker, generator, solver, or old unknown run is imported or executed.

One reviewer implementation error was caught and corrected: the first
fixture comparator required an ordinary unsigned G13+G29 equality,
whereas those representatives sum to `1002ae636` and their required
mod32 sum is `002ae636`. `IMPLEMENTATION_CORRECTION.json` records that
source version and correction. The author proof was correct, and the
pre-author checker/short-proof hashes are unchanged. All final checks
pass; actual-word/G mutations and a missing high certificate are rejected.

Read-only replay from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/actual-boundary-review-v7/replay_readonly.py
```

Use `--part core` or `--part comparison` for one component. The wrapper
prints new reports without overwriting frozen runs. Only the Python
standard library is needed. `REVIEW_RECEIPT.json` binds all reviewed
bytes and the chronology in `PRE_AUTHOR_FREEZE.json` and
`FIRST_AUTHOR_CONTACT.json`.

This is a separate AI review, not Lean formalization, external human
review, historical-priority certification, a new global word-distance
bound, an actual 13-word message pair, or a SHA-256 hash attack. No
entire support is excluded and no main/DOI/Release action is performed.
