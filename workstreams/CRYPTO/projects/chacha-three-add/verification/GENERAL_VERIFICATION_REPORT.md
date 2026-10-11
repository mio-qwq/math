# Independent verification: arbitrary output bits and a fixed first word

Date: 2026-10-11. Verdict: **all stated identities and finite comparisons passed**.

## Independence and scope

The discovery agent supplied a mathematical candidate and the proposed pair of state variables. This verifier wrote its own Python signed-count dynamic program and a separate C++ direct word enumerator. It did not read discovery `experiments/` or `tooling/`. The latter implementation and its output had not been read by this verifier when these files were generated. The root agent may subsequently compare the separately generated outputs.

The endpoint discovery manuscript was read only after the earlier blind endpoint proof and word enumeration were complete. Its written-proof cross-review is recorded separately in `DISCOVERY_ENDPOINT_PROOF_REVIEW.md`.

The verified quantity is signed `E[(-1)^bit_i(w XOR L)]`, for the three-addition local function in `GENERAL_INDEPENDENT_PROOF.md`. This report covers uniform `a,b,c,d`, or a fixed `a=A` with the other three words independent uniform. At the standard parameters, `w` is also exactly the first output word of a complete ChaCha quarter round: all operations after the third addition change only `b,c,d`. The same observation holds for the first output word of the fully XOR-linearized quarter round. Thus these are exact one-bit linear correlations of that first output word. The joint output distribution, the other output words, several rounds, and fixed secret-key distributions are not established here; no ChaCha20 attack follows from the calculation alone.

## Evidence

| Comparison | Parameters | Exact comparisons | Result |
|---|---|---:|---|
| New four-state evaluator versus earlier blind direct word enumeration | `n=3,4,5`, every `r,q` in `[0,n)`, every output bit | 50 parameter groups, 216 bit values | All equal |
| Fixed-word evaluator versus newly written direct word enumeration | `n=1,2,3,4`, every `A`, every rotation pair, every output bit | 346 parameter groups, 1,274 bit values | All equal |
| Same fixed-word check restricted to requested range | `n=2,3,4` | 344 parameter groups, 1,272 bit values | All equal |
| Averaged conditional direct counts versus uniform evaluator | `n=1,2,3,4`, all rotation pairs and bits | 100 bit values | All equal |
| Arbitrary-bit evaluator versus previously independently proved endpoint fraction | `(n,r,q,i)=(32,16,12,28)` | One exact rational equality | Equal |
| Standard-rotation exact spectra | `(n,r,q)=(32,16,12)`, uniform `a` plus four standard constants | 160 exact rational values | Produced |

The newly executed C++ program enumerated 1,086,480 `(A,b,c,d,r,q,n)` cases. Its control flow consists only of the original additions, XORs, rotations, and signed output-bit counting; it does not use transformed random variables or carry states. The earlier uniform C++ count file is reused without modification. At `n=3,4`, averaging the new conditional counts also reconstructs previously tested uniform domains using separate word-enumerator code.

All rotations, including zero rotations and wrapping rotation sums, were included. All bits, including bit zero, coincident borrow boundaries, and cases with no surviving Walsh terms, were included. No mismatch was found in these finite domains. General validity rests on the written proof, not on extrapolating this finite evidence.

## Explicit negative controls

| Deliberately incorrect interpretation or simplification | Counterexample | Correct value | Incorrect value |
|---|---|---:|---:|
| Taking absolute correlation | `n=3,r=1,q=1,i=2` | `-3/16` | `3/16` |
| Calling probability bias the correlation | Same parameters | `Cor=-3/16` | Bias is `-3/32` |
| Dropping the Walsh correction terms after middle-carry elimination | `n=3,r=0,q=1,i=2` | `-1/16` | `0` |
| Using the uniform-first-word result when `a` is fixed | `n=2,r=q=0,i=1,A=0` | `1/2` | `1/4` |
| Using the non-wrapping endpoint closed form at a wrapped endpoint | `n=3,r=1,q=2,i=0` | `1/2` | `-3/16` |

These are deliberate controls. They are not claims about errors in a particular published paper.

## Standard 32-bit exact values

The file `general_standard32_exact.json` stores the complete spectra, as signed reduced rational numbers with integer numerators and denominators. Decimal approximations are presentation fields only. At bit 28:

| Distribution of first word | Signed correlation |
|---|---|
| Uniform | `-47180567524833621/1180591620717411303424` |
| `A=0x61707865` | `-5014914159307157/295147905179352825856` |
| `A=0x3320646e` | `-20742118815994171/590295810358705651712` |
| `A=0x79622d32` | `-36166661545322725/590295810358705651712` |
| `A=0x6b206574` | `-14797957587093615/295147905179352825856` |

These values condition only the first word. The other words retain the explicitly stated uniform distribution. They must not be interpreted as a full cipher or fixed secret-key correlation. The official full quarter-round left-rotation convention and RFC 8439 Section 2.1.1 known-answer vector were independently checked in the preceding blind verification; see `independent_word_counts.jsonl` and `VERIFICATION_REPORT.md`.

## Reproduction and environment

Run from any directory:

```sh
python /workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add/verification/general_independent_verify.py
```

The runner compiles `general_fixed_word_enumerator.cpp`, executes it, stores raw signed counts, checks them with the separately implemented exact evaluator, and generates the standard spectra and a provenance record. It removes the generated executable after the run. The recorded run exited zero. The compiler invocation used `-O3 -std=c++17 -Wall -Wextra -Werror`; compilation and enumeration emitted no stderr. All finite tests are exhaustive, and no pseudorandom sampling or seed was used.

Environment: Python 3.12.14, GCC 13.3.0, Linux x86_64 with glibc 2.39. Exact command arguments, exit codes, elapsed times, input/source SHA-256 hashes, every comparison result, and the generated spectrum hash are in `general_independent_run.json`.

The proof establishes a direct cost of `O(n^2)` signed-integer operations for an individual output bit with four state counts per moment, and `O(n^3)` such operations for independently computing every bit. This is a cost for evaluating the specified local statistic, not an attack complexity or a claimed improvement over published exact ARX evaluation methods.

## Claim status

- The proposed arbitrary-bit elimination identity has an independently reconstructed ordinary mathematical proof.
- The proposed fixed-first-word adaptation has an independently reconstructed ordinary mathematical proof.
- Separate direct word enumeration and signed-state evaluation agree on the full declared finite domains.
- Standard 32-bit spectra are exact recurrence outputs, supported by the proof and finite implementation checks.
- Novelty, superiority to prior exact ARX algorithms, and publication value have not been established by this verification work.
- This is internal agent verification, not human peer review or formal proof-assistant verification.

No discovery implementation was imported, no file outside the assigned verification directory was modified, and this verification agent made no Git commit or external submission.
