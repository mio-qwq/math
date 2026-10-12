# Correcting the displayed identities in Braun-Bruegge Proposition 30

This note concerns Proposition 30 and its proof on printed pages 22-23 of Braun-Bruegge, *J. Integer Sequences* **26** (2023), Article 23.7.2, <https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf>. The corresponding erroneous ratios also occur in the inspected arXiv v1-v4 PDFs of <https://arxiv.org/abs/2201.13303>.

The proposition's upper-bound conclusions remain valid. The correction is to displayed identities in the proof; no historical first-discovery claim is made.

## 1. A boundary formula from the facet definition

Let a,b be positive even integers, a,b>=2. The graph CB(a,b,1) is simple. Set

\[
A=\binom a{a/2},\qquad B=\binom b{b/2}.
\]

Then

\[
\boxed{N(CB(a,b,1))=\frac{ab+2}{2}AB.}
\tag{1}
\]

Here is a direct explanation using the established facet-labeling characterization (Theorem 5 in the source). Normalize one common endpoint to 0 and write t for the other endpoint. The path of length one gives t in {-1,0,1}.

- If t=0, its edge is inactive. The remaining two paths form the cycle on all vertices. On a path, two inactive edges disconnect an intervening internal segment from both endpoints. Each even path with endpoint difference zero has an even number of inactive edges. Consequently neither path can have an inactive edge in a connected facet subgraph. There are A choices on the a-path and B on the b-path.
- If t=1 or t=-1, the short edge is active and joins the endpoints. An even path with odd endpoint difference must contain an odd number of inactive edges. The same internal-segment argument permits at most one, hence exactly one. On the a-path there are \(a\binom{a-1}{a/2}=aA/2\) choices; similarly there are bB/2 on the other path. For either sign, all these choices give a connected active subgraph.

The three endpoint-label cases are disjoint and exhaustive. Thus the total is

\[
AB+2\frac{aA}{2}\frac{bB}{2}=\frac{ab+2}{2}AB.
\]

Equation (1) also follows from the already published Corollary 25(iii); it is not asserted as a new facet-count formula independent of that corollary.

## 2. Correct ratios

### Even k

Take a=b=k and let C=binom(k,k/2). Equation (1) and the arithmetic expression for M give

\[
N(CB(k,k,1))=\frac{k^2+2}{2}C^2,
\qquad M(2k)=\frac{k(k+1)}{2}C^2.
\]

Therefore

\[
\boxed{\frac{N(CB(k,k,1))}{M(2k)}=\frac{k^2+2}{k(k+1)}}.
\tag{2}
\]

The published final numerator k^2+1 in this branch is incorrect. The upper bound follows from k^2+2<=k(k+1) for k>=2.

### Odd k

Take a=k+1, b=k-1, and let C=binom(k-1,(k-1)/2). Then

\[
\binom{k+1}{(k+1)/2}=\frac{4k}{k+1}C.
\]

Equation (1) yields

\[
N(CB(k+1,k-1,1))=\frac{2k(k^2+1)}{k+1}C^2,
\qquad M(2k)=2k^2C^2.
\]

Consequently

\[
\boxed{\frac{N(CB(k+1,k-1,1))}{M(2k)}=\frac{k^2+1}{k(k+1)}}.
\tag{3}
\]

The published final numerator k^2+2 in this branch is incorrect. The upper bound follows from k^2+1<=k(k+1) for k>=1, with graph-domain requirements handled separately.

The odd-k expansion in the source also writes a term k^2 F(k-1,k-1,1). Corollary 25(iii) requires instead

\[
(k^2-1)F(k,k-2,1).
\]

The same corrected ratios arise by retaining the source's M(2k-2) and M(2k-3) intermediate expressions and then applying the two appropriate parity cases of Lemma 29. In the printed proof those cases were interchanged at the last substitution.

## 3. Exact diagnostics

| k | Graph | N | M(2k) | Actual ratio | Published claimed ratio |
| --- | --- | --- | --- | --- | --- |
| 5 | CB(6,4,1) | 1560 | 1800 | 13/15 | 9/10 |
| 6 | CB(6,6,1) | 7600 | 8400 | 19/21 | 37/42 |

The integer counts were checked by `check_boundary_correction.py`, which builds each graph and enumerates edge increments in {-1,0,1}, retaining exactly the normalized labelings whose active edges span a connected graph. It does not import the F function or a discovery program. The closed arithmetic formula is compared to these independent finite counts using exact fractions. The checker also records admissible labelings rejected because their active-edge graph is disconnected.

This finite regression supports the transcription diagnosis. Equations (1)-(3) are proved for all parameters in their stated domains by the preceding argument; no finite sample is used as a universal proof. This note supplies no Lean formalization and does not resolve Conjectures 32 or 33.
