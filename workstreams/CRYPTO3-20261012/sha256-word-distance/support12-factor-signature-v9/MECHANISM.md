# Mechanism and failure boundary

The useful negative conclusion is constructive.  Instead of treating the
accepted sigma0 and sigma1 valuation tables independently, the low-26 witness
uses one real 32-bit pair at each factor.  Hence a `J` factor keeps a single
input XOR mask for both small sigmas.  Exact residues modulo `2^26` retain
strictly more information than valuations and include all scalar carries
through bit 25.

Discovery used one fixed `QF_BV` query with Z3 4.15.3.  The first 60-second
attempt returned `unknown: timeout`; it is not evidence.  With the same seed
and a 180-second bound, the frozen source returned `sat`.  The model was then
copied into `CERTIFICATE.json` and is re-evaluated by `check.py`, which has no
solver dependency.  No retry or timeout result is used as a theorem.

An exploratory strengthening that required all shared additive differences
to agree in the full 32-bit ring, while keeping only low derivative bits,
quickly became UNSAT for the fixed numerical value `b=00010000`.  No proof
certificate was produced, so that result is deliberately **not** claimed.
The already accepted joint-image proof independently excludes that one fixed
signed residue.  The exact two-factor witness at `b=bfbf0000` records why this
does not extend to the entire valuation-16 layer.

The next high-value step is therefore not another valuation-only CSP.  It is
to add certified numerical cross-factor information above bit 25 for a
variable odd multiple of `2^16`, or combine the accepted base-lift residuals
with the full factor system.
