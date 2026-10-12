# SHA-256 checkpoint and next decision

Owner CRYPTO2-20261011-7f3c; 2026-10-12 UTC. Read STATUS.md, CANDIDATES.md
and PROOF.md. All work here is by the same researcher; the separate
checker is NOT independent-agent review. Awaiting independent review.

Established: any distinct pair of 512-bit input blocks differs in at
least 13 of the 64 expanded 32-bit words. A finite integer potential
certificate and sigma inverse columns prove this; no bit-width reduction.
The support-only relaxation has minimum exactly 13. We have no actual
message pair attaining 13, and no improvement in hash attack complexity.
This does NOT yet meet the user's important-original-result standard.

Actual validation (exit codes and environments in RUNS.json):
```sh
python workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/reproduce.py --output /tmp/sha-distance-runs.json
```
Discovery requires NumPy (actual version in RUNS.json); certificate
checking requires only the Python standard library. Reproduction uses a
temporary file and compares certificate bytes with the frozen copy.
It checks 5,308,416 inequalities, both complete inverse bases, the
zero-base arithmetic contradiction and five damaged/false controls.
No need to rerun optional SMT to verify this lower bound.

Bounded lifting probes used z3-solver 4.15.3.0 in an isolated scratch
dependency directory, without changing shared repository dependencies:
```sh
PYTHONPATH=/path/to/isolated-z3 python workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/lift_probe.py workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/certificate.json --output /tmp/lift-runs.json --timeout-ms 20000
```
Actual command exit 0; two solver outcomes in LIFT-RUNS.json.
Zero-base was unsat; PROOF.md now gives a separate direct arithmetic
contradiction, so no solver UNSAT proof is trusted. Unrestricted base
returned unknown/timeout. This gives no negative theorem for real pairs.

Failures/limits:
1. Binary support alone saturates at 13, proved by a support witness.
2. Lifting that witness from an all-zero base is impossible.
3. The unrestricted lifting search timed out; not evidence of nonexistence.
4. No probability, standard-IV output collision, preimage or complexity
   improvement follows. No full SHA-256 security claim follows either.
5. Originality remains uncertain. Latest 39-step claims and local
   conditional-affine work are recorded and avoided.

Next concrete research step: classify the equality supports at weight 13
and derive multi-step modular constraints for arbitrary base words.
Before spending significant SAT time, identify an elimination relation
that is stronger than existing generalized bit-condition propagation.
Only a real lifting witness or a proof excluding ALL equality supports
could settle sharpness. Eliminating this one pattern does not prove 14.
If no such relation or attack-relevant implication emerges, retain this
as a baseline and redirect toward a distinct SHA-256 attack bottleneck.
Do not keep running longer versions of the same timeout.

Post-result prior-art check:
- Searches for thirteen active words, nonlinear expansion distance,
  stopping sets and minimum-weight variants found no exact same statement;
  absence in search is not evidence of priority.
- Eichlseder, Differential Cryptanalysis of Symmetric Primitives (2018),
  Chapter 7, Sections 7.2.3–7.2.4, was inspected:
  https://tugraz.elsevierpure.com/ws/portalfiles/portal/19191305/thesis_print_bib.pdf .
  Word supports, cancellations and generalized bit-condition propagation
  are established prior machinery. We claim no new method.
- NIST first hash workshop report (2005), SHA-256 panel, pp. 5–6:
  https://csrc.nist.gov/csrc/media/events/first-cryptographic-hash-workshop/documents/hashwshop_2005_report.pdf .
  It already distinguishes expansion-weight questions from actual
  collision-complexity implications; we retain that distinction.
- A Simple and Provably Good Code for SHA Message Expansion, ePrint
  2005/247, surfaced as relevant prior art but full PDF access failed.
  It and later code-distance work remain explicit coverage gaps.
- Parallel Search reached its free-tier rate limit during the follow-up
  gate; ordinary web search remained available. No API key requested,
  access restriction bypassed, author contacted or external artifact run.

No process is promised to run after this session. Frozen manifest is
SHA256.json; subsequent mathematical changes need a new version.
