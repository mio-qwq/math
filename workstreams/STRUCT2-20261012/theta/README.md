# Facet maxima for bicyclic and theta graphs

The two proofs here resolve the length-weighted mixed-parity obstruction
in Braun--Bruegge's
[*Facets of Symmetric Edge Polytopes for Graphs with Few Edges*](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf),
*Journal of Integer Sequences* **26** (2023), Article 23.7.2.
All graphs are finite, connected and simple.

## Global \(n\)-vertex, \(n+1\)-edge maximum

For odd \(s\ge3\), put \(h(s)=s\binom{s-1}{(s-1)/2}\). For \(k\ge3\),
define

\[
W(k)=
\begin{cases}
h(k-1)h(k+1),&k\text{ even},\\
h(k)^2,&k\text{ odd},
\end{cases}
\qquad M(2k-1)=W(k),\quad M(2k)=2W(k).
\]

The [bicyclic proof](PROOF.md) establishes

\[
\max_{\substack{|V(G)|=n\\|E(G)|=n+1}}N(G)=M(n)\qquad(n\ge5),
\]

and strictly \(N(\Theta(a,b,c))<M(n)\) for every legal theta on
\(n\ge5\) vertices. Here \(\Theta(a,b,c)=\mathrm{CB}(a,b,c)\) has
positive path lengths summing to \(n+1\), with at most one length 1.
This proves original Conjecture 32 and, with the graph reduction,
Conjecture 13 on the range where Definition 12 describes genuine
simple comparison graphs.

The equality block data are also explicit. At odd order the two odd
cycles have balanced lengths and meet in one vertex. At even order the
same balanced odd cycle lengths are accompanied by one bridge; the
bridge may connect two disjoint cycles, or be a pendant edge attached
to a wedge of the cycles. Thus the even-order global maximum need not
have a unique graph isomorphism class.

The new bound controls both terms of the original exact count

\[
N(\Theta(x,y,z))
=zT(x,y,z-1)+xyT(x-1,y-1,z),
\]

where \(x,y\) share parity, \(z\) has opposite parity, and

\[
T(a,b,c)=\sum_t B_a(t)B_b(t)B_c(t),\qquad
B_m(t)=\binom m{(m+t)/2}
\]

with the usual parity and range zeros, including \(B_0(t)=1[t=0]\).
A central-binomial envelope retains the total length of the other two
rows while accounting for the external coefficients \(z\) and \(xy\).
The argument is derived directly from facet labels, so length-one paths
are justified without importing a positive-row transfer theorem at a
zero argument.

## Exact maximum within the theta class

The later [maximizer proof](MAXIMIZERS.md) establishes a unique maximizing
unordered triple for every \(n\ge4\):

| Order | \(k\) parity | Unique triple |
|---|---|---|
| \(n=2k-1\) | even | \((k-1,k-1,2)\) |
| \(n=2k-1\) | odd | \((k,k-2,2)\) |
| \(n=2k\) | even | \((k,k,1)\) |
| \(n=2k\) | odd | \((k+1,k-1,1)\) |

It proves Conjecture 33 and extends its original \(n\ge10\) range.
Mixed parity admits a strict compression to length 1 or 2 in the path
of exceptional parity. An exact comparison then strictly improves any
unbalanced remaining pair. Explicit mixed-parity competitors exclude
all same-parity triples. Section 8 gives four exact maximum values
and their ratios to \(M(n)\).

The original Proposition 30 contains transposed constants in its two
even-order ratio displays and an error in one earlier \(F\)-term.
The [source correction](literature/PROPOSITION30_CORRECTION.md) gives
the correct formulas and its independently executed graph checks.
These errors do not invalidate that proposition's inequality conclusion.

## Small graph domain

At \(n=3\) the simple \(n+1\)-edge class is empty. At \(n=4\) its sole
graph is \(K_4-e=\Theta(1,2,2)\), with exactly 12 facets.
The original Definition 12 formally mentions an undefined \(C_1\)
at these orders. We state the small case directly; numerical \(M(4)=12\)
is an explicitly identified extension of the binomial expression, not
an invented graph convention. Duplicate length-one paths are never
treated as distinct edges.

## Source and verification map

- [Source gate](literature/SOURCE_GATE.md): JIS original, Braun--Bruegge
  arXiv versions, Mori--Mori--Ohsugi follow-up and its journal metadata,
  and later-work/erratum searches. The follow-up's complete-join results
  do not supply these mixed-theta bounds. Its journal full text was
  not retrieved, so a word-for-word journal comparison is not claimed.
- [Bound review](independent/BOUND_REVIEW.md) and
  [final source receipt](independent/FINAL_SOURCE_REVIEW.json):
  separate-agent mathematical review of the complete global proof,
  binding SHA256
  `81f7c5f4326828b16a34204e1a84b3dec136ea1d61c30cfb60b17e6395616655`.
- [Actual facet checker](independent/check_actual_facets.py):
  constructs the graph and enumerates integer vertex labels via a
  spanning tree, then checks all original edge inequalities and connected
  saturation. Multiple spanning trees yield identical normalized label
  sets. This counting method does not use the binomial formula as oracle.
- The `maximizers_review/` and `scalar_checks/` directories record
  the exact maximizer's separate mathematical review and finite
  original-formula regression. Source SHA256 is
  `c0c02847ae525260d65dd5b11c1ee940b4b63aec6e2167c39fa8a9c12fc12fab`.

The geometric bound and exact maximizer are written mathematical results.
Finite computations, auxiliary formalization, literature coverage, and
human peer review are not interchangeable. No full Lean proof or
historical-priority certification is claimed.
