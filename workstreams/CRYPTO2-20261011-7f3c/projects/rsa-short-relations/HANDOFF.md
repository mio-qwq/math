# RSA recovery checkpoint

Owner CRYPTO2-20261011-7f3c, branch partner/dist-CRYPTO2-20261011-7f3c.
Claim publication: 3b651069e690bc237faa6c608de895f532160736, verified tree
0b19920d4cec1080ab328ee266c9da5fc9c93d51. This was published before the
first lattice diagnostic. Keep all work within this workstream.

Read STATUS.md, PROOF-v1.md, GENERAL-PROOF-v1.md, SOURCES.md, FAILURES.md and RUNS.md before
continuing. The user's priority is substantial cryptographic progress;
RSA/AES/SHA-256 are examples. The v1 constraints are not that major result.

Completed: a proof candidate for factor inheritance in powers of
(e,1+x(N-y)), valid also for composite e; a quantitative content defect;
an all-parameter obstruction to a specified dimension/determinant proof
strategy; conditional recovery from one quadratic relation, and from one
arbitrary-degree t=0 relation with a stated 3^m norm margin; exact
certificates and a separate integer checker.
These are not independently reviewed. Generic common-factor and ideal
methods have extensive prior art. Do not present novelty as established.

Next smallest unresolved step:

For positive y-shift support S(m,t), the leading row may have degree m+t
but only ideal order m. Determine an exact factor-by-factor allocation of
this deficit, then test whether the discriminant/weighted-height argument
can force a recoverable component in a range with an actual relation
existence theorem. The t=0 case is already covered by the general proof;
do not repeat it as new work. The useful goal remains a quantified range
delta>1/4 without assuming independent equations. Before extending, close
the full-text gaps for Aono et al.'s optimality results and Keegan Ryan's
2024/1577. A determinant-bound improvement alone is insufficient.

If the positive-y deficit/height combination yields no new constraint or
workable recovery mechanism after concrete analysis, suspend this line
and reopen the unused candidate
gate. Do not replace it with an unbounded lattice survey. Before any new
claim about SHA-256 or AES, reopen their latest full primary sources and
visible repository claims; their previous gate was not a proof that no
later work exists.

Recheck frozen evidence with `python check.py` from this project. With the
isolated pinned dependencies, `python reproduce.py` must regenerate all
five certificate files byte for byte, and extract the general controls'
keys from public inputs and the supplied relation. Replays are recovery checks, not new
research progress. The interrupted 256-bit run has no checkpoint and is
not a background job. No process is intended to continue after this turn.

Any change to frozen v1 files should form a new version and a new manifest.
Never rewrite Ascon-v3 or another member's files, and do not assume a push
has directly notified another researcher.
