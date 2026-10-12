# Independent review: a positive gap below one quarter

Date: 2026-10-12. Status: independent written verification passed. The proof
below is reconstructed from the code definition. No numerical optimization,
asymptotic error term, or Lean compilation is used.

## 1. Scope and statement

Let \(A\) be an alphabet of cardinality \(m\ge1\). A set \(C\subseteq A^4\)
is an ordinary comma-free code when, for every \(u,v\in C\), none of the
four-letter windows of \(uv\) starting at \(1,2,3\) belongs to \(C\).
The words \(u,v\) need not be distinct.

We independently verify the universal bound

\[
 \boxed{|C|\le\left\lfloor\frac{182m^4}{729}\right\rfloor.} \tag{1}
\]

In particular it holds for the strict codes whose every length-eight word
has at most two selected window occurrences. Thus the reviewed repair theorem
gives

\[
 \operatorname{gp}(\operatorname{Ka}(m,4))
 \le\left\lfloor\frac{182m^4}{729}\right\rfloor+73m^3,
 \qquad
 \lambda_4\le\frac{182}{729}<\frac14. \tag{2}
\]

This is a mathematical verification, not a claim that (1) is historically
new. The natural scope of (1) includes ordinary comma-free codes, not only
the stricter class used by the Kautz repair theorem.

## 2. A three-level labeling of ordered pairs

Build a digraph \(H\) on vertex set \(A^2\). Put an arc \(ab\to cd\) exactly
when \(abcd\in C\).

There is no directed walk of length three in \(H\). Indeed, such a walk
would have the form

\[
 ab\longrightarrow cd\longrightarrow ef\longrightarrow gh.
\]

Then \(abcd,cdef,efgh\in C\). In the concatenation \((abcd)(efgh)\), the
window at position two is \(cdef\), contradicting comma-freeness. This
argument permits repeated pair vertices or repeated arcs. The absence of a
three-edge **walk**, rather than merely a simple path, is essential.

