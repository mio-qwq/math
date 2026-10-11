# General exact counting and cross-checks

The mathematical derivation is [GENERAL_REDUCTION.md](../GENERAL_REDUCTION.md). `exact_dp.py` computes the signed correlation of one output bit of the **three-addition** local word program, with either four independent uniform inputs or a fixed first word and three independent uniform inputs. It supports every bit and rotation in `[0,n)`, including zero rotations and wraparound. It does not search keys or attack a service.

## Commands

Run from this project directory:

```sh
python tooling/exact_dp.py --n 32 --r 16 --q 12 --bit 28
python tooling/exact_dp.py --n 32 --r 16 --q 12 --bit 28 --fixed-a 0x61707865
python tooling/exact_dp.py --check --standard-table --output tooling/results/dp_all_bits.json
python tooling/cross_check_standard.py
```

The `--check` mode reads previously generated exact input counts in `verification/independent_word_counts.jsonl` and `experiments/results/exact_signed_max5.json`. To regenerate those first, use their documented commands. No random generator, external Python package, floating-point probability computation, or solver is required by this directory. Floats in the JSON are display conveniences only; all checks use exact integer counts and reduced rational numbers.

## Observed run

The general check/table command ran on 2026-10-11 07:25:28 UTC and completed with actual exit code **0**, empty stderr, and program elapsed time about **0.608 seconds**. The outer process receipt is `results/dp_execution.json`; the complete output is `results/dp_all_bits.json`. This is an environment-specific duration, not a claimed asymptotic speedup over literature.

The run made these exact comparisons:

| Evidence source | Comparisons |
|---|---:|
| Independent original-word counts, n=3..5, all rotations | 50 parameter sets / 216 bit values |
| Discovering implementation's original-word counts at fixed a | 248 conditional values |
| Closed expressions at additional widths through n=64 | 105 values |
| n=1 carry-free boundary | 3 values |
| Rejection of invalid parameters | 6 cases |

The separately written verifier later produced standard 32-bit results without reading this implementation. `cross_check_standard.py` compares its uniform model and four ChaCha constants, all 32 output bits, against this program: **160 exact rational comparisons**. Its receipt is `results/standard_comparison.json`; an outer execution receipt records the real exit code. The fixed `a=0` standard table is deliberately excluded from that comparison because it was not in the verifier's standard output. It has separate closed-form and finite-input support.

## Critical invariants

Carry phases are evaluated before the corresponding bit transition. Repeated borrow indices cancel by XOR. All terminal states are accepted. The fixed-word model changes both the subtraction rule and the normalization; it cannot be substituted by the uniform-word table. Omission of surviving Walsh terms is incorrect in general. These invariants are established in the derivation and exercised by independent original-word enumeration.

The state method and arbitrary-precision counting are established techniques. This implementation and its exact local values have not demonstrated a new best attack or cleared originality review.
