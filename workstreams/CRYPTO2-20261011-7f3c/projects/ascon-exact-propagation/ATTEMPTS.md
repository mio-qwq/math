# Attempts, corrections and limits

1. Treating all first-layer output fibers as affine was rejected. Ascon's
   quadratic forward S-box makes derivative INPUT fibers affine; applying
   the S-box can produce non-affine size-eight OUTPUT fibers. The proof
   uses the exact finite output sets and never makes this assumption.
2. An early discovery implementation transported the second-round constant
   through L as if it were added before diffusion. It belongs after L.
   This interchanged an early zero/factor-two interpretation. Before any
   freeze, the equation was corrected to q=C+D_alpha S(c1), and both the
   direct-table checker and independent reviewer verified the final two
   fixtures. The reviewer additionally flipped e1 to e0 and observed the
   two actual probabilities interchange. No erroneous early claim is frozen
   as a valid certificate. Original scratch output is not a proof receipt.
3. A first bounded triple-family scout incorrectly demanded a non-unit
   ratio from every rank-deficient family. It exhausted 200 candidates for
   lane 0, doubled support, and exited 1 with ('no examples',0,2). The
   immediately following check exited 1 because the formula certificate
   was not generated. These were development failures, not successful runs.
   The failure prompted the proof in EXTENSION Section 3: all five doubled
   support families cancel exactly. The revised scout tests equality there
   and seeks non-unit witnesses only in the five actual exception families.
4. A patch application failed on an unmatched documentation context before
   writing; it was corrected. No certificate depends on that failed action.
5. Direct PDF retrievals sometimes returned 403 or no full text. Source
   extraction hashes are hashes of tool-extracted UTF-8 text, not of the
   publishers' PDF bytes. Source gaps and dated landing revisions are in
   SOURCE-GATE.md. Originality is not inferred from failed retrieval.

Not covered: four or more active input columns, third and later rounds,
fixed-IV/key/nonce distributions in full AEAD initialization, efficiency
of summing all intermediate trails, higher-order differences, actual attack
complexity or signed-DL relative error bounds. Counts are exact over the
full 320-bit uniform domain, not Monte Carlo extrapolations.

Stop/recovery rules: fill the closest literature gaps before enlarging this
into a novelty claim. Do not grow samples of already certified two/three-
column cases. A useful next step must either connect the exact correction
to a specified existing approximation or handle an explicitly constrained
input distribution with a useful bound. Generic character identities alone
are insufficient reason to keep the route open.
