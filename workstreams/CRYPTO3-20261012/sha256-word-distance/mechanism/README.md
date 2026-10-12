# Irregular-support mechanism result

**Candidate written lemma, pending independent review.** For frozen
size-13 SHA-256 support indices 6, 7, 12 and 13, a specified repeated
nonzero word difference cannot be divisible by 2^21. This narrows an
actual-message necessary condition; it does not exclude any entire
support and leaves the universal distance bound at 13.

The complete proof is `VALUATION_BOUND.md`. Its logical dependencies
are the original SHA-256 recurrence, the four exact frozen supports,
eleven sigma1 masks, ten carry-gap positions and one XOR row identity.
`STRUCTURAL-CERTIFICATE.json` and `check_structural.py` provide the small
finite dependency check, including six damaged controls. No SMT result
or large enumeration is a premise of the written proof.

The direct-bit positive checks demonstrate two exact limits: the twin
core without one early equation remains feasible at D=2^31+2^21, and
the isolated sigma0 two-cycle is always feasible for a permutation of
an even cyclic group (`TWO_CYCLE_BOUNDARY.md`). These are not complete
message-pair witnesses. The generic twin witness and twelve stored
high-valuation twin witnesses are verified independently of their
generation routines by `check_twin_witness.py`.

Read-only replay, supplying the frozen support file:

```sh
python reproduce.py --supports PATH/TO/FROZEN/v2/supports.json
```

Adding `--cross-check` also runs the separately written Boolean-truth-table
and F2 traversal of all 121 fixed-difference carry cases. That checker is
by the same researcher, so it is not an independent-agent review. The
discovery traversal and SMT run files are retained as actual exploratory
evidence. The further D=2^20 and D=3·2^20 triple-core UNSAT results have
no claimed mathematical exclusion attached to them.

`RUNS.json` records actual replay exits and source hashes. `provenance.json`
pins the original commit and exact dependency files. There is no Lean
formalization or collision/preimage attack claim in this result.
