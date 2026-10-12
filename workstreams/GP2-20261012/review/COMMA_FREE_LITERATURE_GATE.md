# Four-letter comma-free codes: source gate

Checked on 2026-10-12. This file records primary sources actually inspected,
their mathematical scope, and remaining access gaps. It is not a certificate
of exhaustive novelty or of the absence of other public solutions.

## 1. Consequences for the current research

The classical rotation-orbit bound is \((m^4-m^2)/4\). It applies to ordinary
comma-free codes. The project contributes a bridge from original directed GP
sets to a stricter code class, allowing this classical bound and any valid
ordinary comma-free upper bound to be used for the GP asymptotic problem.

Ordinary comma-freeness alone is insufficient for the lower-bound bridge.
However, an ordinary four-letter comma-free code with no selected consecutive
windows is strict: among five window positions, the only three-element subset
without consecutive positions is \(\{0,2,4\}\), and comma-freeness excludes
that triple. This observation makes some classical dictionaries usable.

The ternary eighteen-word dictionary in the 1958 source is one such
dictionary. Its reversal and a direct strictness proof are documented in
`TERNARY_STRICT_CONSTRUCTION_FROM_LITERATURE.md`. Its density \(2/9\) is not
the best candidate obtainable from the inspected ordinary-code literature:
Jiggs's 1963 paper displays a 57-word dictionary over four letters and proves
that every comma-free dictionary of that size has disjoint initial and final
trigram sets. Once the displayed dictionary has been exactly transcribed and
checked, it gives a strict-code density \(57/256>2/9\). The source table must
be checked from its image, because OCR corrupts some entries. No new search
for an optimal dictionary is needed for that transfer.

No stronger asymptotic four-letter upper bound than the separately reviewed
project inequality \(182/729\) was found in the material actually read below.
This is a statement about this bounded literature check. In particular,
the fact that a 2023 article calls the exact coefficient undetermined does
not imply that no stronger upper bounds have appeared.

## 2. Primary sources with direct mathematical relevance

### Golomb, Gordon and Welch (1958)

S. W. Golomb, B. Gordon and L. R. Welch, *Comma-Free Codes*, Canadian Journal
of Mathematics 10 (1958), 202–209.

<https://doi.org/10.4153/CJM-1958-023-9>

<https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B78C35132E2BCD4A14459BE6A142FF30/S0008414X00045296a.pdf/commafree_codes.pdf>

Read: the eight-page primary PDF, especially Theorems 1, 4–7 and pages
206–208. Page 206 was also rendered and visually inspected. The printed
dictionary condition is \(a<c,\ b\ge d\); reversing the words gives
\(a\le c,\ b>d\). The paper establishes the primitive-rotation upper bound,
the existence of the fixed-length alphabet-size density limit for ordinary
comma-free codes, and a four-letter lower bound \(2/9\) from its ternary
18-word dictionary. Its half-word prefix/suffix partition is relevant to
the pair-level structure in the current upper proof. Its results do not
state the original directed Kautz GP conclusion.

### Jiggs (1963)

B. H. Jiggs, *Recent Results in Comma-Free Codes*, Canadian Journal of
Mathematics 15 (1963), 178–187.

<https://doi.org/10.4153/CJM-1963-021-1>

<https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3F80EAEA1B86983AF9CCBB3410B93FF9/S0008414X00029382a.pdf/regent_results_in_commafree_codes.pdf>

Read: the primary PDF text, including Section 2, Theorems 3 and 5, the
57-word table in Section 3, and Section 5. Theorem 5 says that for word
length and alphabet size both four, more than 56 codewords force disjoint
initial and final trigram sets. Section 3 reports the computer determination
\(W_4(4)=57\) and displays a witness. This gives the additional property
needed for a strict transfer of that witness. The asymptotics section improves
a lower bound for larger even word lengths; it does not supply the desired
new density upper bound.

### Tang, Golomb and Graham (1987)

B. Tang, S. W. Golomb and R. L. Graham, *A New Result on Comma-Free Codes
of Even Word-Length*, Canadian Journal of Mathematics 39(3) (1987), 513–526.

<https://doi.org/10.4153/CJM-1987-023-7>

<https://www.cambridge.org/core/services/aop-cambridge-core/content/view/71A7831337DAC1E7D03DF9AE4C096F08/S0008414X0000448Xa.pdf/a-new-result-on-comma-free-codes-of-even-word-length.pdf>

Read: primary PDF introduction and its main comparison-vector mechanism.
The paper studies when the primitive-orbit bound cannot be attained, using
half-word roles and comparable/compatible vectors over \(\{0,1,*\}\).
The obstruction is to representing every primitive orbit; it must not be
silently promoted to a fixed positive density loss. Page 514 confirms the
earlier value \(W_4(4)=57<60\). The publisher's 2018 online date is the
digitization date; the article is from 1987.

### Cummings (2007)

L. J. Cummings, *A Family of Comma-Free Codes with Even Word-Length*, Journal
of Combinatorial Mathematics and Combinatorial Computing 62 (2007), 171–175.

<https://combinatorialpress.com/article/jcmcc/Volume%20062/vol-062-paper%2016.pdf>

Read: the first two pages as rendered images; the PDF has no extractable
text. Theorem 1 gives a family with
\(\lfloor\sigma^2/3\rfloor^r
 (\sigma^2-\lfloor\sigma^2/3\rfloor)^{k-r}\) codewords of length \(2k\).
