# A direct affirmative answer to the Collins–Sciriha CDC/main-eigenvalue question

**Agent C / independent mathematical research note / 2026-10-10 (UTC).**

**Classification:** A proof of an *affirmative answer to an explicitly posed public question*, **not a counterexample**. No claim of originality, historical priority, independent peer review, or a new published discovery. The argument is elementary enough to be implicit in prior literature; it must be checked against existing sources before any novelty claim.

## 1. Original problem and precise scope

Luke Collins and Irene Sciriha, *On the Walks and Bipartite Double Coverings of Graphs with the same Main Eigenspace*, arXiv:1906.05790v1 (13 June 2019), **Question 5.8**, PDF p. 15 (physical page index 14), ask:

> Given finite simple graphs \(G,H\) with \(\operatorname{CDC}(G)\cong\operatorname{CDC}(H)\), must \(G,H\) have the same main eigenvalues?

The journal article by Irene Sciriha and Luke Collins, *The walks and CDC of graphs with the same main eigenspace*, **Discussiones Mathematicae Graph Theory** 43(2) (2023), 507–532, DOI `10.7151/dmgt.2386`, restates the problem as **Question 16**, expressly calling it open on journal p. 522. The arXiv and published numbering are different. Search/review date: 2026-10-10. These are verified *statements at their respective publication dates*, not a guarantee that no later result exists. A bounded title/question/wording search did not establish historical novelty. The original arXiv paper already states Theorems 3.3 and 4.2 about walk matrices and two-fold isomorphism; the affirmative answer below might be a short unremarked consequence of such background. Verify before public attribution.

References:

1. https://arxiv.org/pdf/1906.05790 (especially pp. 1–3, 9, 15), arXiv v1.
2. https://doi.org/10.7151/dmgt.2386 (2023 journal, Theorem 12 and Question 16).
3. https://bibliotekanauki.pl/articles/59877152.pdf (open-access publisher rendering; journal pp. 517–522).
4. https://arxiv.org/html/2603.27559v3 (later relevant TF-covering discussion; not by itself proof of current open status).

Definitions fixed as in the original. An adjacency eigenvalue \(\lambda\) of a finite simple undirected graph \(G\), with real symmetric adjacency matrix \(A\), is **main** iff its eigenspace has a vector not orthogonal to \(\mathbf1_n\). Let \(\mathcal M(G)\) be the **set of distinct** main eigenvalues (not the full adjacency spectrum, not algebraic multiplicities). \(\operatorname{CDC}(G)=G\times K_2\), on vertices \(V(G)\times\{0,1\}\), has an edge \((u,i)(v,1-i)\) precisely when \(uv\) is an edge of \(G\). In layer ordering its adjacency matrix is

\[
D=\begin{pmatrix}0&A\\A&0\end{pmatrix},\qquad \mathbf1_{2n}=\begin{pmatrix}\mathbf1_n\\\mathbf1_n\end{pmatrix}.
\]

## 2. Complete proof, directly from the definition

**Lemma (main eigenvalues survive the canonical double cover exactly).** For every finite undirected graph \(G\),

\[
\boxed{\mathcal M(\operatorname{CDC}(G))=\mathcal M(G).}
\]

*Proof.* Consider the orthogonal, \(D\)-invariant subspaces

\[
U_+=\{(x,x):x\in\mathbb R^n\},\qquad
U_-=\{(x,-x):x\in\mathbb R^n\}.
\]

Their direct sum is \(\mathbb R^{2n}\). On \(U_+\), \(D(x,x)=(Ax,Ax)\), so \(D|_{U_+}\) has the same eigenvalues as \(A\). On \(U_-\), \(D(x,-x)=(-Ax,Ax)\), so \(D|_{U_-}\) has the negatives of \(A\)'s eigenvalues. Crucially \(\mathbf1_{2n}=(\mathbf1_n,\mathbf1_n)\) lies in \(U_+\) and is orthogonal to **every** vector in \(U_-\).

Fix any real \(\lambda\). A vector in the \(\lambda\)-eigenspace of \(D\) decomposes uniquely into its \(U_+\)- and \(U_-\)-components (both components are themselves \(\lambda\)-eigenvectors, because the decomposition is \(D\)-invariant). Its inner product with \(\mathbf1_{2n}\) is the inner product with the \(U_+\)-component only. That component is \((x,x)\), with \(Ax=\lambda x\), and

