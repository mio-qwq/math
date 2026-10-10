# Exact general position number of length-three Kautz digraphs

**Candidate theorem.** For every integer m>=3,

    gp(Ka(m,3)) = m(m-1)(2m-1)/6 = sum_{j=1}^{m-1} j^2.

This gives an affirmative answer to the k=3 Kautz part of Problem5.2 of Chandran et al., arXiv:2604.15909v1. It is NOT a counterexample and does not settle other word lengths, permutation digraphs, or orientation spectra. The source's Table1 gives the first five numerical values, but the universal equality is the result claimed here. Pending independent review and historical-novelty assessment; no Lean claim.

## 1. Definitions and distances

Fix an alphabet A with m symbols. Vertices are words abc with a!=b and b!=c; equality a=c is allowed. An arc abc->bcd exists exactly when c!=d. Only the final symbol is forbidden for the append operation, unlike a permutation digraph.

For distinct vertices u=abc and v=xyz the original directed distance is

- 1 if bc=xy;
- 2 if bc!=xy and c=x;
- 3 otherwise.

A one- or two-step walk necessarily has the corresponding suffix/prefix overlap. Conversely, append the needed target suffix when there is an overlap. If neither overlap exists, c!=x and appending x,y,z gives a legal three-step walk. The lower bounds exclude shorter paths, so these are the exact distances. Equal vertices have distance0.

Consequently the diameter is at most3, and restricting to words on any subalphabet of size at least2 is isometric. Reversing each word is an anti-isomorphism: it reverses every arc, and thus preserves the general-position property while exchanging first and last symbols.

A set S is in general position when no three distinct members u,v,w satisfy d(u,v)+d(v,w)=d(u,w). All distances in the proof are in this full original digraph.

## 2. Independent sets give the proposed value

Order the alphabet and select every word abc whose middle letter b is strictly smaller than both a and c. There are sum_{j=1}^{m-1}j^2 such words. They form an independent set: consecutive selected words abc,bcd would require both b<c and c<b. Every independent set in a digraph of diameter at most3 is general-position, since two positive selected-to-selected distances are each at least2 and cannot sum to a distance at most3.

We also need an upper bound on independent sets. For each unordered pair {a,b}, the two words aba,bab form a directed2-cycle, so at most one can be selected independently. For each unordered triple {a,b,c}, its six distinct-letter words partition into two directed3-cycles, each contributing at most one to an independent set. These pieces partition the entire vertex set. Therefore every independent set has size at most

    binom(m,2) + 2 binom(m,3) = m(m-1)(2m-1)/6.

It remains to handle general-position sets that contain an arc.

## 3. Missing-first-letter counting lemma

**Lemma.** If S is in general position and no word of S starts with a specified letter0, then at most(m-1)^2 words of S contain0. The same holds with “ends” instead of “starts”.

Put B=A minus {0}, r=|B|. Words of S containing0 have exactly one of the forms

    M_ab = a0b, with a,b in B;
    E_ab = ab0, with a,b in B and a!=b.

Let M be the set of occupied cells(a,b) with M_ab in S. We inject all selected E_ab into the r^2-|M| unoccupied M-cells.

If M_ba is absent, map E_ab to cell(b,a). If M_ba is present, map E_ab instead to the diagonal cell(a,a). This diagonal cell is absent: E_ab -> M_ba has distance1, M_ba -> M_aa has distance2, and E_ab -> M_aa has distance3. These are three distinct words, so M_aa cannot be selected.

Moreover, in that second case E_ab is the ONLY selected E-word with first letter a. For any c in B distinct from a,b, the three distinct words E_ab, M_ba, E_ac have successive distances1 and2, while d(E_ab,E_ac)=3. Thus E_ac cannot lie in S. This includes every other valid E-word starting with a.

The map is injective: first-case images are distinct off-diagonal cells, second-case images are diagonal, and two second-case words cannot have the same first letter by the preceding paragraph. Hence |E|<=r^2-|M| and |E|+|M|<=r^2, proving the lemma. Word reversal proves its last-letter version.

## 4. A selected arc provides a low-incidence letter

Suppose u=abc and v=bcd are both in S. Adjacent letters are unequal, but other equalities are possible. We show that some letter belongs to at most(m-1)^2 words of S, for m>=3.

