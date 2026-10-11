# Closed routes, corrections and operational issues

- Tu–Deng old bound/equality route: stopped at the source gate because current
  complete-proof/equality-classification claims were found. No enumeration.
- General 4-by-4 RD classification: deferred; high risk of merely expanding
  an existing rank algorithm into a large determinant list. Reopen only with
  a structural simplification absent from known Hadamard/Toeplitz results.
- Assumption that quotient MDS might be lost: incorrect for MDS input.
  The exact weight scaling proves descent. Main invertible proof did not
  require it, but v1's commentary needed correction. V2 and review addendum
  record the mathematical delta without overwriting v1.
- n=2 extension: false. GF(4) circulant [[1,alpha],[alpha,1]] is MDS and
  has no nontrivial RD pair. Exact exclusion and support-count proof saved.
- No failed random RD search, large unsuccessful enumeration, or numerical
  heuristic is passed off as a theorem. One bounded MDS10 construction found
  a certificate on its first trial.
- Native git push failed: `fatal: could not read Username for
  'https://github.com': No such device or address` (exit 128).
  This is a local credential-interface issue, not revoked user authorization.
  The authorized GitHub connector succeeded in publishing the reservation;
  transport status and exact SHAs are in HANDOFF/STATUS.
- Python `requests` and `bs4` were unavailable during source extraction.
  Standard-library urllib and HTMLParser were used instead. No shared
  dependency/version changes were made.
- Direct downloads of IACR PDFs and the Whirlwind institutional PDF returned
  HTTP 403. Some indexed publisher text was available via search service.
  Toeplitz full text was not obtained. These limits remain in the novelty gate.

Reopen the literature gate on availability of the missing full texts or a
specific equivalent theorem. Do not repeat the completed finite windows to
create a new-looking progress event.
