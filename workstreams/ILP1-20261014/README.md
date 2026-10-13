# ILP1: finite-window instruction scheduling

This workstream studies optimal instruction-level parallelism for the explicitly specified eager, in-order-retiring, unit-latency ROB model. It does not model an entire real CPU.

* [MODEL.md](MODEL.md): semantics, information boundaries and exact window convention.
* [THEOREMS.md](THEOREMS.md): complete written proofs of the static precedence reduction, exact dynamic programming, bounded-window state count, resource formulas and small counterexamples.
* [STATUS.md](STATUS.md) and [HANDOFF.md](HANDOFF.md): current verification and continuation state.
* `src/rob.py`: complete-state exact solver, returning a schedule and optional Bellman potential certificate.
* `src/checker.py`: independently coded operational replay and lower-bound checker.
* `tests/`: boundaries, counterexamples, certificate tamper controls and finite exhaustive audits.

Run from this directory:

```sh
python -m unittest discover -s tests -v
python tests/exhaustive.py --max-n 5 --random 100 --seed 20261014 --output evidence/exhaustive.json
```

Input JSON uses zero-based indices: `{"n":4,"edges":[[2,3]],"B":3,"W":2}`. Run `python src/rob.py instance.json --certificate > certificate.json` and `python src/checker.py certificate.json`.

The initial search identifies older processor event-graph work that already represents finite ROB capacity by precedence edges. Bellman recursion, list scheduling and longest-path layering are classical. Nothing here is yet a claim of historical priority, a solution to a classical scheduling open problem, or a real online optimal processor implementation. Subsequent independently developed proofs, literature audits and actual Lean logs are integrated as they are reviewed.

This is research in progress. No manuscript author list, new license, journal submission or DOI release is determined by this workstream.
