# Reproducing this release

All release proof checks use Python's standard library. From this
directory, the complete replay is:

```sh
python -B check_manifest.py
python -B verify_release.py
```

The first command checks SHA256 hashes and byte counts for this exact
release's listed files. It ignores unrelated, unlisted research files.
The second copies all listed bytes to a temporary directory, then runs
the explicitly listed checkers there. This preserves every frozen
original, including old run records from scripts whose historical
default was to write a record. The temporary copy is removed after the
run. `--record /absolute/path/outside/this/workstream/replay.json` saves
a new detailed result without modifying reviewed evidence.

The replay includes the principal local h theorem, low-12 mask
classification, irregular-support valuation proof and independent
reconstruction, exact base completion and independent reconstruction,
all seven coupled support bridges, the original RUP proof and the
separate explicit-hint verifier, the word-to-CNF audit, the four-word
sharpness object, the active-pair construction check, and small
dependencies of the older exclusions. The short affine proof and its
independent reconstruction are separately included in the command list.

For a focused replay of the already frozen propositional certificate:

```sh
python -B sha256-word-distance/coupled-review/audit_mapping.py
python -B sha256-word-distance/coupled-review/check_hints.py
python -B sha256-word-distance/coupled-review/audit_dependencies.py
```

These three commands are read-only by default. The first accounts for
all 4,939 source clauses and every original bit operation. The second
checks all 19,460 RUP additions and matches them to the original DRUP
file; it does not invoke a SAT solver. The third checks the complete
low-12 dependency, the signed-power exclusion and all 36 original
support substitutions. The short affine proof is a second certificate
of the same local impossibility, not a second improvement of the global
distance bound.

`VERIFICATION.json` describes the first signed release, commit
`363145d8eee0a62f73ae79e96e112627da458456`.
`STAGE2_VERIFICATION.json` records the subsequent actual replay. Neither
record claims that the earlier 5,308,416 transition inequalities or
735-node support enumeration were rerun here. A manifest or review
receipt binds only the exact bytes and scope it names.

Solver discovery scripts are optional and are not invoked by the
release gate. Their recorded environment was Python 3.12.14, Z3 4.15.3
(z3-solver package 4.15.3.0), and PySAT 1.9.dev15 where specified. The
`unknown` periodic query and the uncertified exploratory UNSAT runs
remain discovery data. Their status is not upgraded by this replay.
No Lean compiler or Mathlib build was run.

The full earlier-source identity check needs an unchanged snapshot of
the CRYPTO2 workstream at commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51` and a repository containing
the pinned main/CRYPTO2 commits:

```sh
python -B review/audit_frozen.py --crypto2-root /absolute/path/to/CRYPTO2-workstream --repo /absolute/path/to/math-repository
```

That check's previously executed command, exact dependencies and outputs
are in `review/RUNS.json` and `review/audit_frozen.json`. It does not
rerun the original large potential or support classification.

## Signature scope

This branch uses a new SSH signing key controlled for the CRYPTO3
workstream. The public key is in `verification/CRYPTO3-20261012.pub` and
the verifier identity mapping in `verification/allowed_signers`.

```sh
git -c gpg.ssh.allowedSignersFile=workstreams/CRYPTO3-20261012/verification/allowed_signers verify-commit HEAD
```

The fingerprint is
`SHA256:5O5l7/sGP9SVSPLXDmRiErO+mwsN5p8/RCbjcs7W47E`.
This is local cryptographic verification of the research key, not proof
of a human identity, GitHub account registration, or external endorsement.
No private signing material is included.
