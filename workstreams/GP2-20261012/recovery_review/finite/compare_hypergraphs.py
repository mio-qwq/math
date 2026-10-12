#!/usr/bin/env python3
"""Compare literal enumeration and independently joined forbidden edge sets."""
import argparse
import hashlib
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    independent = runpy.run_path(str(HERE / "verify_finite_independent.py"))
    original_path = HERE.parents[1] / "stage2" / "verify_forced_cover.py"
    original = runpy.run_path(str(original_path))
    certificate_path = original_path.parent / "forced_cover_certificate.json"
    doc = json.loads(certificate_path.read_text())
    all_orbits, viable, forced = independent["reconstruct_orbits"](doc["n"], doc["levels"])
    original_viable_count, original_forced = original["forced_words"](doc["n"], doc["levels"])
    if original_viable_count != len(viable) or original_forced != forced:
        raise ValueError("independent and original rotation reconstruction differ")
    joined, _, _ = independent["reconstruct_edges"](forced)
    f = sorted(forced)
    literal_edges = {
        frozenset(f[i] for i in edge)
        for edge in original["all_hyperedges"](doc["n"], forced)
    }
    if joined != literal_edges:
        raise ValueError("literal and gap-join hypergraphs differ")
    report = {
        "viable_orbits_equal": True,
        "forced_word_sets_equal": True,
        "full_hyperedge_sets_equal": True,
        "edge_count": len(joined),
        "canonical_hypergraph_sha256": independent["digest_edges"](doc["n"], joined),
        "original_verifier_sha256": hashlib.sha256(original_path.read_bytes()).hexdigest(),
    }
    output = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output)
    print("PASS: full original literal and independent gap-join hypergraphs agree")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
