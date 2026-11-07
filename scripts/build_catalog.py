"""Builds catalog.json from entries/*.json, and refuses what is wrong.

    python scripts/build_catalog.py            # write catalog.json
    python scripts/build_catalog.py --check    # validate only (pull requests)

catalog.json is what Reginald reads. It is generated - edit entries/, never it.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, 'entries')
OUT = os.path.join(ROOT, 'catalog.json')
HOME = 'https://raw.githubusercontent.com/Zement/Patches-Catalog/main/catalog.json'

ICONS = os.path.join(ROOT, 'icons')
#: An icon is icons/<id>.png: a PNG of at most 128 x 128 and 256 KB. The build
#: adds it to its entry with its sha256 - no entry edit needed.
ICON_MAX_SIDE = 128
ICON_MAX_BYTES = 256 * 1024

SOURCE_TYPES = ('hosted', 'linked-release', 'linked-source', 'external', 'none')
DEFINITION_TYPES = ('in-mod', 'hosted', 'generated')
#: `ongoing`: a mod in development, listed without a download (source.type
#: "none" and a page in links)
CATEGORIES = ('mod', 'demo', 'base', 'ongoing')
LENGTHS = ('short', 'medium', 'long', 'full', None)
ID = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
SHA256 = re.compile(r'^[0-9a-f]{64}$')


def problems(entry, filename, ids):
    found = []
    eid = entry.get('id', '')
    if not ID.match(eid):
        found.append('id %r: lowercase letters, digits and dashes only' % eid)
    if filename != eid + '.json':
        found.append('file name must be %s.json' % eid)
    for field in ('name', 'version', 'author', 'description'):
        if not isinstance(entry.get(field), str) or (field == 'name' and not entry[field]):
            found.append('%s: missing' % field)
    if not isinstance(entry.get('revision', 0), int):
        found.append('revision: a number')
    if entry.get('category') not in CATEGORIES:
        found.append('category: one of %s' % ', '.join(CATEGORIES))
    if entry.get('length') not in LENGTHS:
        found.append('length: one of %s, or null' % ', '.join(l for l in LENGTHS if l))
    source = entry.get('source') or {}
    if source.get('type') not in SOURCE_TYPES:
        found.append('source.type: one of %s' % ', '.join(SOURCE_TYPES))
    if entry.get('category') == 'ongoing' or source.get('type') == 'none':
        # Listed without a download: the rest of the checks are for one
        if entry.get('category') != 'ongoing' or source.get('type') != 'none':
            found.append('an entry without a download: category "ongoing" and source.type "none"')
        links = entry.get('links') or {}
        if not any(str(v).startswith('https://') for v in links.values()):
            found.append('links: at least one https page (website, page or announcement)')
        return found
    if source.get('type') in ('linked-release', 'linked-source') and not source.get('repo'):
        found.append('source.repo: owner/name for a linked entry')
    download = entry.get('download') or {}
    if source.get('type') == 'external':
        if not str(download.get('page', '')).startswith('https://'):
            found.append('download.page: the https page the file is downloaded from')
        if not SHA256.match(download.get('sha256') or ''):
            found.append('download.sha256: required for an external entry (the file is checked)')
    elif not str(download.get('url', '')).startswith('https://'):
        found.append('download.url: an https address')
    if download.get('sha256') and not SHA256.match(download['sha256']):
        found.append('download.sha256: 64 hex digits')
    mod = entry.get('mod') or {}
    if not mod.get('folder') or not mod.get('xml'):
        found.append('mod.folder and mod.xml: paths in the download')
    definition = entry.get('definition') or {}
    if definition.get('type') not in DEFINITION_TYPES:
        found.append('definition.type: one of %s' % ', '.join(DEFINITION_TYPES))
    if definition.get('type') == 'in-mod' and not definition.get('path'):
        found.append('definition.path: where main.xml is in the download')
    if definition.get('type') == 'hosted':
        if not str(definition.get('url', '')).startswith('https://'):
            found.append('definition.url: an https address')
        if not SHA256.match(definition.get('sha256') or ''):
            found.append('definition.sha256: required for a hosted definition')
    base = entry.get('base')
    if base not in (None, 'retail') and base not in ids:
        found.append('base %r: "retail" or the id of another entry' % base)
    for req in entry.get('requires') or ():
        if req not in ids:
            found.append('requires %r: not an entry' % req)
    return found


def icon_for(eid):
    """({'path', 'sha256'} or None, problem or None) for icons/<eid>.png."""
    import hashlib
    import struct
    path = os.path.join(ICONS, eid + '.png')
    if not os.path.isfile(path):
        return None, None
    with open(path, 'rb') as fh:
        data = fh.read()
    if not data.startswith(b'\x89PNG\r\n\x1a\n') or data[12:16] != b'IHDR':
        return None, 'icons/%s.png: not a PNG' % eid
    width, height = struct.unpack('>II', data[16:24])
    if max(width, height) > ICON_MAX_SIDE or len(data) > ICON_MAX_BYTES:
        return None, ('icons/%s.png: %dx%d, %d KB - at most %dx%d and %d KB'
                      % (eid, width, height, len(data) // 1024, ICON_MAX_SIDE, ICON_MAX_SIDE,
                         ICON_MAX_BYTES // 1024))
    return {'path': 'icons/%s.png' % eid, 'sha256': hashlib.sha256(data).hexdigest()}, None


def main():
    check_only = '--check' in sys.argv
    files = sorted(f for f in os.listdir(ENTRIES) if f.endswith('.json'))
    entries, errors = [], []
    for f in files:
        try:
            with open(os.path.join(ENTRIES, f), encoding='utf-8') as fh:
                entries.append((f, json.load(fh)))
        except ValueError as error:
            errors.append('%s: not valid JSON (%s)' % (f, error))
    ids = {e.get('id') for _, e in entries}
    for f, entry in entries:
        errors += ['%s: %s' % (f, p) for p in problems(entry, f, ids)]
        icon, problem = icon_for(entry.get('id', ''))
        if problem:
            errors.append(problem)
        if icon:
            entry['icon'] = icon
    if os.path.isdir(ICONS):
        for name in sorted(os.listdir(ICONS)):
            if name.endswith('.png') and name[:-4] not in ids:
                errors.append('icons/%s: no entry with that id' % name)
    if errors:
        print('\n'.join(errors))
        print('\n%d problem(s) in %d entries' % (len(errors), len(entries)))
        sys.exit(1)
    if check_only:
        print('%d entries, all valid' % len(entries))
        return
    catalog = {'schema': 2, 'catalog': HOME,
               'entries': sorted((e for _, e in entries), key=lambda e: e['name'].lower())}
    text = json.dumps(catalog, indent=1, ensure_ascii=False) + '\n'
    old = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
    if text != old:
        with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        print('catalog.json: %d entries (changed)' % len(entries))
    else:
        print('catalog.json: %d entries (unchanged)' % len(entries))


if __name__ == '__main__':
    main()
