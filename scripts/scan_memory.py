"""Reads each mod's archive heap size and fixHeaps patch out of its release.

    python scripts/scan_memory.py                # report every entry with a download
    python scripts/scan_memory.py <id> [...]     # just these
    python scripts/scan_memory.py --write        # also write metadata.archive_memory
                                                 # and metadata.fixheaps_off where known

The archive heap holds every file a level loads: 18 MB in the game, enlarged
by most mods (Newer: 20 MB) through a `<memory>` patch in their Riivolution
XML on the `lis r3, 0x120` in dSys_c::create. And the game's dSystem::fixHeaps
keeps a reserve of ~3.85 MB of it at every course-in, which Kamek code turns
off (a `blr` at its start). Reginald's memory estimate needs both; it reads
them the same way from an installed mod (playtest/dolphin.py), and measures
them in the running game with Import Game Data.

From the release zip with HTTP range requests, only the Riivolution XMLs and
the System*.bin code files:

- `archive_memory` (MB, the size the XML sets; 18 when no patch touches it);
- `fixheaps_off`: true when the PAL code holds the patch, false when the mod
  has no code; left out when its code cannot show it (Kamek code linked at
  load time - DLCode*.bin - or code without the patch as bytes);
- an XML that is not well-formed is reported: Dolphin cannot load the mod,
  and Reginald cannot read it. `mod.xml_fix` in its entry corrects it at
  install ([old, new] text pairs); the scan reads the XML with them applied.
"""

import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_icons import HttpFile  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, 'entries')
FILES = os.path.join(ROOT, 'files')
AGENT = 'Patches-Catalog memory scan'

#: `lis r3, 0x120` in dSys_c::create: PAL, NTSC, JP, KR/TW (as Reginald's dolphin.py)
ARCHIVE_HEAP_SITES = (0x800E4A84, 0x800E4994, 0x800E4914, 0x800E4AA4)
ARCHIVE_HEAP_ORIGINAL = 0x3C600120
RETAIL_MB = 18
#: Kamek's patch record for `blr` at dSystem::fixHeaps (PAL 0x800E53E0)
FIX_HEAPS_OFF = bytes.fromhex('800e53e0 4e800020')


def heap_of(root):
    """The heap size (bytes) the XML's <memory> patches set, or None."""
    found = {}
    for mem in root.iter('memory'):
        try:
            offset = int(mem.get('offset', ''), 16)
            value = int(mem.get('value', ''), 16)
            original = int(mem.get('original') or '0', 16)
        except ValueError:
            continue
        if offset in ARCHIVE_HEAP_SITES and original in (0, ARCHIVE_HEAP_ORIGINAL) \
                and value >> 16 == 0x3C60:
            found.setdefault(offset, (value & 0xFFFF) << 16)
    return next((found[s] for s in ARCHIVE_HEAP_SITES if s in found), None)


def memory_lines(text):
    """The <memory> elements of an XML that does not parse, read one by one."""
    root = ET.Element('wiidisc')
    for tag in re.findall(r'<memory\b[^>]*/>', text):
        try:
            root.append(ET.fromstring(tag))
        except ET.ParseError:
            continue
    return root


def read_xml(data):
    """(root, problem): the XML's root, or the <memory> lines of a broken one."""
    text = data.decode('utf-8', 'replace').lstrip('﻿')
    try:
        return ET.fromstring(text), None
    except ET.ParseError as error:
        line = error.position[0]
        shown = text.splitlines()[line - 1].strip() if 0 < line <= len(text.splitlines()) else ''
        return memory_lines(text), '%s: %s' % (error, shown[:90])


def is_pal_code(name):
    """SystemP1.bin, SystemEU_1.bin, Code/P1.bin: the PAL code (its patches
    hold PAL addresses)."""
    return re.fullmatch(r'(system_?(p|eu)\w*|(p|eu)_?[12]?)\.bin', os.path.basename(name).lower()) is not None


def loads_code(root):
    """Whether the XML loads code: Kamek's loader comes in as a <memory valuefile>."""
    return any(mem.get('valuefile') for mem in root.iter('memory'))


def xml_turns_fixheaps_off(root):
    return any(mem.get('offset', '').lower() in ('0x800e53e0', '800e53e0')
               and mem.get('value', '').lower() == '4e800020' for mem in root.iter('memory'))


class Zip:
    """A release zip read with ranges."""

    def __init__(self, url):
        self.archive = zipfile.ZipFile(io.BufferedReader(HttpFile(url), 1024 * 1024))
        self.names = [n for n in self.archive.namelist() if '__macosx' not in n.lower()]

    def read(self, name):
        return self.archive.read(name)


