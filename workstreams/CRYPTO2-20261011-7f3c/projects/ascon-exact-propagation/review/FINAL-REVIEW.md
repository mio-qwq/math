# Final independent mathematical review: two-round Ascon propagation

## Exact reviewed versions

This review binds the actual bytes of the following project-root files. The original theorem and three-column extension were read in full. Any later content change requires a new version binding.

| File | SHA256 |
| --- | --- |
| `PROOF.md` | `ce579b13525fa7545d8f9daafa34e84703d5fe219254a1b6c862b5b3761fbeae` |
| `EXTENSION.md` | `9c92f88ceef42efee7eae246b7aea7c05358a1e415501ce66abb4885b21deacd` |
| `discover.py` | `4ed1377b243e41d38dd1b717a2b6677bfcc319cccc774ff862a67d2b83b1feac` |
| `check.py` | `322f2d56022946d4393cce0bd77e20215647b5ade6f5cbfa40a617db35edce4a` |
| `rank-certificate.json` | `1fa22e22f070f0daca753968cefd5eaec6672201af895f2dde5551004409e01e` |
| `mismatch-certificate.json` | `2e49a999a4f533f8219ea2ec0daab1847dce9f5b09bd4a69f75ed180288f1e09` |
| `impossible-certificate.json` | `097399f7ca473eff787fab6e26383a10c447b16ab313ed7a73b1e075acc2e48e` |
| `discover_triples.py` | `ee6b25862725e62c0c850dcaa5242436e91fee8ac27fb9c9f0330c8aa34460da` |
| `check_triples.py` | `a64af9933b9a311803c17f48c99075ae4bf3d81f2dbb3f9561bd5db5ccada58a` |
| `triple-rank-certificate.json` | `26d354c01d9a2d231d5ffa3c2d31d957cc7a7790dcf5518863ca5c31b49765b2` |
| `triple-formula-certificate.json` | `a1d61f0776b49ec0ee4ce03b2ae05c2afdd8b9d9e4837cc5c51f1a5c33c3951c` |

## Verdict and accepted scope

**PASS for both the original theorem and the completed three-column extension, at the exact versions hashed above.** I found no mathematical gap or missing assumption within the explicitly stated uniform-full-state, fixed-difference, two-round model.

The accepted original statement is: for every fixed input difference A supported on at most two 5-bit columns, every fixed B,C, and every fixed pair of additive constants, the actual joint probability of the two specified S-layer transitions equals the local-DDT product.

The accepted extension is: among the 41664 three-column supports, exactly the 320 translates of `{0,a_l,b_l}`, for the five actual Ascon lane rotation pairs, admit some paths with a product error. All other 41344 supports have exact products for every choice of differences and constants. For every three-column path, `0 <= P <= 2M`; both endpoints are attained with M positive. The stated one-character correction formula is valid, and the five doubled-support families `{0,2a_l,2b_l}` have a vanishing correction despite deficient projection rank.

“Exactly 320” classifies supports on which universal validity fails. It does not claim that every path on those supports has a product error. No historical originality, attack, or external peer-review certification is attached to this PASS.

## Independence record

Before disclosure, I read the original NIST standard, independently transcribed its coordinate-polynomial S-box, checked all 32 table values, derived the conditional-uniformity proof, and checked the complete one-/two-column rank geometry. I also checked all 1953 normalized triples, obtaining 30 deficient cases, and independently constructed both zero-probability and positive factor-two three-column witnesses.

The sealed pre-disclosure note has SHA256:

`5cbd5629726d347bb5a358fd9621b88527a14c31ececfe0a233d0fd737457669`.

Its independently written computational artifacts were sealed as follows:

| Pre-disclosure artifact | SHA256 |
| --- | --- |
| `independent_probe.py` | `12b8654297197ed7f429fe25c2c38329a560e6a631f61c5e22d4bd6f145c52e7` |
| `independent_projection_results.json` | `ad6181d93e6c47d880ddbdf9b936193fb66eb56018e76a4d6544f0885e53cd76` |
| `independent_witness.py` | `e1611c5c4e85ca6d087fa33c7d342d1cbfd10f1c8f9cbecade2706fc3a5b0d3e` |
| `independent_witness_results.json` | `2f8f9ec6d4bae368e77bcbd12d9f0efb80cb29cca9e413bc03747616458f931b` |

All these hashes were rechecked after disclosure and remain unchanged. The initial independence is relative to the discoverer's artifacts; the task's candidate statement and the original standard were available. The subsequent ten-orbit classification and doubled-orbit refinement were proposed by the discoverer and then independently assessed, not independently discovered by me before disclosure.

The root checker is a separate implementation by the discoverer; it is not alone the independent mathematical review. My pre-disclosure reconstruction and polynomial-based code provide that additional separation. No 2026/358 cryptanalytic implementation was read or imported. No subagents were spawned for this task. All reviewer writes were confined to this `review` directory, with no Git-ref or parent-file modifications.

## Original-standard, event, and quantifier audit

