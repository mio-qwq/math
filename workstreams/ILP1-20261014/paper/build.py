#!/usr/bin/env python3
"""Rebuild the research PDF; keep TeX intermediates temporary."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile


def main():
    paper = Path(__file__).resolve().parent
    evidence = paper.parent / "evidence"
    source = paper / "draft.tex"
    evidence.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ilp1-paper-") as temp:
        for _ in range(2):
            run = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 f"-output-directory={temp}", str(source)],
                cwd=paper, text=True, capture_output=True,
            )
            if run.returncode:
                raise RuntimeError(run.stdout + run.stderr)
        log = (Path(temp) / "draft.log").read_text()
        (evidence / "paper-build.log").write_text(log)
        for prohibited in ("Overfull \\hbox", "Overfull \\vbox", "undefined references"):
            if prohibited in log:
                raise RuntimeError(f"Layout/reference check failed: {prohibited}")
        target = paper / "ilp1-research-draft.pdf"
        shutil.copyfile(Path(temp) / "draft.pdf", target)
    info = subprocess.check_output(["pdfinfo", str(target)], text=True)
    receipt = {
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "pdfinfo": info,
        "build_status": "PASS",
        "visual_review": "Recorded separately; compilation alone is not visual QA.",
    }
    (evidence / "paper-build.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(info)


if __name__ == "__main__":
    main()
