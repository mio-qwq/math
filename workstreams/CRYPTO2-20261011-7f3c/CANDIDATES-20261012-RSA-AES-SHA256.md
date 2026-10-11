# Significant standard-primitive research gate

Date: 2026-10-12 Asia/Singapore (2026-10-11 UTC).
User explicitly prioritizes substantial results about major cryptographic
problems, with RSA/AES/SHA-256 as examples, over small local results bearing
a famous algorithm name. No breakthrough is promised by selecting a target.
Visible CRYPTO head remains 551fcd7; coordination remains abd8e85. Its survey
mentions these primitives but does not reserve the precise target below.
All earlier exclusions remain binding. Existing own Ascon/RD artifacts stay
frozen; this priority change supersedes their proposed immediate next work.

## 1. RSA: remove the short-relation root-recovery heuristic — selected

Original obstacle: Boneh–Durfee, IEEE TIT 46(4), 1339–1349 (2000), DOI
10.1109/18.850673, small-private-exponent attack. More explicit public
question: Miller–Narayanan–Venkatesan, *Coppersmith's lattices and focus
groups: an attack on small-exponent RSA*, arXiv:1708.09445v3, 2020-12-16,
Introduction Q2 and Section 2. Q2 asks whether algebraic dependence creates
a barrier before the norm/determinant bound is reached. The exact latest
HTML was fetched; the older author-hosted and v2 PDFs were not conflated
with that revision. Sources:

- https://arxiv.org/html/1708.09445v3
- https://crypto.stanford.edu/~dabo/pubs/abstracts/lowRSAexp.html
- https://eprint.iacr.org/2024/1331 (Feng–Liu–Nitaj–Pan; full text's Assumption
  1 explicitly requires a zero-dimensional ideal; current landing 2024-08-25).

Long-term quantified target: for every fixed epsilon>0, every sufficiently
large N=pq with q<p<2q, and valid 1<e<phi(N), ed=1 mod phi(N), d less than
N^(1-1/sqrt(2)-epsilon), recover the factors from N,e in polynomial time in
log N, without a zero-dimensionality or resultant assumption. Any restricted
class, extra leakage, prime-e assumption or resource growing with N must be
identified; none is silently promoted to this target. The first useful aim
is a genuinely nontrivial sufficient recovery condition or a rigorous
obstruction for the specified short-relation method. Linear independence,
algebraic functional independence, coprimality and a zero-dimensional ideal
are distinct notions and will not be conflated.

Follow-up gate: Herrmann–May PKC 2010's full text gives a simpler determinant
analysis, not a demonstrated solution of the general dependence issue;
2024/1331 still states its heuristic. Jimenez Urroz arXiv:2606.24717v2
(2026-06-24), full HTML inspected, obtains an unconditional continued-fraction
result WITH partial information on p+q. It does not remove this hypothesis
from ordinary small-d RSA. Boneh's author abstract and Narayanan's homepage
were checked; a complete coauthor/errata audit remains unfinished. Standard
public code mentioned by the source is https://github.com/mimoo/RSA-and-LLL-attacks;
no code has been imported, copied or executed at reservation. Bauer–Joux
EUROCRYPT 2007 and Bauer's thesis remain essential full-text comparison gaps.
The search found no general resolution, which is not proof of current openness.

Precise falsifier: a valid RSA family plus exact lattice/shortness certificates
violating a precisely stated recovery condition. Failure of one LLL run,
or a determinant bound alone, would not refute RSA insecurity at that exponent.
Direct verification: exact integer lattice membership, scaled norm bounds,
polynomial identities/gcds/resultants and actual modular key equation.
First attempts: distinguish removable common factors from an actual recovery
obstruction; combine a common component with the original RSA congruence;
test whether a dimension/height argument forces recoverable components.
Stop a branch of this route if it merely reproves Wiener, needs an unproved
independence assumption, or is a textbook resultant trick with no new range.

This concerns integer small-root geometry in RSA, wholly separate from the
team's APN/Sidon, ChaCha, fixed SHA3 and own Ascon probability work. It targets
a significant proof gap; it is not a claim about conventional e=65537 keys
having small d, nor a general RSA factorization breakthrough.

## 2. SHA-256: improve the actual collision frontier — deferred at gate

Source: Zhang–Li–Gao–Wang, *Collision Attacks on SHA-256 up to 37 Steps with
Improved Trail Search*, EUROCRYPT 2026, ePrint 2026/232 (received 2026-02-12).
Full extracted paper read for Table 1, Sections 3/5/6. It reports two-block,
standard collision analysis for 37 steps, including time exponent 119.1 and
memory exponent 39.9 in its model; these are paper claims, not our executions.
Its explicitly labelled further challenges concern SHA-512, so we do not
misquote that paragraph as a numbered SHA-256 open conjecture.

Our possible target, if selected, would be an algorithm producing distinct
properly padded messages with equal SHA-256 output for at least 38 steps,
standard IV, success probability >=1/2, and expected total work below the
appropriate 256-bit birthday benchmark, including all trail realization,
message modification and preprocessing. An improvement at 37 steps must
compare time/data/memory within exactly the same model. This is our adopted
research objective, not a printed universally quantified source conjecture.

New local-collision automation and precise Boolean conditions are already
covered by that paper. Source code is publicly linked at
https://github.com/Zhang-SDU/AutoSHA2Collision ; the link was checked in the
paper, but source and complete follow-up/code audit are not yet done. No
independent new mechanism has been identified. Direct witnesses can be
verified by two independent standard compression implementations; upper
complexity claims also need a valid probability/cost analysis. Stop before
an expensive solver search if it simply follows their construction/order.
Different from the excluded SHA3 model, but currently below the method gate.

## 3. AES: reduce a meaningful single-key attack cost — deferred at gate

Source: Bao–Guo–List–Wang, *The Cross-ratio Property and Its Use for
Cryptanalysis of Round-reduced AES*, ePrint 2026/1549, current landing
inspected. It already gives cross-ratio matching improvements for seven-round
AES-128 and a multiple-quartet structural switch. The full PDF request failed
403, so its detailed attack table and all assumptions have not been audited.
This source presents advances and motivations, not a named universal open
conjecture that we can honestly reproduce here.

Potential quantified target would be a single secret-key recovery algorithm
for a fixed >=7-round AES-128 instance, success >=1/2 over uniform key,
with an explicit chosen-plaintext budget and total time/preprocessing/memory
strictly improving a verified same-model reference point. Correctness must
include key-schedule consistency and false-candidate rates. Standard AES
encryption and exact field equations can verify local certificates, but
local identities alone are insufficient to prove that attack goal.

A precise reference resource tuple has not yet passed the full-text gate.
Recent cross-ratio coverage makes casually repackaging inverse-S-box geometry
especially risky; no external code/construction sequence is adopted. Stop
unless a distinct mechanism can change the actual attack cost. Objects and
targets differ from all reserved team projects. For now choose RSA Q2,
whose central mathematical obstacle is explicit and available in full text.
