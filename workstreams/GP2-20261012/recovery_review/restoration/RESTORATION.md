# GP2 recovery and remote-delivery acceptance, 2026-10-13

The attached `GP2-20261013-complete(1).zip` was extracted directly with the
terminal. Its SHA-256 is
`bbc2b85f1e07707fe2e48fa012f706aefabcc87ffd37772c351715565a8866e8`.
All 98 individually included GP2 files match the outer manifest. The enclosed
complete-history Git bundle matches SHA-256
`80e926424d82ab136dac6850dddf6e8b4e628cdd29a86574a508d75f88e83e87`
and passes `git bundle verify`.

## Actual remote acceptance

The independently fetched GitHub branch head was
`2e920b20a297fc471c833858cc858f84c4d8f24e`. All 98 proof, checker,
certificate, source and log files are already present, byte-identical to the
attachment. Every remote Git blob SHA was independently recomputed from the
exact file bytes; every SHA-256 also matches. No missing or inconsistent
scientific file was found. The branch contains 117 GP2 files: the 98 scientific
files and 19 older transport/delivery files. Those additional files were
preserved. The remote complete ZIP is byte-identical to the attachment.
`REMOTE_ACCEPTANCE.json` records the per-file results.

The frozen stage-one and stage-two manifests pass (75 and 21 listed files,
respectively; the two manifest files themselves make the outer total 98).
The repository outside `workstreams/GP2-20261012/` matches frozen main
`61488e05c9fe41984f483853f99e79f5715dc893`.

## Signature preservation, precise scope

The exact source commits are
`b45b04eeab0fc521b789d6d47b4d8b94119e8c90` (Ed25519 SSHSIG) and
`fec858c5f1edc36ad6335656a230f324959eee17` (Ed25519 OpenPGP).
Both signatures passed native verification using only the packaged public
keys. The stage-one Python cryptographic verifier also passed. A temporary
public-key import reported that gpg-agent could not start, but imported the
public key; the subsequent `git verify-commit` exited zero with a good
signature. The exact signed commit object text and actual native verifier
logs are preserved beside this report. Public-key validity does not establish
an independently authenticated human identity or external mathematical review.

The source commits are preserved byte-for-byte in the publicly available ZIP's
Git bundle and in the local `gp2-recovery-signed-history` branch. **They have
not been inserted into the native GitHub branch history.** A native terminal
push failed because no HTTPS push credential is configured. The available
GitHub commit-creation interface does not expose the original signature,
author/date or raw-object fields needed to reproduce these identical signed
Git objects. New acceptance/research commits through that interface are
ordinary unsigned commits. No claim that the old signatures were retained
on those new commits is made. No private signing material was accessed,
packaged or published.

## Mathematics remains bounded by its evidence

Recovery verifies delivery, not the truth of every all-parameter proof.
Independent mathematical replay and review are recorded separately. The
inherited trustworthy candidate interval is
`0.224808115216882691... <= lambda_4 <= 182/729`.
The fixed six-letter `41/216` result does not replace the universal upper
endpoint. Complete Ka4, exact lambda_4, all-parameter Lean, human peer review
and historical priority remain unestablished.
