# Derivation and review provenance

This record distinguishes discovering-agent self-checks from independent implementation and later mutual review.

## Before review of other implementations

The discovering agent derived the uniform special-bit formula, the fixed-first-word prefix formula, and the positive-bit range independently of the project's `verification/` implementation. It wrote `experiments/exact_signed.py` and completed the full original-input enumeration run at `2026-10-11T07:19:45.171399+00:00`.

At the time those checks and all three proof documents were completed, the discovering agent had not read any code, result, or proof in `verification/`, and had not read the root agent's general dynamic-programming implementation. The discovering agent's source directly computes the original modular additions; its closed-form predictions and direct enumeration nevertheless belong to one research implementation and are labeled self-checks.

## Boundary of mutual mathematical review

The root agent reported that an independent verifier had already completed blind derivation and exhaustive checks before the verifier was invited to read `special_bit_signed_correlation.md`. The discovering agent has not itself inspected the verifier's implementation or report. Any claim about independent verification must cite that separate report, not merely this message history.

By `2026-10-11 07:23:31 UTC`, the discovering agent had begun reviewing the root agent's proposed general elimination argument **as stated in collaboration messages**, after finishing the three proof documents above. It confirmed the middle-carry marginalization, removal of unused rotated output bits, and the sufficiency of a four-state borrow/carry transfer process. It emphasized phase insertion before processing each bit, cancellation of duplicate boundary phases, and summation over all final states. This is mutual mathematical review, not a second blind discovery of the root agent's algorithm. No root implementation source had been read at that checkpoint.

The later fixed-word sign classification is a continuation of the discovering agent's own fixed-word formula. Its triangle-area implementation imports the earlier discovering implementation for cross-checking, so the two algorithms are not labeled independent verification.

After the sign-check run completed at `2026-10-11T07:26:31.336316+00:00`, the discovering agent read the root-level `GENERAL_REDUCTION.md` mathematical document and found it consistent with the elimination argument already reviewed in messages. It still had not read the corresponding `tooling/` source or the independent verifier's source. The audit found the stated four-state recurrence, pre-transition phase convention, coincident-index handling, unconstrained terminal sum, and arithmetic/bit-operation bounds mathematically consistent with the specified model.

## Originality boundary

The exact local correlations, conditional formulas, and algorithms are not assigned an originality level here. The independent literature review has identified predecessor coverage of constituent carry-sum lemmas and general exact ARX methods. The small elementary moment `M0` is not presented as a new lemma. Full-text comparison with near predecessors remains necessary before claiming a new result, an attack improvement, or publication value.
