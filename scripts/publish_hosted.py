"""Publishes a hosted mod version as a GitHub Release, and updates its entry.

    python scripts/publish_hosted.py <id> <mod.zip> <definition folder | -> <version> <revision>
        [--notes "text"] [--dry-run]

`-` for the definition: the mod alone; the entry keeps its definition
(generated, or the one the mod carries).

Example (Newer, G-c.4):

    python scripts/publish_hosted.py newer-smbw D:/.../edit/Newer_W_1.30.zip ^
        D:/.../edit/Newer_W_1.30/patches/NewerSMBW 1.30 1

- tag `<id>/<version>-<revision>` (newer-smbw/1.30-1), two assets: the mod as
  given (`<id>-<version>-<revision>.zip`) and the definition alone
  (`<id>-patch-<version>-<revision>.zip`, its folder inside). A fix to the
  definition is a new revision whose mod asset can be the same zip again -
  Reginald downloads only what changed (Repair, G-c.3).
- entries/<id>.json: download url/size/sha256, definition as `hosted` with
  url/sha256/folder, version, revision, date. Then run build_catalog.py.

Needs `gh` logged in with write access to the repository.
"""

import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = 'Zement/Patches-Catalog'


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    notes = ''
    if '--notes' in sys.argv:
        notes = sys.argv[sys.argv.index('--notes') + 1]
        args.remove(notes)
    eid, mod_zip, definition, version, revision = args
    revision = int(revision)
    tag = '%s/%s-%d' % (eid, version, revision)
    label = '%s-%d' % (version, revision)
    entry_path = os.path.join(ROOT, 'entries', eid + '.json')
    entry = json.load(open(entry_path, encoding='utf-8'))
    # "-": no definition yet - the mod alone, the entry's definition stays
    # whatever it is (generated, or in the mod) (G-c.8c)
    has_definition = definition != '-'
    if has_definition and not os.path.isfile(os.path.join(definition, 'main.xml')):
        sys.exit('%s has no main.xml' % definition)

    work = tempfile.mkdtemp(prefix='publish-')
    try:
        folder = os.path.basename(os.path.normpath(definition)) if has_definition else None
        patch_zip = os.path.join(work, '%s-patch-%s.zip' % (eid, label)) if has_definition else None
        if has_definition:
            with zipfile.ZipFile(patch_zip, 'w', zipfile.ZIP_DEFLATED) as z:
                for dirpath, _dirs, files in os.walk(definition):
                    for f in files:
                        if f in ('install.json', 'collab.json') or f.endswith('.pyc'):
                            continue
                        full = os.path.join(dirpath, f)
                        z.write(full, os.path.join(folder, os.path.relpath(full, definition)).replace(os.sep, '/'))
        # The mod asset under its catalog name: a hard link where the volume
        # allows it (a 500 MB zip is not copied for a name), else a copy.
        mod_asset = os.path.join(os.path.dirname(os.path.abspath(mod_zip)), '%s-%s.zip' % (eid, label))
        if not os.path.exists(mod_asset):
            try:
                os.link(mod_zip, mod_asset)
            except OSError:
                mod_asset = os.path.join(work, '%s-%s.zip' % (eid, label))
                shutil.copy2(mod_zip, mod_asset)
        print('hashing...')
        mod_sha = sha256(mod_asset)
        base = 'https://github.com/%s/releases/download/%s/' % (REPO, tag)
        entry['version'], entry['revision'] = version, revision
        entry['date'] = datetime.date.today().isoformat()
        source = dict(entry.get('source') or {}, type='hosted', tag=tag)
        source.pop('host', None)                     # here now, not on another host
        entry['source'] = source
        entry['download'] = {'url': base + os.path.basename(mod_asset), 'size': os.path.getsize(mod_asset),
                             'sha256': mod_sha, 'root': ''}
        if has_definition:
            entry['definition'] = {'type': 'hosted', 'url': base + os.path.basename(patch_zip),
                                   'sha256': sha256(patch_zip), 'folder': folder}
        print(json.dumps({k: entry[k] for k in ('version', 'revision', 'download', 'definition')}, indent=1))
        if dry:
            return
        title = '%s %s' % (entry['name'], label)
        body = notes or '%s, hosted for Reginald\'s catalog. All rights remain with its authors: %s.' % (
            entry['name'], entry.get('author', ''))
        assets = [mod_asset] + ([patch_zip] if has_definition else [])
        subprocess.run(['gh', 'release', 'create', tag] + assets + ['--repo', REPO,
                        '--title', title, '--notes', body], check=True)
        with open(entry_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(entry, indent=1, ensure_ascii=False) + '\n')
        print('released %s; now run scripts/build_catalog.py and push' % tag)
    finally:
        shutil.rmtree(work, ignore_errors=True)
        link = os.path.join(os.path.dirname(os.path.abspath(mod_zip)), '%s-%s.zip' % (eid, label))
        if os.path.exists(link) and os.path.abspath(link) != os.path.abspath(mod_zip):
            try:
                os.remove(link)
            except OSError:
                pass


if __name__ == '__main__':
    main()
