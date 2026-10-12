# Unrestricted actual three-pair core: one bounded probe

**Unresolved.** The one authorized Z3 QF_BV query returned `unknown`
with reason `timeout`, after 15.0023 seconds. There is no SAT witness
or certified UNSAT result. No seed sweep, retry or time extension was
performed. This result excludes no input difference or support.

`PLAN.md` fixes the six actual-word model, modular equations, parameter
budget and acceptance protocol before the query. The derived nonzero
D is unrestricted: no high-valuation ceiling or fixed base is imposed.
The object is only the necessary three-pair core, not a base schedule.

`probe-01/MODEL.smt2` is the exact solver query, and `probe-01/RESULT.json`
contains Z3 version 4.15.3, settings, solver statistics, reason for UNKNOWN
and source hashes. `RUN.json` records the real process command and exit.
`SOURCES.json` additionally hashes the available Z3 Python and native
library files. `SHA256.json` freezes the whole directory apart from itself.

For audit, inspect the model and frozen JSON without running a solver.
`verify_model.py` is a read-only independent output-bit arithmetic checker
for a future six-word SAT candidate. It was **not executed against a SAT
model in this run**, because no such model was obtained. It imports no
solver or model-generation function. Its reverse-orientation and four
malformed controls therefore carry no new execution claim here.

The reproducibility script performs exactly one 15000 ms query and requires
a new output directory; it refuses to overwrite an existing one:

```sh
PYTHONPATH=/workspace/scratch/b1d6bae025af/crypto3-deps python -B run_probe.py --out-dir NEW_REPRODUCTION_DIRECTORY
```

That is an explicit solver replay, not the default audit command. It was
not run a second time for this stage.
