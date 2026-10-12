# Independent full replay of the inherited SHA-256 gate

**Accepted in the scope of `REVIEW.md`: written mathematics plus an
independently implemented, complete finite-certificate replay.** This is
independent AI-assisted review, not Lean or external human peer review.
The actual 64-word distance remains at least **13**; attainment of 13
and a lower bound of 14 remain open.

The eight pinned CRYPTO2 source artifacts are included under `sources/`.
`PROVENANCE.json` records their original paths, Git blob identities,
byte counts and SHA256 hashes at commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`. No Git checkout, solver,
third-party Python package, or discovery module is needed to reproduce.

From this directory, the default replay is read-only:

```sh
python -B check_independent.py --negative
```

From the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/inherited-gate-v4/check_independent.py --negative
```

The checker prints its result to stdout. An explicit `--output PATH`
option is available to write a new result; omit it for read-only replay.
Frozen outputs must not be overwritten.

`VERIFICATION.json` and `RUN.json` record the new successful execution.
The stdout copy is `CHECK.stdout.json`; stderr was empty.
`RECEIPT.json` pins the accepted versions and scope. `SHA256.json`
freezes all other files in this directory.

The new run verifies all **5,308,416** transition inequalities,
**65,535** nonzero initial-state bounds, **65,536** terminal zeroes,
**64** right-inverse columns and **128** basis-composition identities.
Complete equality-path traversal yields **735** nodes and exactly
**15** supports. The universal exclusions of indices **3** and **14**
and the deliberately feasible non-H tail boundary are checked as well.
All **15** malformed controls are rejected.

This fills the deliberately deferred full-replay scope of the earlier
`../../review/review.md`; it does not change those frozen source bytes
or extend any local result to an actual distance-13 message pair.
