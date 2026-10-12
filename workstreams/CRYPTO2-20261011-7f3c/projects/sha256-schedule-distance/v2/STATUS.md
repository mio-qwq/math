# SHA-256 equality-support continuation

Owner CRYPTO2-20261011-7f3c; date 2026-10-12 UTC / Asia-Shanghai.
Local baseline 7d67cc39f000783800575fff6a2f345f963ada7e.
Remote baseline 3558a51aabcf1242c2b8c40162643f9b260d937a.
Coordination and partner claims unchanged after fetch; main updated to
61488e0 and is not modified here. Frozen v1 evidence is reused, not rerun.

Same reserved object: actual SHA-256 32-bit, 64-word expansion distance.
Current goal: completely characterize all weight-13 supports allowed by
the certified necessary conditions, then derive arbitrary-base multi-step
constraints or find actual word pairs. No claim that d64=13 is known.
An all-zero-base failure is not sufficient for a universal exclusion.

First experiment is bounded: traverse only equality edges of the existing
potential certificate, count/enumerate all optimal supports, then inspect
their equations. Do not merely increase the earlier SMT timeout. A new
representation or mathematical constraint is required for further solving.
No new public number, other member's scope or file is used. No independent
review is claimed. Initial stage: equality-case analysis before computation.

## Completed mathematical checkpoint

The relaxation's weight-13 equality cases are now completely classified:
15 supports, 735 traversal nodes. A written universal 32-bit sigma-chain
proof excludes supports 3 and 14 for every base message. The exact actual
lower bound remains 13; 13 support patterns remain undecided.

A follow-up also establishes a boundary: the five shared tail equations
without the forced-H condition have an explicit satisfying word-pair
assignment. This refutes the attempted blanket extension, not any public
conjecture. TAIL.json is not a full expanded message pair.

Evidence: byte-identical equality-support regeneration, separate stdlib
checker, 256 carry cases, sigma inverse checks, 12 recurrence substitutions,
exact tail witness and seven rejected negative controls. RUNS.json records
commands, environment, exit 0 and results. Existing v1 evidence is pinned;
Z3 discovery logs are not used as proof certificates. No Lean or independent
SHA review has been done. SHA256.json freezes this checkpoint separately.

Post-discovery prior-art check confirms that general differential constraint
and carry propagation methods are established. The specific classification
was not found in the bounded search; priority remains unconfirmed. The
result is modest and does not meet the user's major-result objective yet.

Blocker: the remaining patterns are not forced into the half-word case, and
the isolated common tail is feasible. Next: retain the full earlier/base
equations and derive a different global constraint; stop this route if it
only leads to the same timeouts. HANDOFF.md records that decision gate.
