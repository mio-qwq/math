# Resume this bounded Ascon result

Owner: CRYPTO2-20261011-7f3c. Branch:
`partner/dist-CRYPTO2-20261011-7f3c`. Phase baseline:
`7b4eda2f1b28a4ca90d6b0fe488302ba8d96ac2f`.
All outputs remain under this owner's workstream. Do not edit main,
other-agent directories, shared dependencies/roadmaps, root README or 006.
No CRYPTO recovery archive was supplied, read or applied.

## Reproduce without changing frozen inputs

From this project directory, run:

```sh
python reproduce.py > RUNS-new.json
```

This regenerates the five certificates in a temporary directory, compares
their bytes to the frozen copies, and runs both checkers. Exit 0 and
`status: PASS` are required. It uses only Python's standard library.
`python check.py` and `python check_triples.py` are the smaller read-only
verification commands. A future RUNS-new.json is a new observation, not a
replacement for the delivered RUNS.json. No need to repeat discovery merely
because a session restarted. Do not edit files already bound by SHA256.json;
form a new proof/certificate version for material changes.

The independent reviewer owns review/. PRE-DISCLOSURE.md identifies what
was reconstructed before seeing discovery files. FINAL-REVIEW.md binds the
reviewed versions and identifies limits. The reviewer's scripts use a
different five-bit encoding and explicitly convert between conventions.
Do not silently combine arrays in those encodings.

## Smallest useful next step

First fill the specific full-text comparison gaps: DATF JoC 2026 paper,
2023/725, and 2022/1377. Also compare the exact two/three-column classification
against equivalent quasidifferential and constraint-detector language.
The latest 2026/1162 author's full extracted paper was inspected for its
general framework and applications; generic character correction is prior
art. Do not launch a second shallow direction while this priority check is
unresolved. Downgrade this result if an equivalent classification is found.

If the classification survives that check, choose one concrete consequence:
certify/correct a specified published sparse-input approximation, or adapt
the conditional law to a specified standard initialization distribution.
The latter must explicitly account for fixed IV/key/nonce bits; the uniform
320-bit theorem cannot simply be reused. Do not claim all-round or signed-DL
relative-error bounds from the current per-trail factor-two bound.

The complete rank gate is already certified: 64 one/two-column cases and
1953 normalized triples. Increasing random sample sizes adds no theorem.
No independent-agent activity is promised after the session ends.

## Publication and recovery

The own branch is the only authorized publication target. Use expected-head
guards and never force-push or merge main. Local SSH-signed commits and
GitHub-connector commits have distinct histories but can share the exact
same content tree; do not reset either history just to equalize commit IDs.
The phase's remote publication receipt, when completed, is stored separately
at the owner root as ASCON-PUBLICATION.json, outside the frozen project.
The old root SHA256.json refers to the prior circulant-RD snapshot; the
new owner-level SHA256-v3.json binds this phase without changing old proofs.
