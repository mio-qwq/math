# Exact forced-orbit obstruction as a weighted vertex cover

GP2-20261012, second-stage mathematical theorem. **Scope:** a *fixed* ordered-pair level array; this does **not** give a new universal numerical value for the Kautz length-four general-position density. The combinatorial proof is elementary; the fixed six-letter example has two fully explicit certificates rechecked without a solver. The reduction to vertex cover and fractional matching is a standard idea and is **not claimed as historically new**; the precise forced-orbit application and frozen finite certificate are the mathematical work reported here.

## 1. Forced candidates and the hypergraph

Let `A` be a finite alphabet with probability weights `mu(a)>=0` summing to one. Let `ell:A^2->{0,1,2}` be **arbitrary**, and write

    V_ell={abcd in A^4 : ell(ab)<ell(cd)}.

A rotation orbit is the set of distinct cyclic rotations of a four-letter word. It is **viable** when it meets `V_ell`. Each viable orbit of positive product weight is necessarily primitive: opposite rotations compare the same two ordered pairs in opposite directions, so a shorter-period orbit contains no eligible word. There are at most two candidates per viable orbit.

Define `F_ell` as the set of **forced words**: the unique candidate in every viable orbit having exactly one candidate. Each `f in F_ell` belongs to a different orbit. Set

    wt(f)=mu(f_0)mu(f_1)mu(f_2)mu(f_3),
    T_ell=sum_(viable orbits O) wt(any representative O).

This is `(1-E_ell)/4` from `ROTATION_COMPLETION.md`, but this theorem needs only its orbit definition.

A strict code `C` selects at most two occurrences among the five four-letter windows in **every** eight-letter word. Repetitions are counted by occurrence, and a strict code selects at most one word per cyclic orbit.

Build a hypergraph `H_ell` on the **vertices** `F_ell`. For every eight-letter word `x_0...x_7` and every `0<=i<j<k<=4` for which all three length-four windows at starts `i,j,k` lie in `F_ell`, insert the nonempty **set** of those three windows as a hyperedge. Its cardinality can be one, two, or three, since the same forced word may appear at multiple positions. Set semantics are essential: selected occurrences are still three, even when the word values are not all distinct.

For nonnegative weights, let `tau_w(H_ell)` be the minimum of `sum_(f in D) wt(f)` over subsets `D subset F_ell` meeting every hyperedge. For the empty hypergraph this minimum is zero.

### Theorem 1 (all finite weighted alphabets; fixed level array)

Every strict code `C subset V_ell` satisfies

    mu^4(C) <= T_ell - tau_w(H_ell).                    (1)

**Proof.** Every selected word belongs to one viable orbit, and strictness permits only one selected word per orbit. A viable orbit with its unique candidate `f in F_ell` contributes nothing if `f` is absent. Hence

    T_ell - mu^4(C) >= sum_(f in F_ell \ C) wt(f).

The missing forced words `D=F_ell \ C` meet every hyperedge: otherwise all three occurrences witnessing that edge would be selected in the same eight-letter word, contradicting strictness. Thus `D` is a vertex cover and its weight is at least `tau_w(H_ell)`. This proves (1), with no independence assumption, and with arbitrary nonnegative (including zero) letter weights. `C` need not be maximal. QED.

### Corollary 2 (independently checkable lower certificate)

For rational edge coefficients `y_e>=0` satisfying

    sum_(edges e containing f) y_e <= wt(f)  for every f in F_ell,

one has

    mu^4(C) <= T_ell - sum_e y_e.                        (2)

Indeed, summing the constraints over a vertex cover `D` shows `sum_e y_e<=sum_(f in D)wt(f)`. Thus a *fractional matching* provides a rational lower certificate for the vertex-cover cost. In particular, for uniform weights `mu=1/n` and `k` vertex-disjoint forbidden hyperedges, every strict code loses at least `k/n^4` density from viable orbits.

