# Endpoint supports and the independent strict-code subclass

Candidate structural note, GP2-20261012. All statements here concern **strict window codes**, unless an actual Kautz lift is explicitly stated. This note supplies reductions and a deletion obstruction; it does not improve the universal density bound or establish that an extremal code is independent. Historical novelty is unconfirmed. No Lean proof is claimed.

## 1. Definitions

Let `A` be a finite alphabet. A strict window code is a set `C subset A^4` for which every word in `A^8` has at most two selected length-four windows at positions `0,...,4`. Occurrences are counted by position, even if they spell the same word. The alphabet words here may have equal adjacent letters. The elementary repair theorem in `../construction/STRICT_WINDOW_REPAIR.md` connects this stronger finite object to arbitrary original Kautz GP sets with an `O(m^3)` deletion error.

For `r=1,2,3`, let `P_r` and `Q_r` be the sets of length-`r` prefixes and suffixes, respectively, of words of `C`. Call a selected word `w` **incoming-free** when `prefix_r(w) notin Q_r` for all `r=1,2,3`; call it **outgoing-free** when `suffix_r(w) notin P_r` for all three lengths. These terms refer to selected overlapping occurrences, not to all arcs of the ambient Kautz digraph.

A selected adjacency is a five-letter word `abcde` such that `abcd` and `bcde` both belong to `C`. Put `P=P_1`, `Q=Q_1`, `L=P minus Q`, and `R=Q minus P`.

## 2. Every selected adjacency has free exterior ends

**Lemma 1.** In any selected adjacency `u=abcd`, `v=bcde`, the word `u` is incoming-free and `v` is outgoing-free. In particular `a in L` and `e in R`.

**Proof.** If some selected word has a suffix equal to a prefix of `u` of length `r`, it can be followed by `u` after `4-r` shifts, and then by `v` after one further shift. The three selected occurrences span `5-r <= 4` shifts. Extend the resulting word to length eight if necessary. This contradicts strictness. The argument on the right is the same: after `u,v`, append a selected word whose prefix overlaps `v` in `r` symbols. No assumption of distinct selected words or distinct letters is used. Taking `r=1` says `a notin Q` and `e notin P`; their selected-word roles also give `a in P` and `e in Q`. ∎

**Corollary 1.** If either `P subset Q` or `Q subset P`, the code has no selected adjacency. In particular this holds when `P=Q` or when both are the whole alphabet.

Thus a proof for independent codes cannot be imposed on arbitrary codes without an additional argument. Nonindependence requires both endpoint-exclusive sets `L` and `R` to be nonempty.

A more precise consequence is that, in the adjacency digraph induced by the selected words, every nonisolated component is bipartite with all arcs from words having selected out-neighbors to words having selected in-neighbors. No selected word can have both kinds of neighbor. These two sides lie among incoming-free and outgoing-free words, respectively. The assertion is about the structure of each induced component; it does not require its edges to be complete bipartite.

## 3. A universal three-level pair graph

For any code `C`, form a digraph `H_C` on all ordered pairs `A^2`, with the edge

`ab -> cd` exactly when `abcd in C`.

Loops and repeated letters are included in this definition.

**Lemma 2.** Every strict code has no three-edge directed walk in `H_C`. Consequently there is a map

`ell : A^2 -> {0,1,2}`

such that `ell(ab) < ell(cd)` for every `abcd in C`.

**Proof.** A three-edge walk on pair vertices `B_0,B_1,B_2,B_3` gives the eight-letter concatenation `B_0 B_1 B_2 B_3`. Its windows at positions `0,2,4` are all selected, which violates strictness. In any digraph with no three-edge walk, define `ell(v)` as the largest length of a directed walk ending at `v`, allowing the length-zero walk. This largest length belongs to `{0,1,2}`. Appending any edge `u->v` shows `ell(v) >= ell(u)+1`, as required. In particular directed cycles and loops cannot occur. ∎

The level structure holds for **every** strict code; independence is not needed. Conversely, any graph all of whose edges increase a three-valued level has no three-edge walk.

For independent words, this is exactly the remaining restriction. Independence means `P_3 intersection Q_3` is empty. If selected occurrences are independent, the only way three of them can lie in five consecutive windows is at positions `0,2,4`. Thus a code is independent and strict if and only if it has no selected adjacency and its pair graph admits the displayed three levels.

## 4. An exact characterization for arbitrary strict codes

**Theorem 3.** A set `C subset A^4` is strict if and only if both of the following hold:

1. `H_C` has no three-edge directed walk.
2. For every selected adjacency `u,v`, the first word is incoming-free and the second is outgoing-free.

