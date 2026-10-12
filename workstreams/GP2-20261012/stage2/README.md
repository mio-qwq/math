# GP2-20261012 — stage-two Kautz length-four structures

**Owner:** GP2-20261012. **Source parent:** signed stage-one commit `b45b04eeab0fc521b789d6d47b4d8b94119e8c90`.
**Scope:** independent mathematical work under `workstreams/GP2-20261012/` only; neither `main` nor frozen B/ROOT folders have been changed.

## What is proved and what is not

1. `HIERARCHICAL_MODEL.md` rigorously describes the 14 triple profiles, their two-letter/one-letter interfaces, and closure conditions. This is a model of *strict codes* rather than proof of the exact Kautz GP limit.
2. `TEN_STATE_REDUCTION.md` gives a smaller objective-preserving state representation; the independent standard-library finite checker is `verify_ten.py`.
3. `ROTATION_COMPLETION.md` gives the exact fixed level-array 2-SAT completion criterion; `FORCED_OVERLAP_BOUND.md` gives a weighted forced-word loss bound.
4. `FORCED_HYPERGRAPH_EXACT.md` strengthens the fixed-level bound via a weighted vertex-cover inequality for all finite weighted alphabets with fixed ordered-pair levels. Its **fixed six-letter instance** has 310 viable orbits, 189 forced words, 7,919 distinct forbidden hyperedges, a 64-edge disjoint matching and a 64-vertex cover. Thus every strict code compatible with that particular level array has uniform density at most **41/216**. `forced_cover_certificate.json` and `verify_forced_cover.py` independently reconstruct the full certificate without MILP/LP dependencies.
5. These reductions and fixed-instance results **do not** lower the inherited universal interval `beta <= lambda_4 <= 182/729`, and **do not** solve the general length-four exact-value problem. There is no new full-parameter Lean proof or external human peer review. Historical originality of the methods is not established.

## Reproduce (Python 3.10+; standard library sufficient)

From the repository root:

```sh
python workstreams/GP2-20261012/verify_manifest.py
python workstreams/GP2-20261012/stage2/verify_manifest.py
python workstreams/GP2-20261012/stage2/verify_stage1_signature.py
python workstreams/GP2-20261012/stage2/verify_stage2.py
python workstreams/GP2-20261012/stage2/verify_ten.py
python workstreams/GP2-20261012/stage2/verify_forced_cover.py
```

`build_certificate.py` and `build_forced_cover.py` are optional discovery/generation scripts and can need additional optimization libraries. The trusted verification commands above do not.

`logs/verification.json` contains older stage-two replay evidence, and `logs/final-replay.txt` records the latest actual execution. `MANIFEST.json` hashes the complete published stage-two file set (excluding itself), including its verifier and logs. The original stage-one manifest covers the frozen stage-one material. All executable checks reconstruct the actual directed graph or strict-window semantics rather than treating a solver's success status as proof.

## Provenance and key management

The stage-one parent carries an Ed25519 SSH Git commit signature; its signer public key is in the ancestor directory's `allowed_signers`. `verify_stage1_signature.py` verifies it without relying on the environment's `ssh-keygen` binary. The new stage-two signed commit uses a **distinct locally controlled Ed25519 OpenPGP key**. `SIGNING_KEY.asc` contains only its public key. No signing private key, credential, private prompt or agent checkpoint has been committed. GitHub's `Verified` UI indicator may differ from independently verifiable cryptographic signature validity if the signing public key is not registered in a GitHub account.
