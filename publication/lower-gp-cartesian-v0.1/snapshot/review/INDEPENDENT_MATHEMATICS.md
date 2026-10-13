# Independent mathematical audit of the lower-GP Cartesian-product result

Date: 2026-10-12. Baseline actually inspected: public repository `research`, HEAD `61488e05c9fe41984f483853f99e79f5715dc893`. Its working tree was clean at the start and after the small controls. This reviewer did not participate in discovery, proof writing, or integration. Only this local review directory was written. No partner branch, mathematical source, publication file, or repository status record was changed.

## Verdict and the exact boundary

**No mathematical counterexample or blocking proof gap was found in the specified frozen sources.** The fixed connected counterexample and the role-based family for every integer r >= 6 pass independent written review. The all-order min-5 reduction, exact ray-generation algorithm, zero-pattern closure, and finite profile search are mathematically sound on source inspection. The optimal replacement follows, with the computational dependency stated explicitly.

This is an independent AI mathematical/source audit, not human peer review and not a certification of historical originality. This reviewer did **not** compile Lean, execute the full MET5 certificate, or repeat a large graph enumeration. ROOT must bind its actual fresh Lean and full certificate execution to the same source bytes. The bounded executions described below are real new executions by this reviewer, and their narrower scope is explicit.

The new manuscript has not yet been reviewed. Acceptance here concerns the listed mathematical sources, not wording or claims in a future TeX file.

## 1. Independent check against the primary original question

Primary sources read directly:

- [arXiv 2404.19451v1](https://arxiv.org/html/2404.19451v1), Introduction and Section 2, particularly Conjecture 2.10.
- [Final journal paper](https://oro.open.ac.uk/98050/9/98050final.pdf), printed pp. 110-113 for definitions and product conventions, p. 117 for Conjecture 3. The journal header gives Communications in Combinatorics and Optimization 10(1) (2025), 110-125, DOI 10.22049/cco.2024.29171.1879.

Both versions ask for

    gp^-(G □ H) >= min{gp^-(G), gp^-(H)}.

The source defines GP by shortest paths containing no three selected vertices, and lower GP by the smallest inclusion-maximal GP set. Its general graph convention is simple and undirected; the conjecture itself states arbitrary graphs and adds no explicit connectivity or nontriviality qualifier. The order-at-least-two condition occurs in the separate layer/terminal-set lemma. The present factors are finite, connected, nontrivial, simple, undirected and of diameter two, so the refutation also satisfies the stronger usual assumptions. One need not settle the source's conventions for disconnected distances to refute its claim.

The product is the Cartesian product, changing exactly one coordinate along a factor edge. Distances add for connected factors. The result concerns lower GP, not the upper GP parameter or the lower terminal parameter. The original Proposition 1 concerns a gap involving tp^- and does not already prove the present lower-GP gap.

The final PDF was available through the web tool's text extraction. The web screenshot operation was unavailable and a direct local download received a Cloudflare challenge. No visual PDF rendering or raw-byte SHA256 for that remote PDF is claimed. The mathematical formula, page label, definitions and relevant page text were independently obtained; no computer-use was used.

## 2. Fixed construction and the family: independent derivation

For G_r, take two K_r blocks meeting only in c, with outer cliques A and B of size r-1. A GP set containing c cannot contain an A vertex and a B vertex, because their distance is 2 through c. It lies in a K_r block, and maximality then forces the entire block. A GP set without c is contained in A union B, which is GP: all three-point distance patterns there are (1,1,1) or (1,2,2), with no equality. Maximality without c forces A union B. For r >= 6 these three maximal sets have sizes r, r, 2r-2, giving gp^-(G_r)=r.

For H_r, the five landmarks induce K_5 with u_0u_1 and v_0v_1 removed. Each Q_ij is an r-clique whose members have identical closed neighborhoods. For adjacent true twins x,y, distances from x and y to every third vertex agree. Adding y to a GP set containing x preserves all triples without x by distance substitution; a triple containing both twins has lengths (1,d,d), d >= 1, and is also GP. Hence a maximal GP set meeting Q_ij contains all of Q_ij.

The inclusion-maximal GP subsets of the landmark set are exactly the two pairs {u_0,u_1}, {v_0,v_1}, and the four triangles {z,u_i,v_j}. A nonadjacent pair cannot accept a third landmark, since every remaining landmark is adjacent to both pair members. A landmark set containing z must be a clique. Smaller cliques can extend within the landmarks. Each triangle extends to a member of its Q_ij; each nonadjacent pair extends to a member of Q_00. Since GP is hereditary, every smaller landmark GP set also has an outside extension. Thus every globally maximal GP set meets a Q clique and gp^-(H_r) >= r.

For the five selected product points

    (a,u_0), (a,u_1), (c,z), (b,v_0), (b,v_1),

their off-diagonal distances are 2 or 3. No triple satisfies a triangle equality. The maximality cases in PROOF.md are exhaustive and numerically correct:

- At first coordinate c and second coordinate not z, some endpoint landmark has H-distance 2 from the new vertex; the selected center is between the new point and the corresponding selected endpoint, with lengths 1+2=3.
- At first coordinate in A and h=z, the center blocks, with lengths 1+2=3.
- At first coordinate in A and h outside {z,u_0,u_1}, one v_j has H-distance 2 from h; the center blocks, with lengths 2+2=4.
- At first coordinate in A and h=u_i, the new point must have first coordinate different from a, and the two selected u points block it with lengths 1+2=3.
- The B cases are the same numerical statements with the u and v roles exchanged; H_r is invariant under this exchange, including Q_ij ↔ Q_ji.

The roles and distances do not depend on clone multiplicity. All classes exist for every r >= 6. Therefore gp^-(G_r □ H_r) <= 5, the smaller factor lower GP is exactly r, and the conjectured bound fails with deficit at least r-5. The ratio is at most 5/r. These conclusions are independent of the min-5 theorem and of any finite extrapolation. The r=6 graph has factor orders 11 and 29, as specified.

Neither this argument nor the fixed Lean file computes gp^-(H_r) exactly. That value is unnecessary.

## 3. Pseudometrics, repeated coordinates and product-extension semantics

For a selected product set of k distinct points, its k coordinate labels need not be distinct. Factor distance tables are genuine pseudometrics. In a graph of a connected factor, zero coordinate distance identifies the same actual vertex; the quotient is an ordinary metric. For every ordered middle role, the product triangle slack is the sum of two nonnegative factor slacks. It is zero exactly when both factor slacks vanish with the **same** middle label.

The verifier's separate three equality bits per selected pair are essential and correct. With repeated coordinate landmarks more than one bit can hold. Replacing those bits by one exclusive collinearity case would be wrong; the current code does not do so. The new product point equals a selected point exactly when its two zero masks have a common selected index. Thus the joint test

    equality masks disjoint AND zero masks disjoint

is exactly the GP extension test, once the selected set is itself GP and consists of distinct product points. The model-pair filter rejects common selected distance zeros and common selected triangle-slack zeros in the same aligned indices. It retains every legal product pattern.

In verify_arbitrary_four.py, `base_key` (line 31), `extension_profile` (32-35), distinct projection representatives (47-49), known-known tests (61), and the product GP filter (84) implement these statements. Deduplicating the projections for factor demands is correct; deduplicating the product labels before alignment would not be correct and is not done.

The group representative D may have different numerical distances from an actual factor's table. All operations used on known landmarks depend only on the shared key: zero classes and tight triangles. Equalities involving coincident labels reduce to distance-zero information, so the known profiles and maximal-landmark GP subsets are invariant within a group. The union of possible outside profiles can admit mutually unrealizable numerical profiles. This is a deliberate relaxation and is harmless for a **nonexistence** proof: every actual profile is included, and simultaneous realizability is never used to delete a possible actual system.

## 4. Necessity of every maximal-landmark GP demand

Let L be the distinct actual projected landmark vertices in one factor, and let T be any inclusion-maximal GP subset of L. Then |T| <= |L| <= k < gp^-(G). Consequently T is not globally maximal. For a hereditary finite property, failure of inclusion-maximality gives a one-vertex extension. No vertex of L outside T can extend it, by maximality within L. Hence some vertex outside all of L extends T.

For this actual outside vertex, no equality bit attached to a pair of T is set. That is exactly the demand E_T. Every maximal-landmark GP subset gives a necessary demand, including singleton subsets and subsets smaller than k. The empty subset is legitimately omitted: L is nonempty because k >= 1, every singleton is GP, and the empty subset cannot be maximal in L.

The loop at lines 50-54 enumerates every nonempty subset of the distinct representatives, tests actual landmark GP and inclusion-maximality, and constructs the correct allowed-profile mask. Repeated labels outside the representative pair do not create an additional condition for extension of the actual set T. Multiplicity of actual vertices with one profile is irrelevant because each demand only requires existence.

No projection itself is assumed GP. This is important: an arbitrary product GP set may have a non-GP projection. The proof and code correctly use maximal GP subsets **within** that projection rather than demanding extension of the whole projection.

## 5. MET5 double-description completeness and closure

There are ten nonnegative coordinate forms and thirty triangle-slack forms on five labels. The constructor at verify_metric_rays.py lines 9-14 generates exactly the three triangle inequalities for each of the ten unordered triples. Diagonal zeros and symmetry are built into the distance-vector representation.

Every intermediate cone is inside the nonnegative orthant and is pointed. It is full-dimensional: the all-one coordinate vector is strictly positive on all coordinate inequalities and on every added triangle inequality. Its slice sum d_ij=1 is a nonempty compact polytope. A ray is equivalent to a vertex of that slice.

For two distinct old extreme rays, the intersection of their common active inequalities is their minimal common face. This follows because their sum is positive on every inequality not common to both. The face has exactly those old extreme rays whose active masks contain the common mask. If it has no third ray, it is generated by the two distinct rays and has dimension two; conversely a two-dimensional pointed cone has exactly two extreme rays. Thus the no-third-old-ray test at line 27 is the exact adjacency test. Redundant defining inequalities do not invalidate the argument.

Clipping the slice by one more halfspace keeps feasible old vertices and introduces vertices only at crossings of old edges. For a positive ray r and a negative ray s, the inserted vector h(r)s-h(s)r is their positive crossing ray. Primitive integer normalization preserves its ray. Old zero and positive rays stay extreme in the smaller cone. This gives an inductive completeness proof from the orthant; it does not rely on knowing that MET5 happens to have 25 rays.

For the complete final ray set, every point is a nonnegative ray combination. Every coordinate or triangle-slack form is nonnegative on all rays, so its value on a combination is zero exactly when it vanishes on every positive-support ray. Therefore all zero patterns are intersections of ray zero masks. The origin is the empty-support case, represented by the full mask. A sum with coefficient one on each selected ray has the same zero mask as any strictly positive coefficients on that support.

The queue at verify_arbitrary_four.py lines 21-28 begins at the origin, intersects with **every** ray mask until exhaustion, and binds every newly reached pattern to an exact integer representative. Discarding paths that reach an already known mask loses no future pattern because intersection depends only on the mask. This covers unbounded real pseudometric distances, not just some bounded integer sample.

For k < 4, every (k+1)-label table can be padded to five labels by duplicating a landmark. Label 4 remains the new point. All actual outside points have positive distances to the distinct projected landmarks and survive the filter at line 40. Under lower GP > k such outside points necessarily exist; more abstractly any finite pseudometric table can be extended by a point at a sufficiently large common positive distance.

The [Avis exposition](https://cgm.cs.mcgill.ca/~avis/epc/epc.html), Section 3, is useful background for metric-cone computation. The self-contained common-face/clipping argument above should be kept in the manuscript; the background citation is not an independent proof of this particular code.

## 6. Search pruning and exhaustiveness

Known landmark profiles are unavoidable actual factor vertices. A compatible known-known pair already extends the product set and therefore rules out maximality. An outside profile compatible with a known vertex in the other factor can never occur in a maximal product configuration and may be deleted. Outside zero masks are empty, so the filtering at lines 62-63 needs only the equality intersection.

After that filtering, a search state stores second-factor demands not yet hit and first-factor profiles still available. Choosing q in an unhit second demand satisfies all demands containing q, and deletes exactly the first profiles compatible with q. First-side demands becoming empty make completion impossible. If all second demands have been hit while every first demand remains nonempty, taking all remaining first profiles supplies a relaxed feasible first set. There are no same-factor coexistence constraints in the relaxation.

For completeness, follow any hypothetical actual second profile set Y: at a chosen unhit demand Y contains some branch profile q. Actual first profiles cannot be deleted by that branch, since a deletion would give a compatible actual product extension and contradict maximality. Continuing follows at least one branch until all demands are hit. Hence a real counterexample could not be pruned away. Each branch meets a previously unhit demand, so it terminates. Two paths with the same `(unhit, available)` state have identical future feasibility; merging those states is sound.

The solver's asymmetric choice to branch on the second factor does not make the underlying feasibility problem asymmetric. Iterating unordered model pairs is justified by exchanging the factors. All labels within a model remain aligned; no unsupported label-permutation reduction is used.

The runner invokes all four selected sizes 1,2,3,4. It treats any feasible relaxed system as a failing assertion, rather than silently skipping it. `metric_faces.json` and `metric_rays_verified.json` are comparison artifacts, not inputs to this replay. The full fresh replay is ROOT's execution task, not something performed here.

## 7. Disconnected graphs and sharpness for all parameters

A GP set is maximal in a finite disjoint union exactly when its restriction to each component is maximal. Shortest paths never meet different components. Thus lower GP is the sum of the component lower GP values. Components of a Cartesian product are precisely the products of factor components.

For nonnegative t,y_j, sum_j min(t,y_j) >= min(t,sum_j y_j): if the total is below t, every term is unsaturated and equality holds; otherwise either one term saturates t or the sum of unsaturated terms already reaches t. Write X=sum_i x_i and Y=sum_j y_j. Applying this twice gives

    sum_ij min(5,x_i,y_j)
      >= sum_i min(5,x_i,Y)
      >= min(5,X,Y).

This confirms the disconnected step without using infinity-valued distances in the cone. Nonempty graphs are essential to the stated positive-parameter sharpness convention; empty graphs are outside the claimed theorem.

Combining the universal min-5 lower bound with the family gives product lower GP **exactly 5** for every r >= 6. This equality depends on the computational theorem; the elementary refutation does not.

For r=2,3,4,5, K_r has lower GP r. In K_r □ K_r, a GP set smaller than r misses some row and some column; their intersection has distance 2 to every selected point and extends the set. A full row is GP, and every outside point is blocked by its same-column row vertex and a second row vertex. Thus product lower GP is r. For r=1 the single-vertex product is immediate. These examples realize min(r,5) at every positive integer r.

The complete-graph product formula is already Theorem 2.6 of the preprint/Theorem 2 of the final paper; its use here should be credited. The sharp statement is the optimal universal lower bound depending only on r=min{factor lower GP values}, not an exact formula for the lower GP of every product.

## 8. Lean semantic audit and historical evidence

The fixed source's OriginalGP uses arbitrary actual simple shortest paths, with three strictly increasing support positions; endpoints need not be selected. MetricGP checks three pairwise distinct vertices in every ordered middle role. The theorem `metricGP_iff_original` assumes connectedness, proves both directions using actual shortest paths and their subpaths, and avoids using natural-valued unreachable distances as a metric.

`maximalGP_iff_inclusion` proves that one-point maximality equals full inclusion-maximality using heredity. `lowerGP` is `Nat.find` over actual maximal OriginalGP cardinalities, with existence and minimum lemmas. It is not a surrogate statistic or an assumed optimum.

The actual G and H adjacencies agree with the displayed construction, including all four clone classes. Common-neighbor certificates prove their 0/1/2 distance tables from graph edist; the product is Mathlib's actual `G □ H`, with the actual box-product distance theorem. The factor lower bounds quantify over arbitrary finite selected subsets. G uses three structurally exhaustive large supersets; H uses true-twin saturation and the 32 core subsets. The five selected product points and every outside blocker are checked by ordinary `decide`, with a theorem supplying actual shortest simple blocking paths.

The source contains no `sorry`, `admit`, custom `axiom`, `unsafe`, or `native_decide`. Its 15 `#print axioms` commands correspond to the existing audit records, which report only propext, Classical.choice and Quot.sound and source SHA256 d1608a26...52ab3e. The historical log/JSON record successful execution on 2026-10-10 with Lean 4.34.1 and pinned Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612. This is historical evidence inspected here, not a new compilation by this reviewer.

**Exact fixed Lean scope:** G,H and their actual product are connected, both factor lower GP values are at least 6, product lower GP is at most 5, and the original universally quantified bound therefore fails. The source does not prove G lower GP equals 6, the full r-family, the universal min-5 theorem, the sharp all-r result, or product lower GP equals 5. Those stronger statements have the separate written/computational dependencies above.

## 9. Actual bounded independent executions

Executed `scratch/independent_small_controls.py` using the bundled Python; exit code 0, recorded UTC 2026-10-12T09:07:14.722667+00:00. The source hashes were compared before and after and were unchanged. Results are in `scratch/independent_small_controls.json`.

- MET3/MET4 only: isolated the production ray function, replaced its fixed 25-ray count for these smaller dimensions, and instrumented every positive/negative candidate pair with an **independent exact rational matrix-rank adjacency criterion**. All 5 and 39 adjacency-pair checks agree. Outputs are the 3 and 7 expected cut rays. Queue zero-mask closure equals direct enumeration of every ray support, giving 8 and 106 patterns. The original MET5 routine was not called.
- Five small actual connected graph-product fixtures: built fresh adjacency/BFS distances and examined 2,518 GP sets of sizes at most four. For each product point, the mask compatibility criterion agrees with direct triangle-equality extension: 46,148 checks. The sets include 1,813 with a repeated factor projection. All 412 applicable factor-demand instances have actual landmark-outside extensions.
- 2,000 small independently generated Boolean demand/profile systems: isolated only the production `infeasible` function and compared it in both factor orders with direct enumeration of **every** first/second profile subset. All comparisons agree, including known-profile constraints and empty-demand failures. The production function visited 4,299 states.

These controls test semantic edge cases, adjacency implementation, zero-mask closure and pruning direction. They do not establish the 25-ray/9,484-pattern MET5 totals or the full nonexistence claim by themselves.

## 10. Concrete manuscript requirements and remaining verification

No mathematical repair is requested on these frozen sources. For a reviewable new manuscript, retain the following distinctions:

1. Define finite nonempty simple graphs, shortest-path GP, inclusion-maximality and lower GP explicitly; handle disconnected graphs componentwise.
2. State the ordinary conjecture as false and the min-5 theorem as its sharp universal replacement. Do not call the replacement a proof of the untruncated conjecture.
3. Explain zero distances/repeated projections, three separate equality bits, and why numerical-group unions are a relaxation in the safe direction.
4. Include the maximal-landmark subset demand lemma and the common-face/clipping proof for double description. A PASS label and the count 25 alone are not completeness evidence.
5. Bind ROOT's fresh complete certificate replay and Lean compilation to the exact hashes below. Retain historical records without presenting them as newly executed.
6. Label the universal theorem computer-assisted, the all-r counterexample family a written proof, and the Lean result a fixed connected 11-by-29 refutation. Product equality 5 depends on the universal theorem.
7. Do not infer minimum counterexample order, an exact H_r lower GP value, all-parameter Lean, historical firstness, or human peer review.

The only execution not performed by this reviewer is the intentionally ROOT-owned full certificate/Lean replay; that is an evidence boundary, not a newly found mathematical obstruction. A later frozen TeX review must independently check that the manuscript preserves these claims and dependencies.

## 11. Actual SHA256 bindings

All paths below are relative to the baseline `research` repository and were hashed from actual file bytes. The full machine-readable table is also in the small-control JSON.

| File | SHA256 |
|---|---|
| workstreams/ROOT/lower-gp-product319-counterexample/PROOF.md | bfc815e52a7a918705b256fce12bf61a98a853fd49dcff5b2c4b9a47e865f658 |
| workstreams/ROOT/lower-gp-product319-counterexample/FAMILY_PROOF.md | 7a1128ec4186fffa041ac013fe1bdfef4e58e079700f834841b39ab47defb7ad |
| workstreams/ROOT/lower-gp-product319-counterexample/LowerGPProduct319.lean | d1608a26b68eface444fc2c2feb53ebe8b24e364021213f589bd51e3aa52ab3e |
| workstreams/ROOT/lower-gp-product319-counterexample/lean-audit.json | 67217678b5058d53f6de36d21364ad19fd784a1205f698a59967ece448f9f5f3 |
| workstreams/ROOT/lower-gp-product319-counterexample/lean-audit.log | 68d4c28da37b5fcf044e9f829504e9cedbec1cc1036d58b844203d1118a6dc35 |
| workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/UNIVERSAL_FIVE_PROOF.md | 9ecfeb62c4f52a2ef86ae161a0b1fb8c5f4ca16e96eb62a2b14a3af83122aac5 |
| workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/UNBOUNDED_GAP_PROOF.md | 0970e52c71f759c24c1281bce5b7a1c9f4095398d511f556cd709b5a19d3496e |
| workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/verify_metric_rays.py | 59299a4e518d539dc9a527832eddfe8842f62c171cce1df0b46bf1634db9321c |
| workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/verify_arbitrary_four.py | 9ff179bc74f046a639247b4df16040258c9a62dfcbf7ce05fa404904dcd38997 |
| workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/verify_universal_five.py | a3fbbc53d73ed2144c489c6ec89048c0dac2d76693577a52fb7a7ea8484b63a3 |
| workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/metric_faces.json | 01001dc53737560f49749784eaef85fe4d8c9297afde51093923a34ef185a382 |
| workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/metric_rays_verified.json | 0153b1d6ca7449b5c6f7a4af256b3bcf8c6513e48ac8b226554a1b384339a8ef |