\[
\langle (x,x),\mathbf1_{2n}\rangle=2\langle x,\mathbf1_n\rangle.
\]

Thus the \(\lambda\)-eigenspace of \(D\) contains a vector nonorthogonal to \(\mathbf1_{2n}\) **iff** the \(\lambda\)-eigenspace of \(A\) contains a vector nonorthogonal to \(\mathbf1_n\). This remains valid when \(\lambda=0\) or \(\lambda\) and \(-\lambda\) are both eigenvalues; it neither assumes connectivity nor bipartiteness. \(\square\)

**Theorem (affirmative answer to arXiv Q5.8 / journal Q16).** If finite undirected graphs \(G,H\) satisfy

\[
\operatorname{CDC}(G)\cong\operatorname{CDC}(H),
\]

then \(\mathcal M(G)=\mathcal M(H)\).

*Proof.* Let \(S\) be the permutation matrix implementing the given cover isomorphism: \(D_H=S D_G S^{\mathsf T}\). Every permutation matrix fixes the all-ones vector, \(S\mathbf1=\mathbf1\). Therefore \(D_G,D_H\) have exactly the same main eigenvalues: an eigenspace vector \(v\) has nonzero inner product with \(\mathbf1\) iff \(Sv\) does. Apply the lemma to \(G\) and \(H\):

\[
\mathcal M(G)=\mathcal M(\operatorname{CDC}(G))
=\mathcal M(\operatorname{CDC}(H))=\mathcal M(H).
\]

This handles arbitrary finite simple graphs (including disconnected graphs and isolated vertices). \(\blacksquare\)

**What this does NOT imply:** the full adjacency spectra of \(G,H\) coincide, their main-eigenvalue multiplicities coincide, or \(G\cong H\). The assertion concerns exactly the sets of main adjacency eigenvalues from the source problem.

## 3. Second proof: isomorphic-cover walk counts and uniqueness of finite moments

An alternative proof uses only combinatorial walk counts and the standard real spectral theorem; it neither needs the source's TF-isomorphism result nor its walk-matrix proof. For every integer \(k\ge0\), the number of ordered \(k\)-walks in a graph with adjacency matrix \(A\) is \(w_k=\mathbf1_n^{\mathsf T}A^k\mathbf1_n\). In the double cover, every source walk has **two** lifts, one for each initial layer. Hence \(w_k(\operatorname{CDC}(G))=2w_k(G)\). A cover isomorphism therefore yields \(w_k(G)=w_k(H)\) for **all** \(k\).

Writing \(A=\sum_{\lambda}\lambda E_\lambda\), orthogonal spectral projections, gives

\[
w_k(G)=\sum_{\lambda\in\mathcal M(G)}c_\lambda\lambda^k,
\qquad c_\lambda=\|E_\lambda\mathbf1_n\|_2^2>0.
\]

Likewise for \(H\). Let the union of main-eigenvalue sets be \(\{\lambda_1,\dots,\lambda_m\}\) (distinct real numbers), and subtract the two expansions. For \(k=0,\dots,m-1\) the resulting Vandermonde system is nonsingular; hence the difference of each coefficient is zero. Each coefficient on a graph's own main spectrum is strictly positive and is zero elsewhere; thus the supports (main-eigenvalue sets) coincide. This also proves that the two graphs' main spectral masses \(c_\lambda\) coincide, a strictly stronger **weighted** assertion.

## 4. A third matrix route / independent arithmetic identity

For direct comparison with the source's Theorem 4.2, its TF-isomorphism condition gives \(B=P A Q\) for permutation matrices \(P,Q\). Set \(C=P^{-1}BP=A T\) with \(T=QP\). Both \(A,C\) are symmetric. Hence \(T^{-1}A=AT\), or \(TA=AT^{-1}\). As \(T\mathbf1=T^{-1}\mathbf1=\mathbf1\), induction using this relation shows \(TA^k\mathbf1=A^k\mathbf1\) for every \(k\ge0\). A further induction gives \((AT)^k\mathbf1=A^k\mathbf1\), so \(B^k\mathbf1=P A^k\mathbf1\) for every \(k\). In particular all finite walk matrices agree after a *single* relabelling, and their main-eigenvalue sets agree. This route depends on correctly interpreting the cited TF-isomorphism theorem, but the direct cover proof in `2 is self-contained.

## 5. Exact 12-vertex nonisomorphic demonstrator (NOT a counterexample)

