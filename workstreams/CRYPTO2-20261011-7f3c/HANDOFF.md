# Handoff — CRYPTO2-20261011-7f3c

Read STATUS.md, RESULT.md and **PROOF-v2.md** first. The result is a complete
universal mathematical theorem with independent-agent review, not a cipher
attack. Historical originality remains unresolved. No background work is
promised after this session.

## Ownership and repository boundary

- Branch: `partner/dist-CRYPTO2-20261011-7f3c`.
- Exclusive directory: `workstreams/CRYPTO2-20261011-7f3c/`.
- Baseline: `a8c3f22e26b08c2d294e2b0e6df2d9cfa430cda0`.
- Coordination snapshot: `abd8e85628b1348f250c5d5c46a5450caae2876d`.
- No main, root README, shared dependencies, 006 paper, or other member's
  workstream was modified. No public result number was assigned.
- The CRYPTO recovery archive was not available/read/applied. Its APN and
  SHA3 results were neither reviewed nor taken over. No direct conversation
  with Sora or a separate project-main agent is claimed.

## Mathematical delta

For every characteristic-two field and every invertible circulant M of
order n>=3, construct distinct nonzero u,v satisfying the coordinatewise
relations R(u,v) and R(Mu,Mv), where R(x,y) means x_i y_i(x_i+y_i)=0.
Known odd-order and multiple-of-four bases are attributed. The proposed
new application is the periodic subspace MJ=JB: repeating quotient pairs
settles n=2 mod4, hence the orders left open by the inspected KYS version.
The same weight identity proves MDS descent. n=2 is excluded by a real
MDS counterexample. Neither a finite test nor a quotient rank calculation
is used as a replacement for the full proof.

The unnumbered remaining-order direction comes from KYS,
arXiv:2605.27535v1, Theorem 5 and Section VI. SOURCE-GATE.md records exact
retrieval limits, subsequent-paper checks and originality risk. This is
plausibly a focused structural note, with no claim of major cryptanalytic
impact or historical firstness.

## Version and review history

- PROOF.md is frozen v1, including the now-corrected ancillary wording.
- PROOF-v2.md is authoritative; its SHA256 is
  `71d5a5dc6e757402db8b54a15507ffd6e4e8e87eec0f4f4fe438c21f6cf55d91`.
- review/PRE-DISCLOSURE.md records the reviewer's reconstruction before
  reading the discoverer's proof. review/REVIEW.md reviews pinned v1.
- review/ADDENDUM.md establishes MDS descent and corrects the earlier
  implication of nonpreservation, including the reviewer's own wording.
- review/V2-RECEIPT.md binds the final revised proof file to its review.
- SHA256.json freezes the complete delivered directory except itself and
  ignored build/cache files. Later mathematical changes require a new
  version/receipt rather than silently editing these frozen proofs.

## Reproduction

Run from the repository root. Python 3.12.14 was used, standard library
only. g++ 13.3.0 was used for optional reconstruction of the MDS fixture.
Actual commands, outcomes, timings, source hashes and exit codes are in
RUNS.json; independent-agent commands and environment are in review/.

```sh
python workstreams/CRYPTO2-20261011-7f3c/check.py workstreams/CRYPTO2-20261011-7f3c/certificates/mds10.json --negative
python workstreams/CRYPTO2-20261011-7f3c/verify_mds.py workstreams/CRYPTO2-20261011-7f3c/certificates/mds10.json
python workstreams/CRYPTO2-20261011-7f3c/regression.py
```

The first two commands are read-only and print results. The last reproduces
3,710 checks but rewrites REGRESSION.json with a new elapsed time and the
deterministic witness file; run it in a fresh checkout/copy if preserving
the frozen manifest. Do not use Python -O: assertions are part of the
regression's test harness. inspect independent_check.py before rerunning,
since its output file is also a frozen review record.

The constructor uses row elimination; check.py directly validates raw
coordinate products and uses distinct field arithmetic and rank routines.
verify_mds.py checks every square minor by division-free Laplace recurrence,
not the C++ discovery program's elimination/table arithmetic. These are
same-author implementation separations; independent-agent review is
separately identified. Negative controls include bad field encodings,
reducible modulus, zero/equal vectors, corrupt products/quotients and a
zero-entry non-MDS matrix. Exhaustive and sampled parameter sets are
explicitly separated in REGRESSION.json.

## Publication transport

Native git push returned exit 128 (no local HTTPS credential provider).
Authorization was not withdrawn. The GitHub connector published the
reservation at `b407c26994978afc7432cf505d8d78cdd9712ff9`; its tree matches
the local signed reservation commit
`141b9df2921f7da287608bb3e7c23647ceff1676`.

Final publication uses a fast-forward connector commit from the remote
reservation, guarded by the expected head. The final local signed snapshot
and connector commit can have different commit IDs with identical trees.
Connector commits are unsigned; no GitHub-verified signature is claimed.
The final chat receipt supplies the actual published commit after fetching
it and comparing trees. No credentials or signing private material belong
to this directory. The signed local lineage is preserved, not reset.

## Next action and stopping rule

Do not expand the already adequate finite tests. Obtain the missing latest
full texts listed in SOURCE-GATE.md and search equivalent invariant-code,
periodic restriction and circulant quotient formulations. If an existing
same-scope result appears, attribute it and close the novelty route. Until
then describe the theorem as rigorously proved here with independent
mathematical review, with originality unconfirmed. No author contact,
submission, DOI/preprint publication or main merge was authorized/performed.
