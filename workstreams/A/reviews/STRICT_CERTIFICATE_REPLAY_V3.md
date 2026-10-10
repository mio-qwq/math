# Agent A — strict proof-certificate and classical-prior-art replay (2026-10-10)

This is a NEW worker-owned review object and not a replacement for the
complete Conjecture 10 original mathematical freeze at
`7168f6df66ba5518cd3420c4668eab5352e4be8c`, which ROOT has already
independently accepted in WRITTEN mathematics. This new executable, short
de Werra presentation and source provenance need separate independent review.

## Exact GitHub branch and source identities

Branch: `mio-qwq/math` `partner/dist-A`.
Source checkpoint HEAD before this receipt: `5b9191b965165717ad5081c91241f2575e4efc9d`.
The following critical Git blobs have been re-fetched and exactly match the
freshly executed files:

- `code/check_euler_order_certificate_strict.py`:
  `4d3bde472761ea171bc78d664ed19a545c1d4f9b`
- `code/verify_strict_euler_certificates.py`:
  `aca9653ca407a845f46dd7c8991e8878badfac03`
- `code/issue_euler_certificate.py`:
  `ac98d5c1cf046c43394604e888bf06659b67bfa7`
- `code/verify_euler_certificate_json.py`:
  `f3969227c21bdfad7194a4fdca0073c2e9cf1979`
- `code/global_balanced_partitions.py`:
  `901f80296d25b3e7b0ad0cdbf85bf5908969a85a`
- `code/verify_global_balanced_partitions.py`:
  `b9f123805d0895e06b9cce24eb35ec88d9ea7dee`
- `paper/DE_WERRA_SHORT_PROOF.md`:
  `de98e22dbb2886b992e9147c4508edc4a8bfbfd9`
- `proof/GLOBALLY_BALANCED_TWO_PARTITIONS.md`:
  `09662f3d5dc399813a3f972b7e2860b14a2085c5`

All **18** files in the portable packet, including frozen dependencies,
demo input, demo proof, README and the sources above, had their exact
canonical Git blob IDs checked against remote GitHub objects.

## Portable independent replay

Artifact:
`/mnt/data/agent_A_strict_certificate_and_dewerra_20261010.zip`

- File size: **33,320 bytes**
- ZIP SHA256: `acbf0a73a930a733a0c3facd540c6d3b197647320886d1da97dbd82a98578c56`
- Contains a `MANIFEST.json` with all source blob/sha256 identities and byte sizes.
- Actually extracted to a NEW temporary directory and run there under
  **Python 3.13.5**, standard library only, no network or Lean.

Commands from extracted package root:

    python3 workstreams/A/code/verify_strict_euler_certificates.py
    python3 workstreams/A/code/verify_global_balanced_partitions.py
    python3 workstreams/A/code/issue_euler_certificate.py workstreams/A/code/demo_k6.json > proof.json
    python3 workstreams/A/code/verify_euler_certificate_json.py proof.json
    python3 workstreams/A/code/verify_euler_certificate_json.py workstreams/A/code/demo_k6_certificate.json

Actual output, all return code **0**:
- **5,598** complete fixed-eight-vertex d=5 factor/matching witnesses, now checked by an independent **structural** checker.
- **588** additional seeded regular input/colouring witnesses across n=4,...,16.
- **9** deliberately damaged or **non-certified** witnesses rejected. One
  swapped-edge example still satisfies all original endpoint inequalities
  and was accepted by the OLD loose checker, but it violates the claimed
  insertion order and is rejected by the NEW checker.
- **44,169** complete small two-partition pairs with global red count
  exactly floor(|X|/2) and block discrepancy <=1; plus **2,738** larger seeded
  inputs and a **100,000-element** stress case with exactly **50,000** red.
- K6 standalone JSON proof is valid under the independent verifier, and
  a deliberately corrupted K6 proof exits **nonzero**.

Separate 1,000-vertex regular graphs, with d=3,5,9,31, were also
constructed and independently checked from the literal original edge order.
Those are *finite scalability examples*, not evidence of the infinite
conjecture without the mathematical proof.

## Mathematical scope and originality

**Complete Conjecture 10:** the original paper is A. Gorzkowska and
J. Kwaśny, *Distinguishing adjacent vertices by ordering edges*,
arXiv:2609.11832v1 (2026). Their unequal-palette Theorem 5 is imported
with explicit attribution. The A full regular ordering proof has a
specified independent written mathematical PASS at original freeze.

**Balanced two-partition theorem:** exact global half-size plus local
discrepancy <=1 is a special case of the CLASSICAL strongly equitable
2-edge-colouring theorem for bipartite multigraphs of **D. de Werra**
(1970s; see *An extension of bipartite multigraphs*, Discrete Mathematics
14 (1976), 133–138, DOI 10.1016/0012-365X(76)90056-X, and
A. Frank, *Connections in Combinatorial Optimization*, Theorem 2.4.22).
Neither A's derivation nor its executable should be advertised as
a new first mathematical theorem.

The NEW short proof `paper/DE_WERRA_SHORT_PROOF.md` attributes de Werra
for root selection and retains A's nontrivial, actual single-edge-order
insertion and endpoint verification. This alternative draft is
**not** yet independently accepted, despite earlier acceptance of the
separate original full proof.

## Core remaining work

- ROOT independent source/logic review of the NEW strict certificate
  checker and de Werra-based short proof; do not infer review from tests.
- Original v2 execution HOLD is a separately tracked issue; the corrected
  worker replay was submitted earlier. Do NOT claim ROOT has lifted HOLD
  unless a newer coordinating card says so.
- Actual Lean theorem: neither this certificate package nor the draft
  `HallBridge.lean` is an accepted/compiled proof. Pinned Mathlib already
  supplies finite Hall's marriage theorem; formalize the two-partition
  cardinal argument and then root ordering and single global edge list,
  recording true compiler/axiom receipts.
- Recheck follow-up literature before any historical-priority statement;
  no submission, author contact, new project number, PR merge or scheduled
  background task has been made.
