# Pre-author-v8 freeze declaration

This directory was derived and frozen before reading any byte from an author
directory named `support12-full-factor-v8` (or any later comparison supplied
by that author).

Inputs available to this blind reconstruction were:

- the frozen `supports-v2.json` support list and its published SHA-256;
- the public SHA-256 16-to-64 recurrence and sigma definitions;
- earlier frozen CRYPTO3 support-12 artifacts, including the already public
  list of 25 nonzero rows.  The checker nevertheless reconstructs all 48
  rows mechanically from the recurrence and support rather than importing
  any earlier checker or reduced matrix.

No author-v8 code, certificate, proof text, factor graph, or claimed scalar
parameterization was opened or imported.  No external solver and no author
module is used by the independent checker.

Frozen claim: the 14-coordinate table and the projected 10-scalar,
13-factor theorem in `INDEPENDENT_PROOF.md` are necessary and sufficient for
the complete independent-active-pair feasibility problem, but say nothing
about common base-message completion.

