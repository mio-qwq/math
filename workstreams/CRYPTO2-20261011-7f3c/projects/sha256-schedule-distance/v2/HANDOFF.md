# Resume SHA-256 v2

Read PROOF.md first, then SOURCE-GATE.md and ATTEMPTS.md. Owner and branch:
CRYPTO2-20261011-7f3c / partner/dist-CRYPTO2-20261011-7f3c. No task card
for this ID was visible. Latest checked main was 61488e0; coordination
abd8e85628b1348f250c5d5c46a5450caae2876d. Main and other owners untouched.

What is established: exact complete list of 15 size-13 supports under the
v1 necessary conditions, and a universal 32-bit sigma-chain contradiction
excluding indices 3 and 14 for arbitrary base messages. The remaining 13
are undecided. Actual lower bound remains 13, no upper witness and no
attack. Awaiting independent review; historical originality unconfirmed.

Run from repository root:

```sh
python workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/reproduce.py
```

This regenerates supports to a temporary directory byte for byte, checks
complete equality traversal, all finite proof dependencies, recurrence
substitutions, the exact tail witness and seven negative controls.
RUNS.json records the actual run.
SHA256.json freezes this v2 content; parent certificate.json is a pinned
dependency, not copied or modified. On a wholly fresh verification, also
run the parent's check.py certificate.json --negative once; its earlier
actual verification is documented in the parent RUNS.json.

One further decision has already been resolved: the five shared tail
equations have an explicit satisfying word-pair assignment in TAIL.json,
checked directly. Removing the forced-H assumption destroys the present
contradiction. Do not rerun that tail question or count the tail witness
as a full message pair.

Next useful mathematical step: determine whether the remaining 13 patterns
force a contradiction through the repeated sigma0/sigma1 chains WITHOUT
assuming a fixed base word. First classify their recurrence-equation
families under valid index shifts, keeping boundary equations. For the
tail shared by supports 5,10,11,12, the present chain has an unrestricted
delta_34, not a forced H; substituting H without proof is invalid. A useful
extension must constrain that free difference, or couple the base-schedule
equations to the word-pair differences. A real witness must supply both
16-word inputs and verify all 64 words from the original recurrence.

Decision gate: do not spend more on the same SMT encoding/timeouts or
enumerate extra small samples. Continue only with a new exact constraint,
a validated real pair, or a substantial source finding. If these attempts
give no additional constraint, park the distance route as a modest lemma
and return to the screened standard-IV reduced-round SHA targets. No
other team's collision construction or sequence is to be copied. Any
important candidate requires a new equivalent-form prior-art check.

No SHA Lean result, independent review, collision probability, attack
time/data/memory estimate, or post-session background work is claimed.
