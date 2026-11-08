"""Writes files/<id>.json: the files in a source-linked mod's archive.

    python scripts/list_files.py            # every linked-source entry whose list is missing or stale
    python scripts/list_files.py <id> ...   # just these (written again)

A `linked-source` entry downloads GitHub's archive of its pinned commit, and
those archives send no byte ranges - so Reginald could not update one by parts
and downloaded the whole archive every time. With this list (the archive's own
directory: each file's name, size and CRC-32, and the commit it is for)
Reginald compares a mod's files against it and fetches only the ones that
differ, one by one from raw.githubusercontent.com (D-o.5 B7).

The resolver (resolve_links.py) writes the list whenever it moves a pin; the
build adds it to its entry as `download.files` with its sha256, and refuses a
list made for another commit.
"""

import io
import json
import os
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, 'entries')
FILES = os.path.join(ROOT, 'files')


def listing_path(eid):
    return os.path.join(FILES, eid + '.json')


def current(entry):
    """Whether the entry's list exists and is for its pinned commit."""
    try:
        with open(listing_path(entry['id']), encoding='utf-8') as f:
            return json.load(f).get('commit') == entry['source'].get('commit')
    except (OSError, ValueError):
        return False


def write_listing(entry):
    """Downloads the archive once and writes its list. Returns the file count."""
    url = entry['download']['url']
    request = urllib.request.Request(url, headers={'User-Agent': 'Patches-Catalog'})
    with urllib.request.urlopen(request, timeout=300) as response:
        data = response.read()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        files = [{'name': info.filename, 'size': info.file_size, 'crc': info.CRC}
                 for info in archive.infolist() if not info.is_dir()]
    os.makedirs(FILES, exist_ok=True)
    listing = {'commit': entry['source']['commit'], 'files': files}
    with open(listing_path(entry['id']), 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(listing, separators=(',', ':')) + '\n')
    return len(files)


def main():
    wanted = set(sys.argv[1:])
    for name in sorted(os.listdir(ENTRIES)):
        with open(os.path.join(ENTRIES, name), encoding='utf-8') as f:
            entry = json.load(f)
        if (entry.get('source') or {}).get('type') != 'linked-source':
            continue
        if wanted and entry['id'] not in wanted:
            continue
        if not wanted and current(entry):
            continue
        try:
            print('%-40s %d files' % (entry['id'], write_listing(entry)))
        except Exception as error:      # one mod never stops the others
            print('%-40s failed: %s' % (entry['id'], error))


if __name__ == '__main__':
    main()