**Proof.** Necessity is Lemmas 1 and 2. For sufficiency, suppose selected occurrences occur at `t_0<t_1<t_2` with `t_2-t_0<=4`, and let the two positive gaps be `a,b`. If neither gap is one, then `a=b=2`; these occurrences give a prohibited three-edge walk in `H_C`. Otherwise there is an adjacent selected pair. If `b=1`, the first word of that adjacent pair has the earlier selected occurrence at gap `a<=3`, contradicting its incoming-free property. If `a=1`, the last word of that pair has the later selected occurrence at gap `b<=3`, contradicting its outgoing-free property. These cases exhaust all positive gaps with sum at most four. ∎

This is a support-based exact criterion. It replaces testing all eight-letter words by prefix/suffix support tests and a three-level pair graph, but does not by itself solve the extremal optimization over those supports.

## 5. A complete saturation representation of the independent subclass

Given arbitrary maps

`ell : A^2 -> {0,1,2}`,  `tau : A^3 -> {0,1}`,

define

`C_(ell,tau) = {abcd : ell(ab)<ell(cd), tau(abc)=1, tau(bcd)=0}`.

**Theorem 4.** Every such code is independent and strict. Conversely, every independent strict code is contained in one of these codes on the same alphabet.

**Proof.** Selected adjacency would require the shared triple to have both `tau=0` and `tau=1`, so it is impossible. The pair levels exclude three-edge walks, and Section 3 now gives strictness. For the converse, use the canonical levels of Lemma 2 and put `tau=1` precisely on `P_3(C)`. Because independence gives `P_3(C) intersection Q_3(C)=empty`, every original selected word obeys both triple conditions as well as its pair-level condition. Adding every other word obeying those conditions preserves independence and strictness by the first part. ∎

For any probability vector on `A`, the exact independent-class density optimization is therefore

`max_(ell,tau) Pr[ell(U_0,U_1)<ell(U_2,U_3), tau(U_0,U_1,U_2)=1, tau(U_1,U_2,U_3)=0]`,

where the four letters are independent with that common distribution. This is a finite-label structural parametrization. It does **not** assert that all strict codes can be saturated in this form, nor that independence preserves the global optimum. The interaction between the pair levels and the overlapping triple cut remains the substantive optimization problem.

## 6. Dense adjacency cannot be removed at lower-order cost

Consider the binary strict code `D={0001,0011}`. Among gaps `1,2,3`, the only possible overlap from one selected pattern to another is `0001 -> 0011` at gap one. Its first pattern has no selected predecessor with any of those gaps and its second has no selected successor. There are no gap-two overlaps, so the pair graph has no directed walk of length two, and Theorem 3 proves strictness. This also proves strictness directly without any optimizer.

### Full strict-code blow-up

Partition an alphabet into two blocks `L,R`, each of size `q`, and retain every four-letter word with block pattern `0001` or `0011`, including words with equal adjacent letters. Each type contains `q^4` words, so there are `2q^4` in total.

For a fixed triple `(b,c,d) in L x L x R`, selected adjacencies form a complete bipartite component between

`{abcd : a in L}` and `{bcde : e in R}`.

These are all selected adjacencies, and the components partition all selected words. Each component is `K_(q,q)`, and there are `q^3` components. An independent subset contains at most one entire side's worth, namely at most `q` of its `2q` vertices. Consequently every independent subset has size at most `q^4`, with equality attained by retaining either one of the two block patterns.

### Actual valid Kautz blow-up

Now retain only valid vertices in `Ka(2q,4)`, with `q>=2`. The two pattern counts are both

`q^2(q-1)^2`,

since the two same-block adjacent inequalities each remove one choice. The whole set is original GP because it is a valid-word lift of the strict template.

A component is indexed by `b,c in L` with `b!=c` and `d in R`; there are `q^2(q-1)` such triples. Its two sides are

`{abcd : a in L minus {b}}` and `{bcde : e in R minus {d}}`,

so it is `K_(q-1,q-1)`. These components again partition the selected words and include all their selected adjacencies. Every independent subset must therefore delete at least

`q^2(q-1)^2 = (2q)^4/16 + O(q^3)`

vertices, exactly half of this GP set. The lower bound is attained by removing one pattern completely.

Thus neither an `O(m^3)` independent-subset repair nor density-preserving deletion can hold for arbitrary GP sets. This does not rule out a transformation that **replaces** selected words by different ones, nor does it show that this small-density example is globally extremal. Any proposed independent-class completeness theorem needs such an additional mechanism.

## 7. Reproducible finite checks and remaining work

`verify_endpoint_structure.py` checks the support and layer criteria against direct length-eight windows for every subset of the two-pattern example and for representative independent codes. It rebuilds the actual small Kautz graph by its shift-and-append adjacency for `q=2,3`, verifies the connected components and exact independent-subset bound, and includes damaged code, distance and parameter controls. Its role is semantic checking; the all-alphabet proofs are Sections 2–6.

The next mathematical question is whether replacement can reduce arbitrary extremal strict codes to the exact independent saturation family of Section 5. Pure deletion is now ruled out. Even within that family, a density bound of `1/4` would require a new inequality coupling the overlapping triple cut to the pair levels; the elementary three-level edge count alone still gives only `1/3`.