Files `certificate-q58.json` and `verify_q58.py` specify two connected nonisomorphic simple graphs, each with 12 vertices and 28 edges, and explicitly specify the map between their canonical double covers. The checker reads **separate raw edge lists** for the two graphs, reconstructs both adjacency matrices from the undirected-edge definition, tests every unordered pair of vertices in their two 24-vertex double covers under the explicit map, tests connectivity and degrees, distinguishes the original graphs by the multiset of incident triangle counts at degree-four vertices, and independently verifies an exact integer Krylov recurrence.

- Source graph nonisomorphism invariant: degree-four vertex triangle-count multisets \((2,2,4,4)\) versus \((3,3,3,3)\).
- Distinct main adjacency eigenvalues in **each** graph: the roots of \(x^2-3x-8\), namely \((3\pm\sqrt{41})/2\). In each graph \(A^2\mathbf1=3A\mathbf1+8\mathbf1\) and \(A\mathbf1\) is not constant. Consequently the vector Krylov space has dimension exactly 2 and its monic minimal polynomial is \(x^2-3x-8\). Since each graph is real symmetric, the roots are exactly its two distinct main eigenvalues, not just potential eigenvalues.
- Both have exactly the same all-ones total walks \(w_0,\ldots,w_6=(12,56,264,1240,5832,27416,128904)\).
- Three negative tests corrupt a cover edge, corrupt the cover permutation, and corrupt the alleged polynomial; all are required to fail.

This finite exact test is an illustration and check of one example. It is **not** a proof of the universal theorem; `2 is that proof. The checker imports nothing from exploratory code and uses integer arithmetic, not floating-point eigenvalue comparisons.

Actual run from inside `workstreams/C/`:

```console
$ python3 verify_q58.py
PASS; exact integer computation; no third-party dependencies
Python: 3.13.5
graphs: n=12, m=28, connected=True
CDC(G) ≅ CDC(H) with explicitly tested 24-vertex map
nonisomorphism: triangles at degree-4 vertices: {'G': [2, 2, 4, 4], 'H': [3, 3, 3, 3]}
minimal polynomial: x^2-3x-8; roots (3±sqrt(41))/2
same walk totals for k=0..6: [12, 56, 264, 1240, 5832, 27416, 128904]
negative tests rejected: 3
```

Source bytes SHA-256 (run `sha256sum verify_q58.py certificate-q58.json`):

- `verify_q58.py`: `74ac11cc8cbc33c8f28978ca42fb0947f760e5341eec9ba07b016725c4b73e75`
- `certificate-q58.json`: `0acbc9ad4f0322b4fa3899eec9857ee2b9a848a3bf168b6819cf2e4a2ded4c1a`

No Lean implementation was attempted: the universal proof is two elementary invariant-subspace arguments, while the certificate is an exact stand-alone Python program. **Lean compilation and axiom audits: not run / not claimed. External independent review: pending.**

## 6. Search history, bounded literature checking, limitations, and stop decision

1. Checked source arXiv v1 and its Theorem 4.2; searched for an existing direct answer and verified the journal version retains the open *Question 16*. Searches not finding an answer do **not** establish novelty or unambiguous open status in 2026.
2. Initially looked for counterexamples among symmetric pairs produced by differing row and column permutations; the exact graph construction and a nonisomorphic example were obtained. Observed walk totals always agreed. The moment and block-matrix arguments prove **no finite counterexample can exist** under the actual question's assumptions, so halted this search; more brute force would add no evidence.
3. The published authors' original Theorem 3.3 already connects isomorphic covers with walk matrices and can suggest a positive result. The direct invariant-subspace proof is shorter and avoids assumptions about how a cover isomorphism maps its two layers. We have **not** established whether this argument was explicitly published independently, or whether the original theorem/proof has a historical correction or erratum. A 2023 paper can call a question open at publication while a new note offers a proof; that is not evidence of firstness.
4. The complete proof is a mathematical argument in this note, *not* a formally kernel-checked Lean theorem or third-party peer review. No submitted paper, author communication, or universal automated proof is claimed. The finite checker checks exactly its finite encoded example.

**Disposition:** Complete written affirmative proof and exact finite demonstrator submitted for independent review. Not suitable for a counterexample claim; stop original counterexample search. Integration by the primary agent must preserve the distinction from workstream 006 (a genuine published-conjecture counterexample), and should obtain a genuinely independent proof review and a more exhaustive originality check before publicly calling this a new solution.
