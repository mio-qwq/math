# support12 valuation-16 generalization v9

This package extends the fixed `D=+/-2^16` selected-twin obstruction to
nine positive odd quotients `q<=31` and their negatives.  It also records
actual twin survivors for the other seven quotients, proving that the old
bit-30 mechanism is not uniform across the valuation layer.

The mathematical result is an author finite proof pending independent
review.  `PROOF.md` states the theorem and scope; `PRECOMMIT.md` fixes the
finite protocol; `CERTIFICATE.json` contains the exhaustive output; and
`check.py` reconstructs it using only the standard library.

The Z3 files are discovery-only.  Their UNSAT answers are explicitly not
premises.  No full support or message pair is decided here.

