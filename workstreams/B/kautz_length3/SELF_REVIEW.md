# Personal review and actual execution receipt

B personally derived and checked the proof. This is NOT independent peer review. No new agent was opened; no Lean or optimization certificate is claimed.

Exact scope: arXiv:2604.15909v1 Problem5.2, ONLY Ka(m,3) for all integersm>=3. Formula gp=m(m-1)(2m-1)/6. It gives a positive universal solution to this slice; the source's observed values are credited and not relabeled as new numerical discoveries. Other word lengths and exact permutation values remain unresolved by this proof.

Actual command: `python workstreams/B/kautz_length3/verify.py` from repository root. Python3.12.14, Linux, standard library only. Result PASS, complete output verify.log.

- Original graph rebuilt from all ordered pairs of valid words, with only the last-symbol exclusion for arcs; actual BFS distances, not a presumed closed formula.
- 247508 ordered distance-formula checks;93848 separate alphabet-restriction/isometry comparisons.
- 250744 local geodesic checks covering the injection and all four selected-arc cases throughm=8.
- 599734 unordered selected triples in the explicit lower-bound sets form=3..8, with all ordered geodesic tests performed.
- Exhaustive base: all4096 subsets of Ka(3,3),219GP sets, maximum5. The human proof also supplies a noncomputational base case.
- Restricted m=4 injection check:32768 subsets of the15 words containing0 but not starting0;1832GP sets, maximum9. Together with base checks,3296 injection tests.
- Three definition/range controls: adding a word to a fixed lower-bound set creates a rejected geodesic triple; m=2 hasGP2 and rejects the false sum-of-squares extension; the arc010->101 is legal here and would be wrongly removed by the permutation-graph rule.

Primary mathematical checks:
1. In the missing-first-letter lemma, every exceptional map E_ab->(a,a) requires selected M_ba; this excludes M_aa and every other E_ac with the same first letter. This makes the diagonal images injective and disjoint from the off-diagonal images.
2. The selected-arc case partition is exhaustive, including repeated endpoint letters. The three-cycle case counts the sole first-a word and sole last-a word separately, subtracting two distinct absent middle-a words.
3. The digon case bounds a-letter incidence by(m-2)^2+2, valid against(m-1)^2 only whenm>=3. The excluded m=2 genuinely fails the theorem.
4. Deleting an alphabet letter preserves original distances, not merely induced adjacency. Induction is used only whenm-1>=3; the m=3 argument is explicitly separate.
5. No assumed general upper bound, independence=GP assertion, empirical extrapolation, or numerical solver is used in the proof. The equivalence of the two maxima follows from the completed proof rather than being assumed.

Discovery note: SciPy1.17.0/milp availability was checked during planning, but no MILP call was run. The analytical injection resolved the intended test before numerical optimization became necessary. Two earlier tiny feasibility snippets on m=3 were not treated as new results; the final standalone checker supersedes them reproducibly.

Post-candidate literature/source check: original and Augustsurvey primary pages still present k>=3 as open; exact Kautz/general-position/squares/formula/erratum searches found no later same-scope resolution. Search also surfaced an older paper with “Independence Number” in the title (Deng–Xu2008, DOI10.1016/j.dam.2008.01.009); its reported(l,omega)-independence terminology must not be conflated with GP or ordinary independence, and no full-text review is claimed. The elementary independent-set count here is not asserted historically new. Full prior-art and human responsibility review remain pending.
