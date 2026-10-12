# Distinguishing adjacent vertices by one global edge order

This package contains a complete written proof of Gorzkowska–Kwaśny Conjecture 10 from *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1. [Original paper](https://arxiv.org/html/2609.11832v1).

For every finite connected simple graph G other than K2 or an even cycle, and **every given proper edge colouring**, there is **one total order of all edges** such that the complete lists of incident colours differ across every edge. The colouring is fixed throughout. The new regular construction covers every d≥3 and every proper colouring using exactly d colours, including disconnected graphs. The original authors' **Theorem 5** supplies the unequal-palette case; this dependence is explicitly attributed.

Read `DE_WERRA_SHORT_PROOF.md` for the concise derivation, `ALL_DEGREES_THEOREM.md` for the original elementary construction, and `GLOBALLY_BALANCED_TWO_PARTITIONS.md` for the self-contained selection tool. The latter is a **classical de Werra corollary**: both set partitions have discrepancy at most one in every block, and the total red size is exactly floor(|X|/2). It is not a new mathematical theorem. The Eulerian proof preserves labelled parallel incidence edges and includes singletons and the empty set.

The general constructor also gives an exact obstruction classification for fixed proper colourings on possibly disconnected simple graphs: a valid order exists precisely when no component is K2 or an even cycle coloured with exactly two colours. Isolated vertices are harmless; even cycles with at least three colours can be ordered.

The full mathematical chain was independently reconstructed by an AI reviewer on 10 October 2026. A separate 12 October AI review checked the new short derivation, balancing proof, strict certificate source and bounded original-definition controls. These are written mathematical/source reviews with real small executable checks; they are not peer review, a historical-firstness guarantee or a complete Lean formalization. No full Lean compilation or axiom audit is provided, and this package has not been submitted as a separate paper.

## Reproduce the fixed certificate

Use Python 3.12 or later, standard library only, from this directory:

```text
python code/verify_euler_certificate_json.py code/demo_k6_certificate.json
```

Expected output is `PASS PASS exact certified construction and endpoint sequences`. The JSON verifier imports only the strict checker, which independently reconstructs the input graph, the auxiliary certificate and the exact construction before checking every endpoint list. Its certificate format covers nonempty simple d-regular graphs with d≥3 and exactly d fixed colours; it is not a certificate format for every general graph.

For a new witness from the supplied K6 input:

```text
python code/issue_euler_certificate.py code/demo_k6.json > proof.json
python code/verify_euler_certificate_json.py proof.json
```

`code/construct_full_graph.py` accepts `{ "n": n, "edges": [[u,v,colour], ...] }` and uses the original authors' unequal-palette construction or the regular construction component by component. Integer and string colours are supported; vertices are numbered 0,…,n−1. Its exact finite validation and error conditions are separate from the universal written proof.

Program source bytes are unchanged from the frozen branch. Large historical worker enumeration counts are recorded only as worker results and were not independently rerun for this integration. `VERIFICATION.json` states the actual independent checks and the fresh-path K6 replay. `provenance.json` pins original hashes, earlier mathematical review objects and fixed GitHub source links. Indexed-adjacency linear-time arguments in the mathematics should not be confused with worst-case bounds for the current Python dictionary/sort implementation.
