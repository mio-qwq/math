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

The weaker candidate `2X<=T+L` is now **refuted**, not an open proof target.
`stage3/ORIENTED_TRACE_TRANSFER.md` gives a 46-vertex binary orientation
with `T+L-2X=-759`, checked by matrix products and all 4,477,456 ordered
quadruples. A separate explicit 1057-vertex binary Cayley orientation has
`2(T+L)/R4=1723885/8660823<1/5`, so the weaker proposed scalar coefficient
`1/5` is also false. Group convolution and literal outgoing-neighbor/rooted
walk counts agree exactly; six damaged certificates are rejected.

The note also proves a uniform transfer theorem: every homogeneous linear
inequality in `(T,L,X,Y)` true on all finite binary orientations must be
true on all finite nonnegative matrices, including diagonal entries and
digons. A seven-dimensional circulant matrix therefore puts the ceiling
`2548/12899<1/5` on any universal scalar coefficient. This ceiling is not
claimed sharp or achievable. It does not change the accepted lambda bound.

The earlier order-five local minimality remains true only for zero-one
matrices. Weighted matrices and product-weighted indicator kernels already
have an order-four negative local bracket. The overbroad inference that
every useful certificate must see at least five vertices is withdrawn.
Do not seek a flag/SOS proof of the refuted candidate. Resume mixed
reciprocal classes with the actual 10/6/3 compatibility hierarchy; orientation
support alone cannot improve the cone of these four quartic scalars.

The first positive interface step is now proved in
`stage3/BRIDGE_DELETION_FORMULA.md`. For every finite strict code and every
probability distribution, its selected-word adjacency components are
vertex-disjoint complete bipartite graphs indexed by active triple bridges.
The greatest independent subset density is exactly
`p-d(C)`, where `d(C)=sum_s mu^3(s) min{i(s),o(s)}`. The exact adjacency
probability `a(C)` and bridge mass `b(C)` satisfy `d(C)^2<=b(C)a(C)`, with
sharp coefficient one. The 10/6/3 model bounds incoming free-letter mass
by the r2 mass and outgoing mass by the r0 mass. This quantifies the
adjacency branch rather than discarding it. Nine exact input cases,
component-subset optima, raw Kautz BFS and six damaged inputs pass under
ordinary Python and `python -O`. No new lambda bound, independent AI
review or Lean claim is made. Next couple mixed-class rotation loss with
these exact bridge costs, covering both independent and positive-bridge
regimes without assuming extremizers are independent.

Lean 4.34.1 is the intended pinned toolchain, but the recovered local launcher
actually exits with `failed to locate application`; no successful compilation
is claimed. Resolve this environment issue before any formalization claim.

## New endpoint loss and finite-certificate bridge

The follow-up `stage3/ENDPOINT_ROTATION_LOSS.md` proves an intrinsic
support constraint. With first/last supports P,Q and masses l,r,h,n of
P\Q, Q\P, P intersection Q, and the complement, the exact probability F
of no cyclic Q->P edge satisfies

    1-4p >= F+delta h^4,     F>=l^4+r^4.

It includes a complete nonnegative polynomial for F and the bridge bound
`a(C)<=lr mu(P)mu(Q)<=1/16`, giving an explicit adjacency-dependent
rotation penalty. This does not improve the uniform lambda_4 endpoint;
the independent regime remains a core obstacle.

`stage3/INJECTIVE_SAMPLING_BRIDGE.md` proves an exact all-parameter
certificate transfer. If M_n is the maximum strict code on n indices
supported on four-distinct-index words, then for every n>=4

    M_n/n^4 <= lambda_4 <= rho_n=M_n/(n)_4,
    rho_n decreases to lambda_4,
    rho_n-lambda_4 <= [1-(n)_4/n^4]/4.

More generally any pointwise finite inequality in injective motif counts
transfers to every weighted alphabet, including joint adjacency and empty
rotation motifs. Actual letters may repeat; strictness on the finite
index alphabet still tests all eight-index words. Fixed-label optima do
not qualify as M_n certificates.

The exact witness gives M_4=6 and M_5=30, and the five-index optimum can
have four selected adjacent five-index words. Thus neither a pure
five-index density certificate nor the proposed five-index linear
adjacency penalty beats 1/4. This is a limitation of that certificate
form, not a disproof of a global p+c*a inequality. M_6 is unresolved:
the two bounded six-index discovery attempts timed out and certify no
impossibility. Do not repeat them with a larger timeout as the next step.

Primary exact checks pass in ordinary and optimized Python: all 390625
five-letter-alphabet eight-window inputs, the separate triple-state DP,
the 256-term endpoint type polynomial and 255 rational weight cases,
160 sampled alphabet maps, original Ka(5,4) BFS on 320 vertices/1280 arcs
and 24360 ordered selected triples, and eight damaged-input controls.
Independent AI review and a separate checker are in
`stage3/sampling_review/`. These are not Lean or human review. In this
fresh checkout neither lean nor lake is on PATH; no new compilation ran.

Next: derive a structural constraint on the six-index compatibility
problem or a finite motif inequality with canonical pair/triple labels.
A proved M_6<=89 would already imply lambda_4<=89/360, but it is only a
target and must not be reported as obtained. The sampling theorem supplies
the missing finite-to-all-alphabet implication once a genuine certificate
is available. Preserve the current trusted interval stated at the top.

The latest publication SHA must always be read from the actual remote ref;
this file cannot include the SHA of the commit containing itself.
