# Independent A-research review packet · 2026-10-10

This package contains exact executable code and mathematical source from
`mio-qwq/math`, `partner/dist-A`. The initial full Conjecture 10 proof remains
frozen at commit `7168f6df66ba5518cd3420c4668eab5352e4be8c` and already
has ROOT's independently written mathematical PASS. The *new strict executable*
and *new condensed de Werra-based presentation* have **not** inherited that
review, nor are they a Lean proof, signed priority release or journal paper.

## Three distinct activities

1. **Strict witness certification:** `check_euler_order_certificate_strict.py`
   validates the entire root/cycle/insertion mechanism AND the original
   endpoint list inequalities without importing a generator. Existing loose
   verification checks only whether the final order works; a valid but
   rearranged order can pass that check while failing exact proof-provenance.
2. **Portable JSON proof:** `issue_euler_certificate.py` emits a complete
   JSON witness from a correctly d-coloured simple d-regular input. The
   independent `verify_euler_certificate_json.py` checks that witness using
   only the strict verifier and stdlib. The K6 example includes both the
   original input and a fixed issued proof.
3. **Classical balanced partition corollary:** paired odd-degree vertices in
   the bipartite incidence multigraph and Euler orientation give red/blue
   discrepancy ≤1 at all original blocks AND overall exactly floor(n/2)
   red. This is NOT novel: it is de Werra's strongly equitable 2-edge
   colouring of bipartite multigraphs (see book by A. Frank, Thm. 2.4.22,
   and de Werra, Discrete Mathematics 14 (1976), 133–138). The new code is
   an explicit separately checked implementation, not new priority.

## Run (Python 3.13.5, only standard library)

From the extracted directory:

```bash
python3 workstreams/A/code/verify_strict_euler_certificates.py
python3 workstreams/A/code/issue_euler_certificate.py workstreams/A/code/demo_k6.json > proof.json
python3 workstreams/A/code/verify_euler_certificate_json.py proof.json
python3 workstreams/A/code/verify_euler_certificate_json.py workstreams/A/code/demo_k6_certificate.json
python3 workstreams/A/code/verify_global_balanced_partitions.py
```

Original expected stdout contains 5598 exact 5-regular input cases,
588 independently sampled larger regular instances, 9 rejected damaged
certificates, 44169 exhaustive pairs of small set partitions, 2738 larger
pairs, and 100000-element balancing; demo JSON validates. 

`MANIFEST.json` records the SHA256 AND canonical Git blob SHA of each
shipped file. The ZIP was tested after extraction in an **entirely new**
temporary directory; every file hash and all commands passed. These finite
checks do not prove an all-order or all-graph theorem: proofs are the original
frozen full Conjecture10 theorem, the independently sourced shorter proof,
and classical de Werra's equitable graph edge-colouring.

## Open acceptance gates

ROOT still needs to independently inspect this new strict software packet,
new short proof wording and de Werra citation, and newer executable HOLD
status; neither worker testing nor ZIP extraction is ROOT's sign-off.
A real Lean toolchain remains unavailable in this runtime; no Lean theorem,
compiler log, or axiom audit has been fabricated. No merge, new project ID,
automation, paper submission or external author contact was carried out.
