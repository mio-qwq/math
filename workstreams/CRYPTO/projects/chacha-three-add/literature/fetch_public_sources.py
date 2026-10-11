#!/usr/bin/env python3
"""Fetch expressly public research copies; never attempts access-control bypasses.

Downloaded third-party PDFs and full extracted text stay in ignored cache/.
Only a retrieval manifest is intended for version control. No credentials used.
"""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sys
import urllib.request

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "latin_dances_2022": "https://www.iacr.org/archive/asiacrypt2022/137910004/137910004.pdf",
    "latin_dances_2022_mirror": "https://jackgiffin.com/main/pdfs/Coutinho-Latin-Dances-Reloaded-2022.pdf",
    "sarkar_2009": "https://eprint.iacr.org/2009/047.pdf",
    "nyberg_wallen_2006": "https://www.tcs.hut.fi/Publications/knyberg/snowpreproc.pdf",
    "coutinho_2021_collection": "https://www.gov.br/abin/pt-br/assuntos/tecnologia/CEPESC_coletanea.pdf",
    "mealy_2026": "https://hukaisdu.github.io/files/papers/2026-1193-mealy-machines.pdf",
    "walsh_dl_2026": "https://hukaisdu.github.io/files/papers/2026-2013-walsh-transform-differential-linear.pdf",
}


def fetch(name):
    url = SOURCES[name]
    record = {"name": name, "url": url, "retrieval_date_utc": datetime.now(timezone.utc).date().isoformat()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Research-Literature-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=25) as response:
            data = response.read()
            record["http_status"] = response.status
        if not data.startswith(b"%PDF"):
            raise ValueError("Response is not a PDF")
        cache = ROOT / "cache"
        cache.mkdir(exist_ok=True)
        (cache / (name + ".pdf")).write_bytes(data)
        pages = PdfReader(io.BytesIO(data)).pages
        extracted = "\n".join(f"\n--- PAGE {i + 1} ---\n" + (page.extract_text() or "") for i, page in enumerate(pages))
        (cache / (name + ".txt")).write_text(extracted, encoding="utf-8")
        record.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), pages=len(pages), status="retrieved")
    except Exception as exc:
        record.update(status="unavailable", error=f"{type(exc).__name__}: {exc}")
    return record


if __name__ == "__main__":
    names = sys.argv[1:] or list(SOURCES)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(fetch, names))
    manifest = ROOT / "retrieval_manifest.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else []
    merged = {record["name"]: record for record in previous}
    merged.update({record["name"]: record for record in records})
    manifest.write_text(json.dumps(list(merged.values()), indent=2) + "\n", encoding="utf-8")
    print(json.dumps(records, indent=2))
