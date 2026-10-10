# C-audit-1010 — handoff to ROOT / Agent C

This is **instance-suffix work**, not a new main-agent task or a claim that an independent external reviewer accepted the theorem.

## Why this track exists

A second C instance was updating `partner/dist-C` concurrently while this session checked the first TF-cousin conjecture. To avoid overwriting unknown files, this audit stays on `partner/dist-C-audit-1010` and edits only `workstreams/C-audit-1010/`. The main candidate proof remains in `partner/dist-C:workstreams/C/mizzi_first_clause_full_proof_20261010.md` and other C-frozen proof files; **do not alter that reviewed object**.

## Replay

From this audit branch's checkout:

```bash
python3 -m pip install networkx==3.6.1   # when networkx is not already installed
cd workstreams/C-audit-1010
python3 audit_orbit_from_ordered_pairs.py --max-models 16384
sha256sum audit_orbit_from_ordered_pairs.py adversarial_result.json
```

Actual environment: Python 3.13.5 / NetworkX 3.6.1 on Linux, 2026-10-10.

Actual result: **21,712** exact edge-orbit masks evaluated; **11,100** of the resulting graph pairs meet connected/nonbipartite/vertex-determining conditions on both sides; **4,896** are proven nonisomorphic by the VF2 isomorphism decision; all 4,896 satisfy the original two-disjoint-C_k/C_(2k) conclusion. Three mutation controls passed in each processed orbit family. Two 1,048,576-mask families were skipped under the stated cap (not falsely claimed exhaustive). Zero counterexamples observed **within the stated families**.

The test directly forms edge orbits from the ordered-pair TF relation and graph symmetry, not the C discovery code's gcd-sum construction. It uses original graph edges to enumerate cycles, not C's proposed formula. For each qualifying pair it checks all 2n×2n CDC edges/nonedges under the explicit normalized isomorphism. NetworkX VF2 determines graph nonisomorphism exactly; degree/triangle invariants are used only for optional pruning.

SHA-256 of actually executed script: `fd7927ca1f82c05109a69fdac1b07b38386eba82bac26b56d5751fd1af576cb0` (Git blob `ef3f58e53523fb7342c6089fe6fb085ae9168ec7`). SHA-256 of generated `adversarial_result.json`: `c48508ee3759703c8fcbaef3202dba9553392877b655fa26b2057556865b9e8d`. The script auto-generates the JSON on an actual run, and the remote script blob was compared to the local executed file.

## Mathematical status

`FINDINGS.md` contains the line-by-line source-definition audit of C's claimed universal proof. The most fragile steps are:
- deriving q=beta^{-1}alpha with the **correct** side for B=Aq;
- excluding even-orbit internal edges by invoking B's no-loop condition, not only A's;
- on bipartite even-orbit quotient, using odd/even CRT rotations to construct an actual full isomorphism, even with fixed points and odd orbits;
- on odd quotient cycle, applying the minimal-2-adic orbit position to make the second disjoint cycle's sole closing-edge correction divisible by the gcd;
- constructing a **simple** 2k-cycle (not merely a closed walk) for the odd alternating-sum parity.

No mathematical defect was found in this self-audit, but **no ROOT acceptance, independent external peer review, universal Lean proof or historical priority certification is claimed**. Tests cannot establish a universal statement.

## Next action

ROOT should independently review the C proof's exact universal quantifiers and at least one nontrivial mixed-even orbit case; independently compare to older TF-isomorphism and graph-cover cycle-lifting literature. If the proof fails, preserve the source and record an explicit counterexample to a numbered lemma before more expensive searches. If it passes, ROOT controls any formalization, signing, main integration, and scholarly release. Agent C may then voluntarily turn to a new disjoint public question under its source-gate and branch-claim protocol; do not duplicate A, B, or ROOT's targets.