Primary source: NIST SP 800-232, August 2025, Section 3, especially Section 3.2, equation (7), Table 6, and equations (8)–(12):

https://doi.org/10.6028/NIST.SP.800-232

https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-232.pdf

The five rotation pairs in the proof and programs match the standard. I checked the source row-incidence convention against direct physical right rotations on all 320 word-bit basis vectors. The root files encode lane l as bit `2^l`; my independent code uses the standard table's opposite 5-bit display order. Explicit five-bit reversal reconciles the two encodings. All 32 values of the discoverer's circuit, the checker's reversed NIST table, and my coordinate-polynomial implementation agree under this conversion.

The event in `PROOF.md` is the conjunction of the specified first S-layer difference B and second S-layer difference C, with the actual paired computation in both rounds. It correctly fixes the second input difference to LB on the first event. The final diffusion maps C to LC deterministically. The constants `f0,e1` are correctly identified as the **first two rounds of Ascon-p[12]**; they are not being identified as the constants of the separately defined two-round Ascon-p[2] instance. The universal theorem allows any fixed additive constants and therefore covers either selection when its constants are inserted correctly.

The mathematical hypotheses that matter are explicit:

* X is uniform over the whole 320-bit state space; there is no fixed-key initialization subspace or other state restriction.
* A,B,C are fixed differences, not values adaptively selected from X.
* Both members of the pair use the same fixed round constants.
* “Active column” means a nonzero 5-bit column of A, regardless of its bit weight.
* The path fixes the intermediate B. An endpoint differential instead sums these mutually exclusive paths over B.

The proofs do not silently assume a Markov property or an affine first output fiber. Empty first or second transition fibers are separately assigned probability zero. The empty input support is correctly trivial. Cyclic translation is applied to linear ranks, while constants remain arbitrary affine offsets; no rotation invariance of a specific constant is assumed.

## Original theorem: proof and full-width count

Conditioning on the first event constrains only the initially active output columns Y_I. Since the actual S-box is a permutation, the other output columns remain jointly uniform and independent of those constrained values. The free-column projection onto a superset of the second active columns is onto in all one-/two-column geometries. Consequently the relevant second inputs are jointly uniform after conditioning, and multiplying local DDT probabilities is exact.

The original certificate's 64 normalized supports and all 320 lane ranks match my pre-disclosure results exactly. This covers every physical support of size one or two by translation, and every possible choice of differences by using the value-independent envelope. It is a complete finite matrix-rank component of the proof, not statistical sampling or bounded testing of selected differences. It is specific to the 64-bit rotation geometry.

For the discoverer's three-column witnesses, I independently recomputed the first fibers, second difference, projection ranks, and local second-input sets from my polynomial S-box after converting the column encoding. The results are:

| Witness | Actual joint probability | Local-DDT product |
| --- | --- | --- |
| `mismatch-certificate.json` | `2^-54` | `2^-55` |
| `impossible-certificate.json` | `0` | `2^-55` |

The counts refer to the full `2^320` sample space. There are 16 first-fiber tuples on three columns. Outside those columns there are 305 free bits, and the relevant derivative system has free-variable rank 43. Thus each accepted tuple represents exactly `2^(305-43)=2^262` states; accepting all 16 gives `2^266` states and probability `2^-54`. The impossible fixture accepts none. Equivalently, the value projection has 85 target bits, rank 84, and precisely one fixed coordinate. Its rank 84 and the derivative-system rank 43 concern different maps and are not contradictory.

The fixed coordinate is lane 2, position 0. Its value includes the low bit of `e1`; it is not a constant-free shortcut. As a further independent check, changing only that bit, `e1 -> e0`, swaps these two actual results while leaving both local-DDT products unchanged. The first constant is absorbed by translating the uniform initial state. My own pre-disclosure witnesses have different probabilities (`0` or `2^-65`, versus product `2^-66`) because they use different local differences; they independently corroborate the same mechanism.

Section 5's general conditioning identity is also valid within its stated two-S-layer scope. I checked all 1024 input/difference pairs against the affine derivative representation used by the analyzer. Eliminating the free variables leaves consistency conditions on exact first output fibers, without assuming those fibers affine; the factor `2^(-5|I|-r_Z)` and accepted-tuple count are correct. This is a generic exact linear-algebra reduction, not by itself a new algorithmic-complexity result.

## Three-column extension: classification, formula, and doubled supports

I independently matched all 9765 triple-rank claims against my own row construction. The 30 normalized deficient cases are exactly the ten proposed translation orbits, each deficient in only the stated lane by one bit. The explicit masks t are supported in the envelope and satisfy `L^T t` equal to the three source bits on I. I independently checked these identities on every normalized exceptional case.

For fixed constrained values Y_I, rank codimension one and that explicit annihilator imply that the free projection is uniform on exactly one affine hyperplane. Averaging its parity over the independent first fibers gives the density

`2^(-5|J|) [1 + eta * beta_F * (-1)^(<t,z>)]`.

Summing over the product of the second transition fibers yields precisely

`P = M (1 + eta * beta_F * beta_G)`.

