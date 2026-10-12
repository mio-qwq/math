# Independent AI acceptance of the exact support12-v4 ceiling

**ACCEPT, exact frozen version.** For each specified support 12,6,7,13,
every actual SHA-256 schedule pair has common nonzero difference D
with **v2(D)<=18**. This improves the earlier necessary ceiling 20.
No entire support is excluded, the global word-distance lower bound
remains 13, and no pair attaining 13 is supplied.

The accepted author manifest is SHA256
`3f8fab844410d88aebc26afed62a186553e9127b4196424d334be6831698acdc`.
The accepted proof, checker, and certificate hashes are respectively

    b74ae3ed3fc09d5aa6f8ac1e8b0e2a0ec76015722db3b031ae1416de52d8cffd
    b159cb1a0190bc9d85062b30415ef55461b098ee2c6bf9ce522e7e5b34a55fff
    1763fbb3256509c4d2b7503eb143c7527d09231237b539221ed826c3320fec2c

These receipts must not be silently reused after any reviewed bytes
change. `REVIEW_RECEIPT.json` binds the complete author manifest and
independent files.

The reviewer independently rebuilt the original recurrence bridge,
the complete v>=19 width reduction, both third-pair signs, and a
different finite carry model using 96 actual base-input bits. That
checker and its seven-case run predate the first author-file read.
The complete model exhausts all 89,243 triples of exact carry masks,
with no satisfiable branch. It includes k=4 and needs no old valuation
bound as a premise. The low input bits and bit31 wraparound remain
arbitrary; sigma0 is used only as an XOR-linear map on input masks.

The written author proof and checker were then read and compared.
All 17 artifact hashes, the positive input cubes, 3389 mask-pair
indices, 32 third masks, 512 direct XOR receipts, and 28 written
recurrence combinations pass the independent checks. The reviewer
did not import or execute any author checker/generator. The author's
particular search edge/conflict counts remain author replay statistics;
the independent execution has its own different branch order and
counts.

Positive and mutation controls pass. The genuine k=5 wrapped twin
is accepted when the third pair is removed; its mutated second base
word is rejected. Exhaustive twin classification confirms that this
is the only feasible input-mask pair among the 3389 cases. Direct
receipt corruption and missing-case mutations are detected.

Reproduce from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-review-v4/replay_readonly.py
```

Only the Python standard library is required. The chronology and exact
old-source contact are recorded in `INITIAL_SOURCE_CONTACT.json`,
`PRE_AUTHOR_FREEZE.json`, and `FIRST_AUTHOR_CONTACT.json`.
`RECONSTRUCTION.md` gives the mathematical interpretation of the
independent checker. `INDEPENDENT_RUN.json`, `NEGATIVE_CONTROL_RUN.json`,
and `COMPARISON_RUN.json` record actual executions.
The replay wrapper prints fresh reports without modifying these frozen
execution records. `--part core`, `--part controls`, or `--part comparison`
can replay only the requested check.

This is review by a separate AI agent, not external human peer review,
Lean formalization, historical-priority certification, an independent
rerun of the inherited global support classification, a SHA-256 hash
attack, main integration, or permission for a DOI/Release. No new
failure mechanism was discovered in the accepted proof. The twin
positive control explains precisely why dropping the third pair
would invalidate the claimed stronger ceiling.