At length four its leading density is \(2/9\). It interlaces pairs from a
two-letter comma-free dictionary and its complement. The introductory upper
bound is the primitive-orbit bound. Its use of “maximal” for an example must
not be read as a proof of maximum cardinality.

### Fimmel, Michel, Pirot, Sereni and Strüngmann (2023)

E. Fimmel, C. J. Michel, F. Pirot, J.-S. Sereni and L. Strüngmann, *Diletter
and triletter comma-free codes over finite alphabets*, Australasian Journal
of Combinatorics 86(2) (2023), 233–270.

<https://ajc.maths.uq.edu.au/pdf/86/ajc_v86_p233.pdf>

Read: introduction, Definition 2.1, Section 3 and relevant references.
Page 236 explicitly describes the leading coefficient for even word lengths
as undetermined. Definition 2.1 distinguishes ordinary comma-free codes from
strong comma-free codes. The paper's principal exact results concern lengths
two and three, so they do not settle the four-letter strict-code density.
The earlier preprint at <https://hal.science/hal-02376793> could not be fully
opened in this session; the final primary journal PDF was available.

### Stanovnik, Moškon and Mraz (2024)

S. Stanovnik, M. Moškon and M. Mraz, *In search of maximum non-overlapping
codes*, Designs, Codes and Cryptography 92 (2024), 1299–1326; published online
2024-01-08.

<https://doi.org/10.1007/s10623-023-01344-z>

<https://link.springer.com/article/10.1007/s10623-023-01344-z>

Read: the primary full-text construction and Theorem 19. Here non-overlapping
codes are the strong comma-free/cross-bifix-free class. The exact length-four
maximum is \(r^3(q-r)\), with \(r\) nearest to \(3q/4\), ties rounded down.
Its leading coefficient is \(27/256\). This is a more restrictive class:
that upper bound cannot be applied to all strict codes or all GP sets.

## 3. Other inspected sources and explicit access limits

* Levenshtein, *Combinatorial problems motivated by comma-free codes*, Journal
  of Combinatorial Designs 12(3) (2004), 184–196; first published 2004-01-26,
  <https://doi.org/10.1002/jcd.10071>. The publisher's abstract and references
  were readable. The author-institute PDF
  <https://www.keldysh.ru/papers/2003/source/article/golomb4.pdf> was indexed,
  and portions of its introduction/asymptotic discussion were available as
  primary-source search excerpts, but direct full-text retrieval repeatedly
  failed with 502/timeout responses. Wiley PDF/EPDF retrieval also failed.
  This paper was not completely read, so it remains an access gap. Its
  institute catalog labels the manuscript as a 2003 item; the journal
  publication data above come from the publisher.
* R. A. Scholtz, *Maximal and variable word-length comma-free codes*, IEEE
  Transactions on Information Theory 15(2) (1969), 300–306,
  <https://ieeexplore.ieee.org/document/1054292/>. Metadata and references were
  readable, but the primary PDF could not be opened. No unchecked even-length
  construction is imported from this reference.
* A. L. Churchill, *Restrictions and Generalizations on Comma-Free Codes*,
  Electronic Journal of Combinatorics 16(1) (2009), R25, published 2009-02-20,
  <https://www.combinatorics.org/ojs/index.php/eljc/article/download/v16i1r25/pdf>.
  The introduction and class definitions were read. Its stronger bounds
  concern extra reflection/swap restrictions and cannot be applied to an
  arbitrary strict code.
* Donald Knuth's primary program page,
  <https://www-cs-faculty.stanford.edu/~knuth/programs.html>, and the opening
  documentation of `BACK-COMMAFREE4`,
  <https://www-cs-faculty.stanford.edu/~knuth/programs/back-commafree4.w>, were
  read. The page dates this program to September 2015; its comments explicitly
  say the five-letter search was too slow. This is a historical computation
  record, not a current certificate of openness or a reason to repeat that
  search.
* P. Majer and M. Novaga, *On the independence number of de Bruijn graphs*,
  <https://arxiv.org/abs/2604.14671>, latest version v2, 2026-06-10, with full
  text <https://arxiv.org/html/2604.14671v2>. The introduction, exact graph
  definition and variational encoding were read. Its length-four leading
  coefficient lies between \(91/240\) and \(11/28\) for the independence
  problem. Those are bounds for avoiding adjacent selected windows, a
  different problem. Its coefficient denoted \(\lambda_3\) must not be
  confused with the Kautz GP density \(\lambda_4\).

## 4. Original Kautz problem gate

The live arXiv record <https://arxiv.org/abs/2604.15909> has only version v1,
submitted 2026-04-17. The original text
<https://arxiv.org/html/2604.15909v1> was read at Definition 2.1, the Kautz
definition, Table 1 and Problem 5.2. Its alphabet-size parameter is the total
number of letters. Adjacent letters differ, shifts define directed arcs,
digons are allowed, and GP quantifies over every shortest directed path.

The author survey *The General Position Problem: A Survey*,
<https://arxiv.org/abs/2501.19385>, has latest version v5, dated 2026-08-16.
The relevant text <https://arxiv.org/html/2501.19385> was read at Sections
5.6 and 6 and its reference to the April directed paper. It continues to list
Kautz word lengths at least three among the open questions. That is a dated
statement by the survey authors, not a certification of all subsequent work.

Author publication pages and the accessible citation links were also checked,
but the external citation indexes did not provide a complete readable
network. The inspected sources did not identify a public solution of the
original four-letter directed GP problem. This bounded search does not
establish historical priority for any new project theorem.