The treatment of M=0 avoids empty-fiber division. When the second difference and output difference at a coordinate are both zero, its fiber is the full 32-element set; it is not omitted if it lies in the parity support. This is necessary for the cancellation argument. Since both biases lie in [-1,1], the factor-two bound is immediate and applies to every three-column support, with the full-rank cases giving equality.

The refinement from ten deficient-rank orbits to five actual-error orbits is correct. I separately checked the complete influence table for the doubled supports. First output fibers are stable under adding B_i, so a nonzero lane-l bias forces `(B_i)_l=0`. For lanes 0,2,3,4, the listed parity coordinate then has alpha_j=0 and hence a balanced second fiber. For lane 1, the only possible nonzero alpha at the listed coordinate is the root encoding's 8. I checked the identity `D_8 S(z)=D_8 S(z xor 6)` for all 32 inputs via my independently implemented NIST polynomials, with explicit encoding conversion. The translation flips lane 1 and pairs all solutions in each second fiber. Therefore `beta_F*beta_G=0` in every doubled family, for all differences and constants.

To check that none of the five undoubled families can be removed, I independently constructed a positive factor-two witness for every lane before reading the final extension artifacts; these are recorded in `independent_k2_k1_results.json`. I also recomputed all 20 disclosed formula fixtures from my polynomial implementation. Every fixture matches, with exactly two per lane and scale. The undoubled examples have nonzero correction, whereas all doubled examples are exact. Translating a nonzero-correction witness preserves both bias magnitudes; an arbitrary fixed constant changes only the sign eta. Thus every translated undoubled support fails universal exactness, although particular paths on it can still be exact.

The cardinalities are correct: the ten rank-exception orbits have 640 supports; the five actual-error orbits have 320. A three-element support has no nontrivial translation stabilizer in a cyclic group of order 64. Hence there are `41664-320=41344` universally exact three-column supports.

## Checkers, negative controls, and reproducibility

I executed both frozen root checkers read-only. The original checker passed 320 rank blocks, both exact witness probabilities, and seven negative controls. These controls reject an altered rank, a missing support case, replacing each claimed actual probability by the nominal product, an altered pinned constant, an out-of-range column value, and a nonzero output difference at an inactive second column.

The triple checker passed 9765 rank blocks, 20 formula fixtures, all 37 doubled-cancellation checks, and four negative controls: an altered rank, a missing triple, an invalid family scale, and a false corrected probability. Its output agrees with the independently recomputed classification and 320-support refinement. The character-density proof, rather than the 20 fixtures alone, establishes the quantified formula.

The original checker's acceptance contract does not validate every analyzer bookkeeping field in the JSON. I therefore separately checked the recorded derivative ranks, accepted-tuple counts, fiber sizes, residual constraints, and active columns against the reviewed analyzer; all matched. These metadata checks supplement, rather than replace, the independent table/projection count. Neither checker is being claimed as a general-purpose adversarial JSON validator or a proof assistant.

To verify executable reproducibility without modifying parent artifacts, I ran copies of the two discovery entry points under `review/reproduction`. All five generated certificate files were byte-for-byte identical to their reviewed parent files, as confirmed by SHA256. The added impossible-certificate generation in `discover.py` reproduces the original impossible fixture exactly. No large state-space enumeration or sampling was used.

Post-disclosure audit sources and outputs are `audit_opened.py`, `opened_audit_results.json`, `independent_triple_audit.py`, `independent_triple_classification.json`, `independent_k2_k1.py`, `independent_k2_k1_results.json`, `audit_extension.py`, and `extension_audit_results.json`.

## Consequences, source scope, and limitations

Summing exact joint paths over B legitimately gives exact two-round endpoint differential distributions for the universally exact support classes. Any fixed linear functional of those distributions is therefore also exact under the same full DDT composition. Summing the nonnegative path inequality gives the stated factor-two endpoint upper bound for arbitrary three-column inputs. A relative factor-two bound for signed differential-linear sums does not follow because of cancellation; the extension correctly says so. A zero-probability path does not by itself make the endpoint differential impossible.

This review does not certify historical originality. The general conditional-uniformity argument, GF(2) rank criterion, character-density calculation, and free-variable elimination are ordinary mathematical tools and can overlap existing diffusion-independence theory. Their independent reconstruction here is evidence of correctness, not evidence of priority. The parent is investigating additional relevant prior work, including ePrint 2025/179 and 2023/725; I have not independently audited those papers in this review and make no claim that they do or do not already cover any concrete result. Any later novelty statement must be supported by that separate source analysis.

The accepted results concern a fixed, complete 320-bit permutation model with uniform inputs and exactly two rounds. They do not establish arbitrary-round approximation accuracy, validate every further columnwise approximation in another program, give fixed-key chosen-plaintext attack probabilities, or change a standardized Ascon AEAD security bound. No Lean/formal proof or external referee acceptance is certified.

**Final disposition:** accept the written mathematical statements, finite rank classifications, exact formulas, and supplied full-width probability certificates at the hashes recorded above. No mathematical correction is required within this scope. Historical novelty remains unconfirmed.