class Raw:
    """A linked-source mod: its file list, files from raw.githubusercontent.com."""

    def __init__(self, entry):
        with open(os.path.join(FILES, entry['id'] + '.json'), encoding='utf-8') as f:
            listing = json.load(f)
        self.repo, self.commit = entry['source']['repo'], listing['commit']
        self.names = [item['name'] for item in listing['files']]

    def read(self, name):
        path = name.split('/', 1)[1]
        url = 'https://raw.githubusercontent.com/%s/%s/%s' % (self.repo, self.commit, urllib.parse.quote(path))
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': AGENT}),
                                    timeout=60) as response:
            return response.read()


def scan(entry):
    source = entry.get('source') or {}
    if source.get('type') == 'linked-source':
        files = Raw(entry)
    else:
        files = Zip(entry['download']['url'])
    root = (entry.get('download') or {}).get('root') or ''
    if root == '*':         # the archive's one top folder (GitHub's archives)
        root = files.names[0].split('/', 1)[0] + '/'
    mod = entry.get('mod') or {}
    lower = {n.lower(): n for n in files.names}
    out = {'xml': None, 'problem': None, 'heap': None, 'code': None, 'fixheaps_off': None}

    xml_name = lower.get((root + mod.get('xml', '')).lower())
    if xml_name is None:
        out['problem'] = 'its XML %s is not in the download' % mod.get('xml')
        return out
    out['xml'] = xml_name
    data = files.read(xml_name)
    # The XML as Reginald installs it: with the entry's corrections
    for old, new in mod.get('xml_fix') or ():
        data = data.replace(old.encode('utf-8'), new.encode('utf-8'), 1)
    xml, out['problem'] = read_xml(data)
    out['heap'] = heap_of(xml)

    if xml_turns_fixheaps_off(xml):
        out['fixheaps_off'] = True
    if not loads_code(xml):
        # No code: what the XML patches word by word is all that changes
        out['fixheaps_off'] = out['fixheaps_off'] or False
        return out
    folder = (root + mod.get('folder', '')).lower().rstrip('/') + '/'
    # The code sits in the mod's folder (NewerRes/, Code/), or beside it in the zip
    top = folder.rsplit('/', 2)[0] + '/' if folder.count('/') > 1 else ''
    names = [n for n in files.names if n.lower().startswith(top)]
    out['code'] = 'dlcode' if any(os.path.basename(n).lower().startswith('dlcode') for n in names) else 'kamek'
    code = [n for n in names if is_pal_code(n)]
    if out['fixheaps_off'] is None and any(FIX_HEAPS_OFF in files.read(n) for n in code):
        out['fixheaps_off'] = True
    return out


def main():
    args = sys.argv[1:]
    write = '--write' in args
    wanted = {a for a in args if not a.startswith('--')}
    entries = []
    for name in sorted(os.listdir(ENTRIES)):
        with open(os.path.join(ENTRIES, name), encoding='utf-8') as f:
            entry = json.load(f)
        if wanted and entry['id'] not in wanted:
            continue
        if entry.get('source', {}).get('type') == 'none' or not (entry.get('download') or {}).get('url'):
            continue
        entries.append(entry)

    def one(entry):
        try:
            return entry, scan(entry), None
        except Exception as error:      # one mod never stops the others
            return entry, None, error

    from concurrent.futures import ThreadPoolExecutor
    results = []
    with ThreadPoolExecutor(6) as pool:
        for entry, found, error in pool.map(one, entries):
            if error is not None:
                print('%-48s failed: %s' % (entry['id'], error), flush=True)
                continue
            mb = (found['heap'] or RETAIL_MB << 20) / 1048576
            print('%-48s %5.1f MB%s  code %-6s fixHeaps %s%s' % (
                entry['id'], mb, '' if found['heap'] else ' (no patch)', found['code'] or '-',
                {True: 'off', False: 'kept', None: '?'}[found['fixheaps_off']],
                '\n    XML %s: %s' % (found['xml'], found['problem']) if found['problem'] else ''),
                flush=True)
            results.append((entry, found, mb))

    print('\n%d scanned; broken XMLs: %s; fixHeaps unknown: %s' % (
        len(results), ', '.join(e['id'] for e, f, _m in results if f['problem']) or 'none',
        ', '.join(e['id'] for e, f, _m in results if f['fixheaps_off'] is None) or 'none'))
    if not write:
        return
    changed = 0
    for entry, found, mb in results:
        if found['problem'] and not found['heap'] and not found['xml']:
            continue
        metadata = dict(entry.get('metadata') or {})
        # A lis sets 64 KB steps: 1/16 MB, four decimals exactly
        metadata['archive_memory'] = int(mb) if mb == int(mb) else round(mb, 4)
        if found['fixheaps_off'] is not None:
            metadata['fixheaps_off'] = found['fixheaps_off']
        if metadata != entry.get('metadata'):
            entry['metadata'] = metadata
            with open(os.path.join(ENTRIES, entry['id'] + '.json'), 'w', encoding='utf-8', newline='\n') as f:
                f.write(json.dumps(entry, indent=1, ensure_ascii=False) + '\n')
            changed += 1
    print('%d entries written' % changed)


if __name__ == '__main__':
    main()
