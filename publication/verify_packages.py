"""Validate publication payload manifests, archives and external checksums.

This is file-integrity verification, not a mathematical proof or a publication.
Run from any directory with ordinary Python 3 (no third-party dependencies).
"""
from pathlib import Path, PurePosixPath
from hashlib import sha256
import argparse
import json
import zipfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return sha256(raw).hexdigest()


def safe_path(repo, relative):
    posix = PurePosixPath(relative)
    require(not posix.is_absolute() and '..' not in posix.parts and
            '\\' not in relative and ':' not in relative, 'Unsafe path: '+relative)
    path = repo.joinpath(*posix.parts)
    require(path.resolve().is_relative_to(repo.resolve()), 'Path outside root: '+relative)
    return path


def verify_packet(repo, folder):
    manifest_path = folder/'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    rows = manifest['files']
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'Duplicate manifest entries')
    require(bool(rows), 'Empty payload')
    zip_paths = list(folder.glob('*.zip'))
    require(len(zip_paths) == 1, 'Expected exactly one archive')
    archive = zip_paths[0]
    relmanifest = manifest_path.relative_to(repo).as_posix()
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist()) == len(set(z.namelist())), 'Duplicate ZIP entries')
        require(set(z.namelist()) == set(names+[relmanifest]), 'ZIP entry set mismatch')
        require(z.testzip() is None, 'ZIP CRC failure')
        for row in rows:
            path = safe_path(repo, row['path'])
            raw = z.read(row['path'])
            require(len(raw) == row['bytes'] and digest(raw) == row['sha256'],
                    'Archive payload hash mismatch: '+row['path'])
            require(path.is_file() and raw == path.read_bytes(),
                    'Repository payload mismatch: '+row['path'])
        require(z.read(relmanifest) == manifest_path.read_bytes(), 'Manifest byte mismatch')
    lines = (folder/'SHA256SUMS').read_text(encoding='utf-8').splitlines()
    checksummed = set()
    for line in lines:
        expected, relative = line.split('  ', 1)
        path = safe_path(repo, relative)
        require(relative not in checksummed, 'Duplicate outer checksum')
        checksummed.add(relative)
        require(path.is_file() and digest(path.read_bytes()) == expected,
                'Outer checksum mismatch: '+relative)
    require(archive.relative_to(repo).as_posix() in checksummed and
            relmanifest in checksummed, 'Archive or manifest is not externally checksummed')
    meta = json.loads((folder/'metadata-draft.json').read_text(encoding='utf-8'))
    require(meta['doi'] is None and meta['zenodo_record_id'] is None and
            meta['doi_reserved'] is False, 'Unexpected external-publication claim')
    require(meta['metadata']['license'] is None and meta['metadata']['publication_date'] is None,
            'Unconfirmed license or publication date was filled')
    require(meta['human_author_metadata_status'] ==
            'USER_SUPPLIED_DRAFT_NOT_COMPLETED_ACCOUNTABILITY_REVIEW',
            'Missing author draft boundary')
    require(meta['metadata']['creators'] == [
        {'name': 'Zhang, River', 'orcid': '0009-0004-2437-8566',
         'affiliation': 'Chengdu Neusoft University'}],
        'Author draft differs from the supplied metadata')
    return {'package':folder.relative_to(repo).as_posix(),
            'archive_sha256':digest(archive.read_bytes()),
            'payload_files':len(rows),'zip_entries':len(rows)+1,
            'status':'FILE_INTEGRITY_PASS', 'mathematical_proof_checked':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    folders = [repo/'publication/006-v1.2']
    reports = [verify_packet(repo, folder) for folder in folders]
    print(json.dumps({'status':'ALL_PUBLICATION_FILE_INTEGRITY_PASS',
                      'packages':reports,'external_action_performed':False}, indent=2))


if __name__ == '__main__':
    main()
