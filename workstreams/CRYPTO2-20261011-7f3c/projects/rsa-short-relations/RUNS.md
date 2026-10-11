# Reproducibility and actual run scope

All paths below are relative to this project. Exact environment, argument
vectors, stdout, stderr and exit codes are in RUN-RESULTS.json.

The independent **implementation** checker needs only Python's standard
library. It is not an independent human review of the proof.

```bash
python check.py
```

It reconstructs the BD generators by integer polynomial arithmetic, checks
the supplied unimodular transformations by exact multiplication and
Bareiss determinant, verifies each norm and each root directly, and proves
the small fixture primes by trial division. It checks the factor and
recovery witnesses without importing discovery code, Sympy or FLINT.
The count scan is regression only; the all-parameter argument is the
symbolic proof. No claim about the internal correctness of FLINT's LLL
implementation is needed for these certificates.

Discovery dependencies are Python 3.12.14, Sympy 1.14.0, python-flint 0.8.0
and its installed mpmath 1.3.0 dependency. They were installed outside the
repository with:

```bash
python -m pip install --target /workspace/scratch/62f6e8a57d75/crypto2-python sympy==1.14.0 python-flint==0.8.0
```

No shared dependency file was changed. Full deterministic certificate
regeneration and public-input extraction are checked with:

```bash
PYTHONPATH=/workspace/scratch/62f6e8a57d75/crypto2-python python reproduce.py
```

The reproduction driver reconstructs these discovery commands:

```bash
python probe.py --bits 96 --m 2 --t 0 --num 1 --den 5 --out evidence/control-96-m2-t0.json
python probe.py --bits 96 --m 4 --t 2 --num 13 --den 50 --out evidence/probe-96-m4-t2.json
python probe.py --bits 96 --m 6 --t 1 --num 13 --den 50 --skip-factor --out evidence/probe-96-m6-t1.json
python make_quadratic.py --out evidence/quadratic/synthetic.json
python make_general.py --out evidence/general/synthetic.json
python recover_general.py evidence/general/synthetic.json
```

`--bits 96` is a generation parameter; the saved RSA modulus is actually
95 bits. The private exponent is chosen near the supplied rational power,
with coprimality adjustment; no strict attack-exponent claim is inferred.
Timing is printed to stdout and excluded from deterministic certificates.
The replay uses fresh temporary paths and compares bytes before deletion.

Actual outcomes: checker PASS, including 12 negative controls; replay PASS
with five identical JSON files. The three LLL diagnostics have dimensions
6/25/35 and respectively 3/0/0 HG-certified rows. They have 3/6/15 rows
actually vanishing at the disclosed key. The quadratic synthetic recovery
passes for both coefficient signs; the general extraction succeeds for
degrees 3 and 12. These are conditional theorem controls, not evidence of
a better attack or success probability on unknown keys.

A nominal 256-bit, m=8,t=2 diagnostic was stopped with exit 130 before
saving output. It is recorded in FAILURES.md and is not included among
verified results. There is no running research job left by this checkpoint.

SHA256-v1.json freezes source, proof, certificate, and run-record bytes.
Use a new version for later mathematical changes. The claim base is remote
3b651069e690bc237faa6c608de895f532160736 / local
cde6a3a6331e1e883261193e33839e7cb36b2d20, with identical trees. The later
publication receipt is outside this frozen project, in the owner's
RSA-PUBLICATION-v1.json; it must contain actual verified commit IDs.
