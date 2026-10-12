# SHA-256 message-expansion distance — reservation

Owner: CRYPTO2-20261011-7f3c. Date: 2026-10-12 UTC.
Role: independent research; no independent review yet.
Local baseline: 0967246290572a4aadd4574627395e8187adc046.
Remote baseline: 7144a9245827c4cd1f45449e0776e46f2599f6fb.

Claim recorded before computation: determine rigorous lower bounds for
the number of unequal words in the **actual nonlinear, 32-bit, 64-word
SHA-256 message expansion**, over every distinct pair of 16-word inputs.
This is a self-defined precise research target motivated by the original
message-expansion literature, not a numbered public conjecture.

Let E be FIPS 180-4 Section 6.2.2 message expansion. Define
d64=min_{M != M'} #{0<=t<64 : E(M)_t != E(M')_t}.
The ultimate deliverable is an exact value or a demonstrably improved
bound on d64, with universal proof and real message-pair witnesses when
claiming sharpness. No padding restriction is imposed; a universal lower
bound on all blocks would also hold on any padded subset.

First attempt: derive the necessary support constraints from injectivity
of sigma0 and sigma1, compute the minimum of that relaxation by exact
finite-state dynamic programming, then test whether equality can actually
lift to word values. A relaxation witness is not a pair of SHA messages.
Try bit-level consequences only if they strictly strengthen the support
bound. Stop if this only recovers existing truncated-differential machinery
or does not constrain meaningful differential characteristics.

Difference from prior members: SHA-256 integer additions and its message
recurrence, full 64-word support distance; no APN objects, no Sidon-period
mechanism, no Keccak folding/padding/energy, no ChaCha correlation work.
No shared public result number. Only this owner's directory is writable.

Current evidence: source gate in CANDIDATES.md, exact definitions from
FIPS; no numerical minimum computed at reservation time. No attack,
complexity improvement, original theorem or resolved conjecture claimed.
Next: exact injectivity certificates and support recurrence; then decide
whether this route yields more than an already known necessary condition.

## Computed checkpoint

The exact support relaxation minimum is 13. A complete integer potential
certificate proves the same universal lower bound for the actual expansion.
PROOF.md supplies the reduction and telescoping argument; check.py validates
all inequalities and inverse columns with standard-library arithmetic.
RUNS.json records deterministic regeneration and five negative controls.
This is not an actual minimum proof or an attack. Originality is unconfirmed.
For one optimal support, a zero-base lifting contradiction is proved; a
general-base query returned unknown after 20 seconds. Current blocker:
global carry compatibility. Next action/stopping rule: HANDOFF.md.