This dominates the single-gap forced-overlap moment estimate in `FORCED_OVERLAP_BOUND.md`, since every violation counted there supplies one hyperedge; applying a union bound gives only a particular feasible fractional matching. The full vertex-cover optimization may be much stronger.

## 2. A fixed six-letter exact obstruction

Take `A={0,...,5}` with uniform weights and the prescribed ordered-pair levels (row `a`, column `b`):

    1 2 0 1 2 0
    0 1 2 1 1 0
    2 0 1 2 2 1
    1 2 1 1 0 0
    1 0 2 1 0 0
    1 0 2 2 2 2

This is the **same fixed array** as in `ROTATION_COMPLETION.md` and `FORCED_OVERLAP_BOUND.md`. Exact orbit reconstruction gives 310 viable primitive cyclic orbits, 189 forced words, and

    T_ell=310/6^4=155/648.

The forced-word hypergraph has **7,919 distinct hyperedges**, of which 41 have two distinct vertices and 7,878 have three. There are no rank-one edges in this instance.

The bundled `forced_cover_certificate.json` contains both:

* **64 pairwise vertex-disjoint hyperedges.** Each comes with a literal eight-letter word and the three distinct starting positions. Checking the selected windows reconstructs that hyperedge. The 64 edges cover 187 different forced-word vertices (five rank-two and 59 rank-three edges in the frozen matching).
* **An explicit 64-word vertex cover.** Delete those words from `F_ell`. The remaining forced code is strict: a direct five-step dynamic program on the *full* triple-shift graph finds at most two selected occurrences on every eight-letter word. In particular, every hyperedge is hit. The verifier also enumerates all 7,919 hyperedges separately as a cross-check.

The first certificate proves `tau_w>=64/1296`. The second proves `tau_w<=64/1296`, so **the forced hypergraph cover optimum is exact**, independent of a solver optimality status:

    tau_w(H_ell)=64/1296=4/81.

By Theorem 1, every strict code compatible with this exact `ell` satisfies

    mu^4(C) <= (310-64)/1296 = 41/216 = 0.1898148148... . (3)

This improves the rotation-only bound `155/648 ~= 0.2391975` for this *one* label matrix by a rigorous absolute amount `4/81 ~= 0.0493827`. It is **not** a bound of `41/216` on the unrestricted `lambda_4`. A strict code from a different level array need not obey (3); the inherited **uniform** interval stays

    beta <= lambda_4 <= 182/729.

The two matching/cover witnesses are independent of SciPy or a floating-point MILP. Their provenance is mathematical: the generator may use SciPy to discover them, but the standalone verifier checks the entire claim from the definitions using the Python standard library.

## 3. Verification, deliberate damage, reproducibility

From the project checkout, with Python 3.10+:

    python workstreams/GP2-20261012/stage2/verify_forced_cover.py

The checker independently rebuilds all 310 viable orbits and 189 unique candidates, checks all 64 concrete three-occurrence eight-letter witnesses and their pairwise disjoint forced-word supports, checks the 64-word deletion set via the original full-shift five-step dynamic program, and directly enumerates all hyperedges and cover incidences. It additionally rejects altered level ranges, a missing cover member, out-of-alphabet witness letters, and incorrect alphabet size. There is no external library dependency for checking.

`build_forced_cover.py` can rediscover a certificate with `scipy.optimize.milp` and is a **generator, not the trusted validator**. It is not necessary for a reader who only wants to verify (3). The SHA256 of the frozen JSON is recorded in the actual replay output and in the stage-two manifest.

This finite theorem uses strict codes over a *full* alphabet, not actual finite `Ka(m,4)` vertices. The stage-one repair theorem connects these to the limiting Kautz problem with `O(m^3)` error; it does not permit replacing the universal upper constant by this fixed-array estimate. No complete Lean proof, solver-certified universal extremum, or historical novelty assessment is claimed.
