# Result checkpoint — 2026-10-11

**Complete affirmative written theorem; independent mathematical review PASS.
No Lean, journal acceptance, historical-firstness or new attack claim.**

For every characteristic-two field K and every invertible n-by-n circulant
M, n>=3, there are nonzero unequal u,v with

    u_i v_i(u_i+v_i)=0,
    (Mu)_i(Mv)_i((Mu)_i+(Mv)_i)=0    for every i.

This completes the invertible/MDS remaining-order direction indicated in
Kumar–Yadav–Samanta, arXiv:2605.27535v1, Section VI, beyond Theorem 5's
n not congruent to ±2 modulo 12. That direction is unnumbered and informal;
we do not invent a numbered conjecture. n=2 has real MDS exceptions.

The key step is explicit: if d divides n, group the first-column entries
by residue modulo d and repeat d-coordinate inputs. The smaller circulant
intertwines with the original and remains invertible. Related differences
lift. Taking d=n/2 covers n≡2 mod4, n>2, using the known odd-order result.
Moreover, with t=n/d, branch numbers obey

    beta(B) >= ceil(beta(M)/t).

Thus MDS also descends; the original MDS-scope proof requires only the
known odd-MDS case plus this lift. Full proof: **PROOF-v2.md**.

## Evidence, with roles separated

1. Discoverer wrote the complete universal proof. An independent agent first
   reconstructed it from the original sources and sealed PRE-DISCLOSURE.md
   before reading the discoverer's proof. Its full review is in review/.
2. Discoverer's constructor/checker separation: row elimination versus
   direct products/column elimination, different finite-field multiplication
   algorithms; 3,710 exact witnesses passed. This is NOT by itself an
   independent-agent review. Complete windows and sampled windows are
   separately listed in REGRESSION.json.
3. A concrete 10-by-10 circulant MDS matrix over GF(2^16), modulus
   x^16+x^12+x^3+x+1, has an explicit related pair in certificates/mds10.json.
   All 184,755 nonempty square minors were verified nonzero by both the
   C++ elimination search and a separate Python division-free Laplace
   recurrence. This verifies a real instance in a formerly uncovered order,
   not only a non-MDS or vacuous example. It is a test fixture, not an
   optimized diffusion-layer design.
4. For the n=2 GF(4) MDS boundary, all 210 ordered nonzero unequal input
   pairs fail the RD requirement. Corrupted output, zero/equal vector,
   wrong matrix/quotient/lift, reducible field and invalid-element controls
   were rejected. Exact commands, exit codes and hashes are in RUNS.json.
5. No finite sample proves the theorem; the proof is the complete linear
   algebra argument. No comparison against an attack-complexity record is
   made, because no actual attack is constructed.

## Correction history

The immutable v1 proof contained a misleading parenthetical suggesting MDS
could fail to descend. Its main theorem did not depend on that suggestion.
The discoverer subsequently derived MDS descent; the independent reviewer
confirmed it and explicitly corrected its own similar wording. V1 and its
initial review remain preserved; PROOF-v2.md and review/ADDENDUM.md are
authoritative. This is a genuine recorded correction, not silently rewritten
history. The source-gate candidate warning about not assuming quotient MDS
is superseded in the MDS-input specialization by the proved descent lemma.

## Significance and remaining limits

This removes the dimension restriction for invertible circulant diffusion
matrices in the inspected source. The contribution is a short structural
completion built on attributed earlier results. Its novelty and importance
need broader scholarly assessment, with explicit full-text gaps in
SOURCE-GATE.md. It does not break AES, alter SHA3 security, or cover arbitrary
singular matrices or odd-characteristic fields. The next useful work is
resolving those literature gaps, not growing the completed sample set.
