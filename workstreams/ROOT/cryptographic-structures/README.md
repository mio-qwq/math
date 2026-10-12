# Cryptographic structure results: written proofs and exact certificates

This packet integrates two completed written results and their minimal exact-checking inputs. It does not contain a Lean formalization, a complete cipher attack, an improved security bound, or a claim of historical priority. Original scholars cited in the proofs retain their attribution. No human author identity is assigned by this integration.

| Result | Accepted mathematical scope | Limits |
|---|---|---|
| [Circulant related differentials](circulant/PROOF.md) | Every invertible circulant matrix of order n>=3 over every characteristic-two field has a nonzero unequal related-differential pair. Periodic restriction preserves invertibility; its branch-number inequality implies MDS inheritance. | Order 2 has genuine MDS exceptions. Arbitrary singular matrices and other characteristics are outside the theorem. No attack cost follows. |
| [Two-round Ascon propagation](ascon/PROOF.md), [three-column classification](ascon/EXTENSION.md) | Uniform full 320-bit state and fixed differences/constants. Inputs with at most two active 5-bit columns have exact local-DDT products. Of 41664 three-column supports, 41344 are universally exact; precisely 320 can admit errors. Every three-column path satisfies 0<=P<=2M with the stated exact correction. | The 640 deficient-rank supports are distinct from the 320 actual-error supports. A zero-probability path need not make its endpoint differential impossible. No full AEAD or fixed-key initialization conclusion is asserted. |

The supplied Ascon positive and zero witnesses use the first two constants of p[12], f0/e1. They are not described as the constants of p[2]. The nominal product is 2^-55; their actual path probabilities are 2^-54 and zero. The circulant fixture is a fixed 10-by-10 matrix with a directly checked related pair and quotient lift. Its historical all-minor MDS verification is recorded in the original source; this integration does not repeat that enumeration.

Run from the repository root with Python's standard library:

```sh
python -B workstreams/ROOT/cryptographic-structures/circulant/check.py workstreams/ROOT/cryptographic-structures/circulant/certificates/mds10.json --negative
python -B workstreams/ROOT/cryptographic-structures/ascon/check.py
python -B workstreams/ROOT/cryptographic-structures/ascon/check_triples.py
```

These check the supplied certificates and the complete small rank classification; they do not perform discovery searches or enumerate 2^320 states. The symbolic proofs establish the quantified statements. Exact transformed bytes, original paths and frozen links are in [provenance.json](provenance.json). Actual local execution and independent AI-review boundaries are in [VERIFICATION.json](VERIFICATION.json). AI-assisted review is separate from human peer review and proof-assistant checking. Historical originality remains unconfirmed.

| Other existing work | Current disposition |
|---|---|
| ChaCha | [Frozen local-correlation results](https://github.com/mio-qwq/math/blob/551fcd76ebabe43971123d29d11a94319a3b0096/workstreams/CRYPTO/projects/chacha-three-add/RESULTS.md). L0 exact local-model baseline; originality is not cleared. No full ChaCha20 attack or best-attack improvement. The larger workstream is not copied here. |
| RSA | [Frozen restricted proof candidates](https://github.com/mio-qwq/math/blob/7144a9245827c4cd1f45449e0776e46f2599f6fb/workstreams/CRYPTO2-20261011-7f3c/projects/rsa-short-relations/GENERAL-PROOF-v1.md). HOLD for final exact-version mathematical review and originality. Conditional recovery requires a supplied sufficiently short relation; relation existence and positive-y shifts are missing. The original MNV Q2 and an improved attack exponent are not solved. |
| Keccak | [Frozen target and source qualification](https://github.com/mio-qwq/math/blob/551fcd76ebabe43971123d29d11a94319a3b0096/workstreams/CRYPTO/projects/keccak-conditional-rank/OBJECTIVE.md). No new result or global projection bound; the full instance still awaits independent reconstruction. |

Primary definitions are [RFC 8439](https://www.rfc-editor.org/rfc/rfc8439.html#section-2.1), [NIST SP 800-232](https://doi.org/10.6028/NIST.SP.800-232), and [Kumar–Yadav–Samanta 2605.27535v1](https://arxiv.org/html/2605.27535v1). The circulant source describes its remaining direction informally; this packet does not invent a numbered conjecture.