**Case I: d is different from both a and b.** No word w of S starts with d. Such a w would be different from u,v, and d(v,w)=2, d(u,w)=3. Together with d(u,v)=1 this contradicts general position. Apply Section3 to d.

**Case II: d=b and c!=a.** No word of S ends with a. This is the reversal of Case I, applied to the reversed arc dcb->cba, since a differs from d=b and c. Apply the last-letter version of Section3 to a.

**Case III: d=a.** Here a,b,c are pairwise distinct, and the selected arc is abc->bca. A word of S starting with a must be u: for any other such w, d(v,w)=2 and d(u,w)=3, a contradiction. Reversing the argument shows that a word of S ending with a must be v.

All other selected words containing a therefore have a in the middle. Of the(m-1)^2 possible middle-a words, bab and cac are absent. Indeed,

    bab -> abc -> bca
    abc -> bca -> cac

are length2 geodesics with distinct vertices. Adding the two possible endpoint occurrences u,v and subtracting these two missing middle words gives at most(m-1)^2 occurrences of a.

**Case IV: c=a and d=b.** The selected pair is the digon u=aba,v=bab. The only selected word starting with a is u. To prove this, write another such word as w=axy. If x=b, then u->v->w is a length2 geodesic. If x!=b, then d(v,u)=1, d(u,w)=2, d(v,w)=3. Both alternatives contradict general position. Symmetry gives the analogous assertion for words starting with b; reversal gives the two corresponding last-letter assertions.

Thus, outside u and v, any selected word containing a has a in the middle and has neither a nor b at either end. There are at most(m-2)^2 such words. The incidence count of a is at most

    (m-2)^2+2 <= (m-1)^2  (m>=3).

The four cases exhaust all possibilities: if d!=b, either d!=a (I) or d=a (III); if d=b, either c!=a (II) or c=a (IV).

## 5. The base m=3 without a computational assumption

An independent S has size at most5 by Section2. Otherwise select an arc and use the cases above.

- In Case I, the three-letter alphabet forces c=a. Deleting d leaves only aba and bab as possible words, of which aba is selected. The triple bab->aba->bad is a length2 geodesic, so bab is not selected. At most four selected words contain d by Section3, and at most one avoids d. Thus |S|<=5.
- In Case II, deleting a leaves bcb=v and cbc. The geodesic abc->bcb->cbc prohibits cbc. At most four selected words contain a, again giving |S|<=5.
- In Case III, deleting a leaves bcb and cbc, which cannot both be selected because abc->bcb->cbc is a length2 geodesic. Section4 bounds the incidence of a by four, so |S|<=5.
- In Case IV, Section4 bounds the incidence of a by three, and there are only two words on the remaining two-letter alphabet. Hence |S|<=3+2=5.

The independent construction has five vertices. Therefore gp(Ka(3,3))=5.

## 6. Induction

Assume m>=4 and the theorem for m-1. If S is independent, Section2 already gives the required upper bound. Otherwise Section4 supplies a letter x occurring in at most(m-1)^2 selected words. Deleting all words containing x leaves a general-position set in the isometric Ka(m-1,3), so

    |S| <= gp(Ka(m-1,3)) + (m-1)^2
         <= sum_{j=1}^{m-2}j^2 + (m-1)^2.

The lower bound from Section2 matches. This completes the proof for every m>=3.

## Verification and provenance

The proof uses only the original shift adjacency and explicit shortest paths; there is no optimization, asymptotic assumption, finite extrapolation, or imported unproved graph lemma. The independent-set count and counting injection were personally derived by B during this reserved task. The table's observed sum-of-squares pattern belongs to the source. No claim of historical firstness follows from a bounded search.

The companion definition-first checker reconstructs the actual digraph, runs BFS, checks every local distance pattern used above, exhaustively verifies the m=3 base, and tests the explicit lower-bound sets. Its finite tests supplement rather than replace the universal proof. A separate implementation by B is not independent peer review. Review should concentrate on the injection in Section3, exhaustiveness of the four arc cases, and preservation under alphabet deletion. The theorem excludes m=2, where the digon has general position number2 rather than the sum-of-squares value1.
