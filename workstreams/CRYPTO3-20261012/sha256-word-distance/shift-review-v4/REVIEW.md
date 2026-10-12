# Independent acceptance receipt for the stage-3 window reduction

**Accepted as a conditional, actual-schedule support reduction.** The
eleven mathematical implications in frozen `shift-reduction-v3/PROOF.md`
are correct. This independent review found no gap in legality of new
input blocks, distinctness, inverse prefixes, forward-tail induction, or
the special `3 -> 14` support substitution. It does not improve the
numeric distance bound or construct an actual distance-13 pair.

Reviewed base commit:
`b7eb3becacf474a6978b6acb2879fce3d505e395`, branch
`partner/dist-CRYPTO3-20261012`.

The original proof SHA256 is
`227e4713025452f5aa4b49430af339131c8452d9ab45ec013548a486d7ba39a0`.
The original support SHA256 is
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
The machine receipt binds the proof, manifest, candidate data and
independently written proof to their exact source bytes.
Changing those bytes invalidates this exact-version receipt.

## Method and universal mathematical proof

The reviewer first read the frozen support data and original SHA-256
recurrence, independently wrote `INDEPENDENT_PROOF.md` and
`check_independent.py`, and executed its first check before reading the
discoverer's stage-3 proof. The discoverer's `check.py` was neither
imported nor executed. Its SHA256 is recorded only to bind the candidate
snapshot, without asserting an independent code audit of that checker.

The independent reconstruction is slightly stronger than the candidate's
legality argument: arbitrary inputs admit a unique extension on all
integer indices because one can solve the recurrence for its oldest
word. Every sixteen-word window of that sequence is a legal new input
and generates the translated sequence. Any two initially distinct
sixteen-word inputs remain distinct at every translated window, since
equality on any sixteen consecutive words propagates in both directions.
Neither statement needs sigma invertibility, a support assumption or
random testing.

For the candidate's seven left maps, each extra tail equation has four
equal predecessor word pairs; any newly created predecessor is already
equal by earlier induction. For the three right maps out of support 0,
the inverse prefix equations successively produce equal words -1,-2,-3.
The direct term `d64=d57 != 0` and equal `d65=0` make `3 -> 14` exact
after dropping original active position 1. No independent word-pair
choices are substituted for a complete schedule.

The review's first seven left maps were independently organized as
`0,1,2,4 -> 9` and `6,7,13 -> 12`, with sizes 1,2,3,4 and 1,3,2.
The candidate instead factors the first group through support 0.
`compare_candidate.py` separately verifies the candidate's exact seven
rows, exact three right rows, all their printed dependency indices, and
the special map, using only reviewer-owned code.

## Dependencies and the six representatives

The eleven maps themselves are unconditional implications for actual
pairs having the specified exact supports. The global six-case reduction
also needs the inherited complete classification of distance-13 supports
into the frozen fifteen, and a valid exclusion of support 14. Those
premises are not re-proved by this review. The inherited lower bound 13
is additionally needed to describe six exclusions as sufficient for
the global lower bound 14.

The candidate cites both previous exclusions 3 and 14. Its own special
map shows that exclusion 14 alone already excludes 3; the independent
coverage does not need a second premise excluding 3. Subject to these
premises, distance-13 existence is equivalent to existence on at least
one of supports `5,8,9,10,11,12`.

There is no support-only shared-prefix assertion for the converse
`9 -> 0`: its first inverse row is `d_-1=d15-d8`. For support 12 the
first inverse row is `d_-1=d15-G13`, again involving two active inputs.
The review preserves these expressions as undetermined. Such failure
of a structural proof is not proof that a reverse implication is false
after all original recurrence constraints are imposed.

## Reproducible finite evidence and negative controls

From the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/shift-review-v4/check_independent.py --output workstreams/CRYPTO3-20261012/sha256-word-distance/shift-review-v4/INDEPENDENT_RUN.json
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/shift-review-v4/compare_candidate.py --output workstreams/CRYPTO3-20261012/sha256-word-distance/shift-review-v4/REVIEW_RECEIPT.json
```

These use the Python standard library only. The output is deterministic.
The first command checks exact boundaries, support equality and coverage,
eight negative controls, binary ranks of the original small sigmas, and
a conservative search over all fifteen supports and 126 nonzero offsets
from -63 to 63. The second checks the candidate's manifest and all ten
printed map rows, the special map, the frozen result/log agreement, and
four damaged-data comparison controls.

The negative controls reject blindly reversing support 9 or support 14,
using a wrong shift, discarding the active tail of support 3, and a wrong
target. Concrete input pairs also refute blanket claims that an arbitrary
inverse prefix or forward tail is equal. The comparison controls alter a
target, tail dependency, representative list and inverse-created index;
all must fail independently.

The concrete implementation check uses sixteen deterministically derived
pairs, all 127 offsets -63 through 63, and 260,096 word equalities. It
checks the implementation of the window construction. These concrete
checks and the candidate's original random tests are not premises of
the universal mathematical proof.

## Additional conservative mappings and limits

The broad search accepts 24 exact source-to-target maps, including all
eleven reviewed maps and thirteen additional maps. They express more
edges within the first family and the irregular family; none lowers the
six-representative count. The original small sigmas are independently
checked to have binary rank 32, so a single transformed active predecessor
is nonzero. Two or more active predecessors, or an undetermined
predecessor, remain undetermined; their sum is never automatically
declared zero or nonzero. Search completeness applies solely to this
specified zero/one-active-term oracle and the finite offset range, not
to all possible mathematical shift reductions.

The later supplement `ABSORPTION.md` and its thirty exact finite
witnesses show that this conservative oracle enters an absorbing
sixteen-unknown state within 63 extension steps in both directions for
every source support. Consequently its 24 safe maps are complete for
all integer offsets within this oracle. This extends the scope of the
mechanism check, and still does not exclude stronger mathematical
cancellation arguments or reduce the representative count.

This is independent review by a separate AI agent, not external human
peer review. Neither frozen candidate files nor any other agent's files
were modified. No signed commit, main integration, formal publication,
DOI, Lean theorem, attack on SHA-256, or historical-priority claim is
created by this receipt.
