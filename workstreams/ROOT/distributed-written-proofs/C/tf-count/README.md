# TF normal form and nontrivial-instability enumeration

## Scope

For a fixed disjoint-transpositions TF pair, the unconstrained labelled count is exactly 2^(choose(N-4,2)+2(N-4)+2), and the source-constrained fixed-pattern count is asymptotic to 2^(choose(N,2)-2N+3). For N>=16 the sharpened unlabelled lower bound is (19/20)2^(choose(N,2)-2N+3)/N!. In the full connected nonbipartite twin-free target class, L_n~3 choose(n,4)2^(choose(n-4,2)+2(n-4)+1), U_n~2^(choose(n-4,2)+2(n-4)-1)/(n-4)!, and U_n/g_n~2(n)_4/4^n. Almost all target graphs have Aut(G)=C2 and Aut(CDC(G))=D8 of order eight. Source: [Hujdurovic–Mitrovic, Problem 5.3, DOI 10.1002/jgt.23018](https://doi.org/10.1002/jgt.23018).

## Dependencies and prior theory

The five notes retain the mathematical dependency chain. The global proof supplies small/large-support exclusion, overlap control and canonical unlabelled reconstruction; the group corollary depends on it. Optional finite diagnostics remain accessible through frozen original source links and are not logical dependencies of the universal written proof. Universal odd-order exact-two-cousin classifications and quantitative/effective extensions are outside this packet.

Construction 5.1 / Proposition 5.2 is the original authors' published four-vertex construction. Ordinary random-graph rigidity, Burnside and all-graphs enumeration are classical prior inputs. The fixed lower bounds are prior-method consequences, not separate solved conjectures.

## Verification boundary

The fixed normal form and two lower bounds received independent written review on 2026-10-10. A later genuine independent review accepted the raw public global proof and group corollary. This does not accept odd-CG or quantitative expansions.

The stated scope has complete independently reviewed written mathematics; finite certificates are identified above when required. There is no complete all-parameter Lean proof for these statements. No Lean compilation, mathematical enumeration or checker replay was performed during integration. Preparation checked exact source/output hashes, Python syntax, JSON encoding and required local dependencies. Historical novelty remains unconfirmed.

## Frozen sources

Original branch: `partner/dist-C-audit-1010`. Exact input/output hashes and all editorial transformations are recorded in `provenance.json`. Removed operational appendices remain accessible in the frozen sources.

| Integrated file | Frozen mathematical source | Original SHA256 |
|---|---|---|
| [MINIMAL_TF_SYMMETRY_NORMAL_FORM.md](MINIMAL_TF_SYMMETRY_NORMAL_FORM.md) | [workstreams/C-audit-1010/MINIMAL_TF_SYMMETRY_NORMAL_FORM.md](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/MINIMAL_TF_SYMMETRY_NORMAL_FORM.md) | `2579c69b738a8b82b87fde354dd1d3e0331eea04944c7e076f95be9587488e8f` |
| [UNSTABLE_DENSITY_LOG_BOUND.md](UNSTABLE_DENSITY_LOG_BOUND.md) | [workstreams/C-audit-1010/UNSTABLE_DENSITY_LOG_BOUND.md](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/UNSTABLE_DENSITY_LOG_BOUND.md) | `fa01cdc2ff96883a6781b6bcae3372fe65f5778ea645d93dd0537f366b5bad45` |
| [UNSTABLE_DENSITY_SHARPENED_LOWER.md](UNSTABLE_DENSITY_SHARPENED_LOWER.md) | [workstreams/C-audit-1010/UNSTABLE_DENSITY_SHARPENED_LOWER.md](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/UNSTABLE_DENSITY_SHARPENED_LOWER.md) | `f9afa5c013202fd6b1b488265d01d45946a22628f20b88063632bcf476b860ed` |
| [GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md](GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md) | [workstreams/C-audit-1010/GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md) | `0de1b11b640aae8fb87292d4926748f589f3787de87e2792ed711c84be1740da` |
| [GENERIC_COVER_GROUP_COROLLARY.md](GENERIC_COVER_GROUP_COROLLARY.md) | [workstreams/C-audit-1010/GENERIC_COVER_GROUP_COROLLARY.md](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/GENERIC_COVER_GROUP_COROLLARY.md) | `04d019a58f32649ed8f1edd2bdc2fe82fc68fc8fc7f4564196ce70ba1bed59c1` |