For every \(z\in A^2\), let \(\ell(z)\) be the maximum length of a directed
walk ending at \(z\), including the length-zero walk. This maximum exists
and belongs to \(\{0,1,2\}\). If \(z\to z'\), appending this arc to a
longest walk ending at \(z\) proves

\[
 \ell(z)<\ell(z'). \tag{3}
\]

In particular, equal levels at \(ab\) and \(cd\) exclude both codewords
\(abcd\) and \(cdab\).

## 3. An empty-orbit event

Let \(a,b,c,d\) be four independent uniform letters of \(A\), with
replacement. Let \(f\) be the indicator of \(C\), and write

\[
 R=f(abcd)+f(bcda)+f(cdab)+f(dabc).
\]

Always \(R\le1\). To see this, if two rotational occurrences are selected,
choose one selected rotation \(u\) as a base. The other is \(\rho^j(u)\)
for some \(1\le j\le3\), and it is the interior window of \(uu\) starting
at \(j\), contradicting comma-freeness. The argument also excludes periodic
words: different positions are still counted even if the words coincide.

Define the event

\[
 E=\{\ell(ab)=\ell(cd),\ \ell(bc)=\ell(da)\}.
\]

On \(E\), equation (3) excludes each of the four summands of \(R\). Therefore,
pointwise,

\[
 R\le1-{\bf1}_E.
\]

Every rotation of an independent uniform four-tuple has the same
distribution. Putting \(p=|C|/m^4\), expectation gives

\[
 4p\le1-\Pr(E). \tag{4}
\]

No distinct-letter assumption is made, and collisions create no error term.

## 4. Nine kernels and two Cauchy–Schwarz inequalities

For \(i,j\in\{0,1,2\}\), define

\[
 K_{ij}(x,y)={\bf1}_{\{\ell(xy)=i,\ \ell(yx)=j\}}.
\]

These nine indicator kernels partition \(A\times A\):
\(\sum_{i,j}K_{ij}(x,y)=1\) for every ordered pair.

If all four cross pairs

\[
 (a,b),\ (a,d),\ (c,b),\ (c,d)
\]

belong to one kernel \(K_{ij}\), then
\(\ell(ab)=\ell(cd)=i\) and \(\ell(bc)=\ell(da)=j\). Thus this
monochromatic rectangle event implies \(E\). For different \((i,j)\),
these rectangle events are mutually exclusive, since the color of \((a,b)\)
already determines \((i,j)\).

For any kernel \(K\), put

\[
 t_4(K)=\mathbb E_{a,b,c,d}
          K(a,b)K(a,d)K(c,b)K(c,d),\qquad
 \mu(K)=\mathbb E_{a,b}K(a,b).
\]

To justify the required inequality without any external theorem, let
\(h(a,c)=\mathbb E_b K(a,b)K(c,b)\) and
\(r(b)=\mathbb E_a K(a,b)\). Independence of \(b,d\), followed by two
applications of Cauchy–Schwarz, gives

\[
\begin{aligned}
 t_4(K)
 &=\mathbb E_{a,c}h(a,c)^2\\
 &\ge\bigl(\mathbb E_{a,c}h(a,c)\bigr)^2\\
 &=\bigl(\mathbb E_b r(b)^2\bigr)^2\\
 &\ge\bigl(\mathbb E_b r(b)\bigr)^4
  =\mu(K)^4.
\end{aligned} \tag{5}
\]

The left and right variables range over independent copies of the same
alphabet. There is no requirement to partition the alphabet into disjoint
left and right parts, and hence no loss from such a partition.

Let \(\mu_{ij}=\mu(K_{ij})\). By disjointness of the rectangle events, (5),
and convexity of \(x^4\),

\[
\begin{aligned}
 \Pr(E)
 &\ge\sum_{i,j}t_4(K_{ij})\\
 &\ge\sum_{i,j}\mu_{ij}^4\\
 &\ge9\left(\frac{\sum_{i,j}\mu_{ij}}9\right)^4
  =\frac1{729}.
\end{aligned} \tag{6}
\]

Combining (4) and (6),

\[
 p\le\frac{1-1/729}{4}=\frac{182}{729},
\]

which proves (1).

## 5. Why the reverse-pair coordinate is necessary

The kernel color must record both \(\ell(xy)\) and \(\ell(yx)\). A
monochromatic rectangle for only the three colors \(\ell(xy)\) need not
imply \(E\).

For example, take four distinct letters \(a,b,c,d\), assign level zero to
every ordered pair except \(da\), and assign level one to \(da\). Then all
four cross pairs \(ab,ad,cb,cd\) have level zero. Nevertheless
\(\ell(bc)=0\ne1=\ell(da)\), so \(E\) fails. This is a negative control
for that tempting but invalid substitution in the kernel step. It is not a
claimed labeling produced by a particular GP set; it shows that the proposed
universal event implication with one-coordinate colors is false.

## 6. Bridge and remaining scope

The repair theorem used in (2) is reviewed in
`review/INDEPENDENT_REPAIR_REVIEW.md`. Its precise source is
`construction/STRICT_WINDOW_REPAIR.md`, SHA256
`56ed0af016042abcbca256b52f6fb7539edb908fe81d6ba585a21102f9c4c4f5`.
It deletes at most \(73m^3\) vertices from any original GP set to obtain a
strict code. Strictness implies ordinary comma-freeness, so (1) applies to
that code. This supplies all quantifier changes needed in (2).

The classical bound \((m^4-m^2)/4\) remains separately valid and may be
smaller than (1) for some finite alphabets. The point of (1) is its uniform
positive density gap \(1/4-182/729=1/2916\), which persists as \(m\to\infty\).

This review establishes neither an exact strict-code density nor an exact
ordinary comma-free density. It does not certify historical priority.
The three-symbol lower construction, whose discoverer wrote a separate
note, must be independently reviewed separately; its verification is not
being inferred from the upper-bound argument here.
