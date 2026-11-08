"""Moves the pins of linked entries to what their authors published since.

    GITHUB_TOKEN=... python scripts/resolve_links.py

Runs in the scheduled workflow (resolve-links.yml), which opens a pull request
with whatever changed - a pin moves only when that is merged (G-c Reply 2):

- linked-release: the author's latest release with a zip asset; download =
  that asset (with GitHub's sha256 digest when it gives one), date = its
  publish date, tag = its tag.
- linked-source: the latest tag, or the default branch when the repository has
  none (G-c Reply 2: "pin the latest tag"); download = GitHub's archive of that
  commit (root "*": the archive wraps it in "<repo>-<commit>/"), date = the
  commit's date.

Only the GitHub API, with the workflow's token (1,000 requests an hour) -
Reginald itself never calls the API.
"""

import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, 'entries')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import list_files  # noqa: E402
API = 'https://api.github.com'


def api(path):
    request = urllib.request.Request(API + path, headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + os.environ.get('GITHUB_TOKEN', ''),
        'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def resolve_release(entry):
    repo = entry['source']['repo']
    release = api('/repos/%s/releases/latest' % repo)
    wanted = entry['source'].get('asset')          # optional: an asset name to pick
    assets = [a for a in release.get('assets', []) if a['name'].lower().endswith('.zip')]
    if wanted:
        assets = [a for a in assets if a['name'] == wanted] or assets
    if not assets:
        return None
    asset = assets[0]
    digest = (asset.get('digest') or '')
    return {'tag': release['tag_name'], 'date': release['published_at'][:10],
            'download': {'url': asset['browser_download_url'], 'size': asset['size'],
                         'sha256': digest[7:] if digest.startswith('sha256:') else None,
                         'root': entry['download'].get('root', '')}}


def resolve_source(entry):
    repo = entry['source']['repo']
    tags = api('/repos/%s/tags?per_page=1' % repo)
    if tags:
        tag, sha = tags[0]['name'], tags[0]['commit']['sha']
    else:
        info = api('/repos/%s' % repo)
        branch = api('/repos/%s/branches/%s' % (repo, info['default_branch']))
        tag, sha = None, branch['commit']['sha']
    commit = api('/repos/%s/commits/%s' % (repo, sha))
    return {'tag': tag, 'commit': sha, 'date': commit['commit']['committer']['date'][:10],
            'download': {'url': 'https://github.com/%s/archive/%s.zip' % (repo, sha),
                         'size': None, 'sha256': None, 'root': '*'}}


def main():
    changed = []
    for name in sorted(os.listdir(ENTRIES)):
        if not name.endswith('.json'):
            continue
        path = os.path.join(ENTRIES, name)
        with open(path, encoding='utf-8') as f:
            entry = json.load(f)
        kind = (entry.get('source') or {}).get('type')
        if kind not in ('linked-release', 'linked-source'):
            continue
        try:
            found = resolve_release(entry) if kind == 'linked-release' else resolve_source(entry)
        except Exception as error:
            print('%s: could not resolve (%s)' % (entry['id'], error))
            continue
        if not found:
            print('%s: no zip in the latest release' % entry['id'])
            continue
        pin_before = (entry['source'].get('tag'), entry['source'].get('commit'), entry['download'].get('url'))
        entry['source']['tag'] = found['tag']
        if 'commit' in found:
            entry['source']['commit'] = found['commit']
        entry['date'] = found['date']
        entry['download'] = found['download']
        moved = (entry['source'].get('tag'), entry['source'].get('commit'), entry['download']['url']) != pin_before
        if moved:
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(json.dumps(entry, indent=1, ensure_ascii=False) + '\n')
            changed.append('%s -> %s' % (entry['id'], found['tag'] or found.get('commit', '')[:7]))
        if kind == 'linked-source' and (moved or not list_files.current(entry)):
            # The archive's file list, for updates by parts (D-o.5 B7)
            try:
                list_files.write_listing(entry)
            except Exception as error:
                print('%s: no file list (%s)' % (entry['id'], error))
    print('\n'.join(changed) if changed else 'no linked entry moved')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as f:
            f.write('\n'.join('- ' + c for c in changed) or 'No linked entry moved.')


if __name__ == '__main__':
    sys.exit(main())
