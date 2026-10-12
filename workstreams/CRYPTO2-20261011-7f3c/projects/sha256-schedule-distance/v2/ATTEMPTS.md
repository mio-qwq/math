# Actual attempts and limits

All work here was performed by CRYPTO2-20261011-7f3c. No subagent reviewed
the SHA result. Prior independent reviews of circulant/Ascon work do not
extend to this project.

1. Complete equality enumeration: 15 initial states and 15 complete
   supports, 735 visited nodes. This uses the frozen 5,308,416-inequality
   certificate; repeating that full enumeration was unnecessary.
2. A genuinely different lifting model from v1: independent actual word
   pairs with all 48 modular difference equations, but without the
   base-message expansion equations. UNSAT implies actual impossibility;
   SAT would not itself be an actual message pair. Z3 4.15.3 was used only
   for discovery, in an isolated package directory.
3. RELAXATION-RUNS.json: support 0 timed out at 15s; 3 and 14 returned
   UNSAT in 6.533s and 11.228s. RELAXATION-OTHER-RUNS.json: 5,6,8,10,11,12
   each timed out at 10s. None of these unknown results establishes
   satisfiability or impossibility. No longer-timeout rerun was performed.
4. core_probe.py obtained the seven named constraints in CORE.json.
   Its initial run failed with exit 1 because all-zero recurrence
   tautologies were Python bools, not Z3 BoolRefs. Skipping true tautologies
   fixed this; the completed run exited 0. Core deletion is not a trusted
   UNSAT certificate. It only helped locate the now-written contradiction.
5. An isolated six-word SMT version of the chain also returned UNSAT
   (0.871s), but this one-off timing is not a frozen proof artifact.
   The delivered proof does not depend on this solver result.
6. The first checker execution rejected an incorrectly transcribed decimal
   inverse constant, exit 1, reason `sigma1 half inverse`. The correct
   value is 3337530070 = 0xc6eeaad6; the hexadecimal proof value was correct.
   Final check passes and intentionally tests the corrupted-constant case.
7. No larger Lean project was started. Local Lean documentation shows
   bv_decide uses compiled reflection; no unreported trust extension was
   introduced. The SHA proof here is a written proof with a finite-data
   checker, not a claim of Lean completion. Previous RSA Lean is separate.

Discovery commands (from repository root; observed completed exit 0 except
the explicitly recorded first core run):

```sh
PYTHONPATH=/workspace/scratch/62f6e8a57d75/crypto2-smt python workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/probe_relaxation.py --indices 0,3,14 --timeout-ms 15000 --output workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/RELAXATION-RUNS.json
PYTHONPATH=/workspace/scratch/62f6e8a57d75/crypto2-smt python workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/probe_relaxation.py --indices 5,6,8,10,11,12 --timeout-ms 10000 --output workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/RELAXATION-OTHER-RUNS.json
PYTHONPATH=/workspace/scratch/62f6e8a57d75/crypto2-smt python workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/core_probe.py
```

These discovery scripts overwrite their output paths; rerun only into an
unfrozen copy. Final verification is stdlib-only and does not need Z3.

8. Follow-up falsification of the unforced shared tail: tail_probe.py
   found a satisfying assignment in 0.391s, exit 0. TAIL.json contains the
   exact words; the separate checker verifies all five equations. Thus a
   blanket extension of the half-word contradiction is false. This is a
   useful stopping boundary, not an actual pair of expanded messages.

```sh
PYTHONPATH=/workspace/scratch/62f6e8a57d75/crypto2-smt python workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/tail_probe.py workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/v2/TAIL.json
```
