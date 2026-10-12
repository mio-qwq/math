# CRYPTO3 branch publication status

This research-only branch was uploaded via the GitHub connector on 2026-10-12. **This new GitHub API commit is unsigned.** It is a byte-faithful publication copy of the CRYPTO3 stage-2 source snapshot plus a separate later stage-3 candidate. It is **not** the original SSH-signed CRYPTO3 commit `1af7a5a95aa81d67df87ea201b807451ca7a0e2d`. The signed commit exists in the separately delivered handoff Git bundle; no claim is made that the original signature has been retained on this branch.

## Snapshot and one transport exception

The 204 stage-2 files are taken from the frozen source handoff. The **single transport exception** is `sha256-word-distance/coupled-boundary/boundary.rup.jsonl` (12,444,726 bytes): GitHub's connected upload transport rejected the uncompressed payload. The exact original bytes are instead stored as `boundary.rup.jsonl.xz` (2,437,244 bytes). To recover the original name and verify its SHA256, run from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/coupled-boundary/restore_evidence.py
python -B workstreams/CRYPTO3-20261012/check_manifest.py
```

The expected restored original SHA256 is `cd1845cdde5fca010b4b8557bcb27947eb5aef50b45856619cce7d54608540c5`. Original stage-2 files and their `SHA256.json` have **not** been silently modified. The manifest check requires reconstruction of this one omitted raw file.

The separate `sha256-word-distance/shift-reduction-v3/` directory contains six source artifacts and their own `manifest.json`. Run `python -B workstreams/CRYPTO3-20261012/sha256-word-distance/shift-reduction-v3/check.py` to replay its bounded checks. Its new support-reduction result remains **a candidate pending independent mathematical review**.

## Scientific and publication scope

No real SHA-256 13-word message-pair witness, SHA collision, preimage attack, proof of distance >=14, Lean certification, external human peer review or historical-priority finding is claimed. Prior stage-2 AI-independent checks have the limited scope described by their own frozen review receipts. The original main branch and all other agents' paths are unchanged. A coordinating agent can independently verify, sign when integrating, and decide on release or manuscript publication later.
