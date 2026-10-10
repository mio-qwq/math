# B self-review: universal three-point extension

2026-10-10 11:11UTC. Role: discovering researcher; independent reviewer pending. This packet proves a partial all-orders bound for the original problem, not a counterexample or complete conjecture solution.

Review the statement `gp^-(G square H)>=min{4,gp^-(G),gp^-(H)}`. It implies the original bound for ALL graphs with at least one factor parameter<=4. The proof handles connected factors first, isolated single-vertex factors directly, and disconnected graphs by component additivity and a positive-integer truncation inequality. Empty graphs can be included under the usual zero convention.

The key reduction is not an inference from the two discovery searches. Any product GP triple with a GP three-point projection is extendable if its factor has lowerGP>=4. A two-value projection is handled using two factor-pair extensions. The only remaining possibility is three distinct collinear projected points in both factors with different middles. Section4 shows that at least one of three explicit product vertices extends the triple; it treats coincidences in intermediate candidate coordinates using the exact coordinate triangle deficits. Every case requiring an extension uses a GP-set with cardinality strictly below the actual factor lowerGP parameter.

The important review point is the opposite-middle argument. For the shared endpoint0 and factor middles1/2, failure at(u,b0) forces any equality for{u,a1,a2} to have middle a2; failure at(a0,v) forces any equality for{v,b1,b2} to have middle b1. Thus the third candidate(u,v) cannot have simultaneous coordinate equalities for the remaining old pair. This is proved with arbitrary positive distances x,y,p,q, not by checking bounded integer distances.

Actual run, Python3.12.14 standard library:

    python workstreams/B/lower_gp_product/verify_extension.py

Result PASS:5graph fixtures;287direct factor-extension hypotheses;18314 original BFS matrix entries;182208 GP product triples extended; all seven construction branches exercised (including1024third-candidate graph instances);7integer-metric signatures and49pairs as algebra regressions, with9third-candidate-required pairs;4disconnected/boundary fixtures;3negative controls. The verifier imports the proposed constructor, but independently rebuilds the actual Cartesian adjacency and distances and checks each returned point against original GP definitions. Neither discovery script is imported. This is an independent-algorithm self-check, not independent review.

Discovery:16small factors with no maximal GP set of size<=3 yielded no such product witness across120pairs (7,312,740subsets);6true-twin-blow-up factors yielded none across21pairs (33,252,580subsets). These old searches are now superseded: searching for a three-point counterexample cannot succeed if the written theorem is correct. Do not increase those windows or count the rejected samples as additional results.

Source hashes are in SHA256SUMS and the handoff checkpoint. No Lean compilation, added axiom, journal review, minimum counterexample order or firstness claim. Next mathematical question: can the three-point construction be extended to four-point sets, or can a counterexample have both factor parameters>=5 and a product maximal GP-set of size>=4? No claim about that remaining regime has been proved.
