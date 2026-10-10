# Bipartite subcubic strengthening: review packet

B,2026-10-10 12:32UTC. Baseline general-familyd1d82779f60c522dd2fa689d27c7c839d1115012. This is a stronger restriction of the SAME original Problem4negative answer, not another conjecture. Previous frozen proof bytes unchanged; independent review pending.

For k=2^h,h>=2, graph is connected simple BIPARTITE of maximum degree3. One root has exactp_v=2k by explicit geodesic cover and selected2kposition set. Another root has N+kstrict-boundary witnesses,N=(k-1)(k-2)/2. Ratio>=k/4-1/4+1/(2k) is unbounded. No cubic-REGULAR, planar,2connected, order-minimum or exactglobalextrema claim.

Proof SUBCUBIC_PROOF.md SHA256662b373c535973b83c9676e850fc134410d1c14e767f970d7dded8cce671918e
Verifier verify_bipartite_subcubic.py SHA2568da8c717884d97c2e5f8014ed68c8b0efb8c6447289b948dc1aa9dd9a7c49652
Actual Python3.12.14 stdlib command: python workstreams/B/vertex_position_ratio/verify_bipartite_subcubic.py. PASS. h2/3/4/5orders94/686/5662/46910; edges99/713/5781/47405; all maximumdegree3/bipartite. Exactp_v8/16/32/64; p_ulower7/29/121/497. Three BFS rows (initialu/finalu/finalv)282/2058/16986/140730entries; extra small-instance BFS1410/30870entries checks49/526selectedpairs. Four negative controls PASS. Digestb39e3e96b98d4567db502c94d907706ee5ff4960359e9c5c5ff27767cdf66220.

The weaker first rows are legitimate lower bounds even below1; divergence follows from allh, not monotonicity inferred from four samples. The largest tested ratio>=497/64>6is only an illustration, not the reason boundedness fails. The universal proof is an explicit exact-potential induction.

Critical checks: balanced binary tree ensures common leaf height; backbone links MUST be subdivided to certify bipartiteness; source0is omitted; targetjdescends and sourceidescends by1; initial root distance to trackjbase is2j+2because all tree detours cost>=4k; each current target suffix drops exactly2; all oldcrossedges lie below the updated suffix. The2kroot-position witness includes Hvertices which are NOT boundary themselves: any ascending continuation ends at an unselected Mvertex, so they cannot lie on geodesics to selected track terminals. This distinction is explicit in proof and checker.

Discovery preserved a nonsubdivided-base subcubic intermediate in probe_subcubic.py/log/json. It was not frozen as a final theorem and was superseded before delivery by the bipartite family; no contradictory run or hidden correction occurred. No discovery imports or matching routines in the standalone verifier. All finite cases are semantic checks, not a proof by extrapolation. Generic boundary/path-cover principles are credited in the base proof.

Source gate refreshed with exact vertex-position/ratio/subcubic/bipartite/bounded-degree queries, no matching prior solution located. Historical novelty remains uncertain. No external construction adopted, new agents, main edit, author contact, Lean or external review. Next: freeze/replay this stronger packet, then stop adding restrictions merely to inflate result count. The two original-question answers already delivered await independent review.
