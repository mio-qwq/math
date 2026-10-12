# GP2 complete stage-one and stage-two delivery

The file GP2-20261013-complete.zip is a complete handoff with all 98 GP2 workstream files, verifier scripts, certificates, SHA256 manifest, and a lossless Git bundle holding the original signed commits.

SHA256 of ZIP: bbc2b85f1e07707fe2e48fa012f706aefabcc87ffd37772c351715565a8866e8
Original stage one commit: b45b04eeab0fc521b789d6d47b4d8b94119e8c90
Original stage two commit: fec858c5f1edc36ad6335656a230f324959eee17

To recover the original signed Git history: unzip the ZIP and then run
    git clone -b partner/dist-GP2-20261012 GP2-20261013-complete.bundle gp2-signed
No original ROOT, main, or other agent history was rewritten. The delivery commit created through GitHub's API has a different SHA from the signed commits inside the bundle.

The mathematical proofs and exact certificates are research outputs subject to their recorded scope limitations; no all-parameter Lean proof, exact density or human peer review is implied.
