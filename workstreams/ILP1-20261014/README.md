# ILP1: finite-window instruction scheduling

This workstream studies optimal instruction-level parallelism for a fixed program order under eager admission, bounded unretired occupancy and in-order retirement. Its idealized model is not a complete processor.

## Main results and boundaries

* The eager ROB model is exactly equivalent to unit-job scheduling after adding every precedence edge i->j with i+B<=j. Resource-event edges have substantial prior art; the general operational equivalence is Lean verified here.
* Exact optimal schedules are produced by two independently coded Python methods and an executable, proved-correct Lean enumerator. The Python implementations are not themselves formally verified.
* For arbitrary variable W with B=W+1, every finite forward program now has an exact polynomial optimizer: O(N min(B,N)(N+|E|)) time and O(N+|E|) space, by compressing uniquely forced execution segments between clear prefixes. The general excess c=B-W gives an XP algorithm. These are independently reviewed written algorithm proofs, not yet Lean proofs.
* At B=W+1 and N=kW, exact k-cycle feasibility has a stronger O(N+|E|) test: tile consecutive W-job blocks by legal singleton or boundary-swap pair macros. Rejection has a short true-edge certificate.
* At horizon H, c=B-W and S=WH-N, all feasible traces lie in a completed-set strip of width at most2c+S. The actual ROB strip theorem is Lean verified. A sharp binomial candidate count gives an independently checked exact feasibility algorithm FPT in c+S; its counting/algorithm proof remains written.
* At fixed widths2 and3, a two-input family has exact sufficient windows N and3 respectively. This example loses only one cycle at a small window, so exact saturation must not be confused with a large performance benefit.
* A different chain-prefix family has an exact approximate-saturation formula and requires a window linear in N for fixed tolerance epsilon<1/W. True indegree and outdegree are at most one.
* A universally optimal online policy exists exactly when W=1 or W>=B under the explicitly hidden-future observation model. At B3,W2 the exact strict randomized online ratio is5/4, attained by a simple fair younger-choice policy with general inequality4E<=N+3T*. The general proof has independent review, and a separate two-input repetition proof extends the sharp factors to definitions with an additive constant. The complete ROB/randomized semantics bridge is not yet Lean verified.
* A hidden-subset family gives exact family randomized/advice bounds already at true depth two. At B4,W3, the natural uniform-omission extension exceeds4/3 on a nine-job counterexample; a general optimal policy for these larger resources remains unresolved.

These are mathematical results within R1. Their correctness, formalization, independent review and originality are recorded separately. No historical-first claim is made.

## Reading and reproduction

* [MODEL.md](MODEL.md): operations, semantics, cycle boundaries and observations.
* [THEOREMS.md](THEOREMS.md): complete proofs and links to larger generalizations.
* [Research draft](paper/ilp1-research-draft.pdf) and [LaTeX source](paper/draft.tex).
* [LITERATURE.md](LITERATURE.md), [NOVELTY_AUDIT.md](NOVELTY_AUDIT.md): primary sources, related results and unresolved originality gaps.
* [STATUS.md](STATUS.md), [HANDOFF.md](HANDOFF.md), [PROBLEMS.md](PROBLEMS.md): evidence, recovery and next questions.
* `src/rob.py`: memoized exact state search. `src/checker.py`: independent operational replay and Bellman certificate checking. `src/resources.py`: compact unrestricted-width window-saturation certificates.
* `subagents/verification/constraint_solver.py`: independent exact time-assignment method.
* [CORRIDOR.md](CORRIDOR.md), `src/corridor.py`: parameterized horizon feasibility and actual-trace strip theorem. [FORCED_SEGMENT_DP.md](subagents/theory/FORCED_SEGMENT_DP.md) and its adjacent Python module: polynomial B=W+1 optimization. [PERFECT_SATURATION.md](subagents/theory/PERFECT_SATURATION.md): linear structural test and certificates.
* `formal/`: pinned Lean model, operational bridge, executable exact solver, online pair, resource proofs, actual ROB corridor and a conditional randomized-potential kernel. `subagents/formal-dp/`: general Bellman/search theorems and independent reviews. Current fresh audits cover161 distinct declarations; that count does not turn the conditional kernel into a full ROB policy proof, or verify the new Python algorithms.

From this directory:

```sh
python -m unittest discover -s tests -v
python tests/exhaustive.py --max-n 5 --random 100 --seed 20261014 --output evidence/exhaustive.json
python paper/build.py
```

Input JSON uses zero-based indices: `{"n":4,"edges":[[2,3]],"B":3,"W":2}`. Run `python src/rob.py instance.json --certificate > certificate.json` then `python src/checker.py certificate.json`.

See formal/README.md and HANDOFF.md for actual Lean reproduction commands. Do not rerun unchanged large audits merely after a session switch. This research branch determines no author list, new license, formal publication version, journal submission or DOI.
