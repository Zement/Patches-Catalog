"""Hosted mods whose authors are still at work: which are due for an update
check (Zement, G-c Reply 11 - "check manually for updates each 3 months or
so").

    python scripts/check_upstream.py              # the list, as Markdown
    python scripts/check_upstream.py --mark <id>  # checked today

A hosted entry with `source.upstream` (the author's own page - MEGA,
GameBanana, a website) is a copy of a mod that may move on without us. Its
`source.checked` is the last time someone looked; after DUE_DAYS it is due.
The quarterly *Upstream check* workflow opens an issue with this list.
"""

import datetime
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUE_DAYS = 80          # a quarter, give or take: the workflow runs every 3 months


def entries():
    for path in sorted(glob.glob(os.path.join(ROOT, 'entries', '*.json'))):
        yield path, json.load(open(path, encoding='utf-8'))


def main():
    today = datetime.date.today()
    if '--mark' in sys.argv:
        eid = sys.argv[sys.argv.index('--mark') + 1]
        path = os.path.join(ROOT, 'entries', eid + '.json')
        entry = json.load(open(path, encoding='utf-8'))
        entry['source']['checked'] = today.isoformat()
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(entry, indent=1, ensure_ascii=False) + '\n')
        print('%s checked %s' % (eid, today))
        return
    due = []
    for _path, e in entries():
        src = e.get('source') or {}
        if src.get('type') != 'hosted' or not src.get('upstream'):
            continue
        try:
            last = datetime.date.fromisoformat(src.get('checked') or '2000-01-01')
        except ValueError:
            last = datetime.date(2000, 1, 1)
        if (today - last).days >= DUE_DAYS:
            due.append((e, last))
    if not due:
        return
    print('These hosted mods have authors who may have released a newer version since '
          'they were last checked. For each: look at its page; if there is a new version, '
          'publish it (`scripts/publish_hosted.py <id> <zip> - <version> 1`); either way, '
          'mark it checked (`scripts/check_upstream.py --mark <id>`).\n')
    print('| Mod | Ours | Last checked | Page |')
    print('|---|---|---|---|')
    for e, last in due:
        print('| %s (`%s`) | %s-%s | %s | %s |' % (e['name'], e['id'], e.get('version', ''),
                                                  e.get('revision', ''), last, e['source']['upstream']))


if __name__ == '__main__':
    main()
