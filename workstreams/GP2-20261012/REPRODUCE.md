# Reproduction and validation boundary

All paths below are relative to the repository root. The mathematical
checkers use Python's standard library unless an exploratory file explicitly
says otherwise. Python 3.12.14 was used for the recorded executions.
No optimizer is required for the main theorems.

## Independent seven/nine-window and repair checks

```sh
python workstreams/GP2-20261012/review/independent_window_check.py
python workstreams/GP2-20261012/review/independent_collision_check.py
python workstreams/GP2-20261012/review/independent_collision_check.py --verify-certificate workstreams/GP2-20261012/review/independent_collision_certificate.json
python workstreams/GP2-20261012/review/independent_repair_check.py
```

The collision certificate reconstructs all 877 restricted-growth words of
length seven. It retains occurrence multiplicities and original-graph
distances. Every capacity has an attaining set, and every subset above
capacity has an explicit shortest-path triple. The replayer checks these
finite objects, parameter bindings and deliberate corruptions.

The universal moment identity and the `73m^3` deletion theorem are written
proofs, independently reviewed in the adjacent Markdown files. Their truth
for arbitrary alphabets is not inferred from the small graph audits.

The exact integer finite upper bound can be evaluated, for example, by

```sh
python workstreams/GP2-20261012/cyclic_moments/bound.py 100
```

It tests the sign of an integer quadratic and returns the exact floor,
with residuals at the boundary; no numerical square-root rounding is used.

## Independent lower construction checks

```sh
python workstreams/GP2-20261012/construction/verify_lower18.py
python workstreams/GP2-20261012/construction/verify_jiggs57.py
```

These commands generate deterministic certificates and replay the finite
original graph cases. They may rewrite their own certificate files with the
same content. The saved execution logs and provenance files record actual
successful runs, not planned commands.

For the eighteen-word code, all 6561 block words and all ambient BFS
distances at `m=3,4,5,6` were checked. The arbitrary-block polynomial and
balancing identity were checked coefficient by coefficient in `Z[x,y,z]`.
Eight deliberate changes to the object or certificate were detected.

For the 57-word code, all 65536 block words, all 3249 ordered codeword
concatenations and all 9747 interior windows were checked. Original-graph
distance audits at `m=4,5,8` cover the stated fixed lifts. The original
dictionary's historical maximality is neither assumed nor recomputed.

The separate weighted reviewer reconstructs the rotation orbits, the exact
four-variable polynomial, the sum-of-squares compression, the rational
`(5,5,3,3)` count and an isolating interval for the unique algebraic maximum.
The actual log and precise reviewed hashes are in its directory. Replay it
without rewriting any certificate:

```sh
python workstreams/GP2-20261012/weighted_review/verify_weighted_jiggs57.py --negative-controls
```

The checker pins the literal dictionary and revision 2 of the proof. It uses
only integers and exact rational arithmetic; all nine negative controls are
actually executed by the command above.

## Structural continuation files

```sh
python workstreams/GP2-20261012/construction/verify_fourteen_state_reduction.py
python workstreams/GP2-20261012/review/independent_fourteen_state_check.py --verify workstreams/GP2-20261012/review/independent_fourteen_state_certificate.json
python workstreams/GP2-20261012/global_upper/verify_endpoint_structure.py
```

These are finite semantic checks of separate all-alphabet structural
proofs. They do not certify a maximum code size. Any files named `probe_*`
or `discover_*` are exploratory discovery tools, and are not dependencies
of the main universal inequalities. In particular the independent upper
checker does not import the discovery-side distance code.

## Hashes, signed commit and restoration

The root manifest `MANIFEST.json` records the SHA256 of each file included
in the mathematical package and the precise inherited commit references.
Individual review/provenance manifests also bind their own reviewed sources.
The root manifest does not include itself in its own hash list.

```sh
python workstreams/GP2-20261012/verify_manifest.py
```

The public `allowed_signers` file contains the dedicated verification key.
For a frozen commit, run:

```sh
git -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=workstreams/GP2-20261012/allowed_signers verify-commit HEAD
```

The self-contained Git bundle in the handoff archive includes the main
ancestry needed to restore the branch without modifying any existing branch.
The archive's restoration note gives the exact verified commit and bundle
hash. A private signing key is not included in any mathematical file,
commit, bundle or archive.

## Formalization boundary

The requested version was official Lean 4.34.1. The downloaded release
archive had SHA256
`47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4`.
Extraction succeeded. Running the unchanged executable with `--version`
exited one with `error: failed to locate application`. No Lean source was
accepted in this run, and no new proof was compiled. The environment issue
was not worked around by altering access controls or the toolchain.

Accordingly there is no new Lean axiom report to present. No `sorry`,
`admit` or unproved axiom has been introduced as a substitute for a proof.
The inherited Mathlib pin is unchanged; none of its previous successful
builds is counted as a current execution.
