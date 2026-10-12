# GP2-20261012 current checkpoint

Updated 2026-10-13. Only this workstream and branch
`partner/dist-GP2-20261012` are owned by this task.

## Current mathematical increment

The new all-parameter reciprocal trace argument establishes

    0.224808115216882691... <= lambda_4
        <= (1-1/[27(1+(3+2sqrt(2))^(1/3))^3])/4
        = 0.249578038101911868... .

A convenient entirely rational upper endpoint is 73963/296352, strictly
below the inherited 182/729. See `stage3/RECIPROCAL_TRACE_BOUND.md`, its
exact checker, certificate, actual logs and independent `trace_review/`.
The core judgment and written derivation were performed by the primary
agent, then independently reviewed. No exact lambda_4, complete Lean,
human peer review or historical-priority certification is asserted.

The source-stage README and the 98 recovered files are frozen historical
records with their original hashes. Use this checkpoint and stage3 for
the newer bound; do not silently alter the old signed manifests.

## Recovery and completed acceptance

Remote delivery was accepted at
`471537ae027ada2647f30e94ff6f71d3466f8828`. All 98 original science files
and the complete ZIP match the attachment byte-for-byte and by Git blob/SHA256.
Both source commit signatures pass native verification. Their exact signed
history remains in the public bundle/ZIP; a native GitHub history import
was unavailable because terminal push has no credential and the exposed
commit-creation interface cannot reproduce signed raw objects. New commits
use the already-authorized GitHub interface and are unsigned.

Independent six-letter replay confirms 310 viable orbits, 189 unique
candidates, 7,919 edges and matching/cover size exactly 64. The fixed
41/216 bound remains fixed-label, uniformly weighted and is not lambda_4.
The new independent checker actually rejects 12 damaged certificates.

The inherited `stage2/verify_ten.py` has no executable entry point: its
direct exit-zero log did not perform validation. The new explicit wrapper
and independent checker now actually validate the ten-state reduction,
including 108 local embeddings and 136 domination entries. The missing
entry point did not produce a mathematical counterexample.

## Resume the next meaningful proof step

1. Fetch this branch, inspect actual HEAD and preserve all uncommitted work.
2. Reuse the accepted stage3 proof and certificates. Do not redo the fixed
   six-letter enumeration or the binary-code enumeration solely on restart.
3. Derive an exact decomposition for the empty-orbit event that retains
   mixed reciprocal classes, or derive a uniform fractional forced-orbit
   cover using the 10/6/3 triple/pair/letter hierarchy. The present one-class
   trace bound misses most such configurations; enlarging finite searches
   does not fix this structural omission.
4. Couple the mechanism to canonical strict-code levels or prefix/suffix
   interfaces if the unconstrained color relation is too weak. The claimed
   E>=1/9 for arbitrary relations is already disproved and must not recur.
5. Save every mature increment with a self-contained proof, exact verification,
   negative controls, actual logs, hashes and source limits; publish only on
   this branch and check the remote tree. Maintain main and all other owners
   unchanged. No DOI, submission or main merge is authorized.

The first scalar-coefficient follow-up has now been closed negatively. The
orientation conditions `M_xx=0` and `M_xy M_yx=0` do **not** imply
`2(T+L)>=tr((M+M^t)^4)/4`: the exact 24-vertex certificate in
`stage3/ORIENTED_TRACE_COEFFICIENT_OBSTACLE.md` has ratio
`6385/26889<1/4`. Both ordinary and optimized exact checks pass, including
two tamper controls. This does not change the current lambda bound. Do not
restart from small-order evidence for `1/4`; seek a rigorously smaller
coefficient or, preferably, exploit mixed classes/canonical interfaces.

The weaker candidate `2X<=T+L` is reduced exactly in
`stage3/ORIENTED_FIFTH_REDUCTION.md`. It is equivalent to nonnegativity of
`[tr(S^4)+tr(RSRS)]/4` and would conditionally yield reciprocal coefficient
`1/5`. Exhaustion of all 59,809 zero-one orientations through order five
passes, but a five-vertex witness makes one pair-interface summand negative.
Thus the candidate remains unproved, the finite check is not a new bound, and
the next attempt must use a global square/flag certificate rather than
pointwise positivity or merely larger enumeration.

Lean 4.34.1 is the intended pinned toolchain, but the recovered local launcher
actually exits with `failed to locate application`; no successful compilation
is claimed. Resolve this environment issue before any formalization claim.

The latest publication SHA must always be read from the actual remote ref;
this file cannot include the SHA of the commit containing itself.
