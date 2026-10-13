"""Check this version's payload hashes before replaying any certificate."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
for record in manifest['files']:
    path=root/record['path']
    resolved=path.resolve()
    if not resolved.is_relative_to(root.resolve()): raise ValueError('Invalid payload path')
    data=path.read_bytes()
    if len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['sha256']:
        raise ValueError(f'Changed payload: {record["path"]}')
print(f'PASS: {len(manifest["files"])} exact payload files.')
