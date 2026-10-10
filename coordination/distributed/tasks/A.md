# A — finite union-closed families

ID: A. Role: independent exploratory researcher. State: **prepared, not acknowledged**. Base SHA: `42a30d62d084a9dbe64c92666addd6cf28986b16`. Branch: `partner/dist-A`. Exclusive output: `workstreams/A/`. Read the [shared protocol](../BRIEF.md); do not edit coordination or other streams. No formal project number is allocated.

## Exact initial question and source gate

For a finite family F of subsets of a finite ground set, containing at least one nonempty member and closed under pairwise union, must some x in the union belong to at least half the members? A counterexample requires DISTINCT sets and, for EVERY x in the union, `2 * count{x in S : S in F} < |F|`, as well as every union remaining in F. Empty-family, repeated-set, nonuniform-weight, or weakened closure constructions do not answer this question.

Starting references, to read directly and update:

- Bruhn–Schaudt, *The journey of the union-closed sets conjecture*, [arXiv:1309.3297](https://arxiv.org/abs/1309.3297), for the original formulation and historical references.
- Lu–Raz, [arXiv:2405.10639](https://arxiv.org/abs/2405.10639), distinguishing the original problem from weaker Reimer conditions.
- Tian, [arXiv:2608.25147](https://arxiv.org/abs/2608.25147), a recent restricted-height result; verify its version and exact inclusion/exclusion of the empty set before using it.
- Demontis, [arXiv:2405.03731](https://arxiv.org/abs/2405.03731), a full-proof CLAIM that must be reconciled with later literature, not assumed accepted or ignored.

This card does not certify unrestricted openness. Your first task is a multi-round primary-source check: original definitions, later papers, errata, author pages and public proof repositories. Distinguish claimed from verified solutions. Do not use other teams' task lists or exploration sequence to choose a route.

## First cycle and deliverables

Spend at most 45 minutes on the source gate, then at most 75 minutes on independent mechanism analysis. Write `SOURCE_GATE.md` with exact versions/claims and uncertainty. Compare at most two constructions and spell out the shortest chain from a generated finite family to a genuine strict counterexample. Avoid small-family censuses already covered by known theorems. Do not switch to entropy-polynomial topics from the excluded families.

Only after a clear unresolved scope and a specific mechanism are documented, allow one local exact experiment of at most ten minutes. Predetermine parameters and termination. Deliver `RESULT.md`, a transparent exact verifier and any certificate under this stream; verify set distinctness, closure and every element frequency independently of the generator. A useful obstruction is acceptable but label it as such and explain whether it changes the original problem's prospects. No long Lean library project before a result needs it.

If the source gate remains uncertain, or both mechanisms have known coverage/no new route, pause and propose one different public question about finite set systems within this reservation. A new target needs its own gate before heavy work. Never increase search size solely because a run found nothing.

At start, publish task acceptance in `STATUS.md`; at a checkpoint freeze a signed commit and write `HANDOFF.md` with hashes, commands, exact evidence, remaining gaps, and recovery conditions. A candidate original counterexample goes to independent review before being described as accepted. Do not wait for ROOT's immediate response to continue useful work within scope; avoid editing a frozen candidate until reviewers have a stable version.
