# Patches Catalog

The catalog of *New Super Mario Bros. Wii* mods that [Reginald](https://github.com/Developers-Collective)
offers in its Patch Manager: where each mod comes from, how it installs, and the
Reginald patch definition that goes with it.

Reginald reads one file: [`catalog.json`](catalog.json). It is **generated** from
[`entries/`](entries) - one file per mod - by `scripts/build_catalog.py`, which runs
on every push. Never edit `catalog.json` by hand.

## How a mod gets to the player

Every entry answers two questions.

**Where the mod comes from** (`source.type`):

| Type | When | Download |
|---|---|---|
| `hosted` | Mods no longer worked on, Newer itself, and mods whose authors share them only where a program cannot download from (MEGA, Google Drive, GameBanana). A copy is published here as a release. | A release asset of this repository (or, for now, the old SourceForge catalog, or the archive.org mirror the Horizon wiki links: `source.host`). |
| `linked-release` | Mods whose authors publish releases. | The author's own release asset. |
| `linked-source` | Mods kept only as a repository (tags, no release files). | GitHub's archive of the pinned commit. |
| `external` | Mods still worked on whose only download is a page a program cannot use (MEGA, Google Drive, a mod's own site). | The player downloads the file on `download.page`; Reginald installs it after checking it against `download.sha256`. |

A hosted copy of a mod whose author still works on it names the author's page
(`source.upstream`) and when it was last looked at (`source.checked`). Every quarter
the *Upstream check* workflow opens an issue listing the ones due; a new version is
published with `scripts/publish_hosted.py`, and `scripts/check_upstream.py --mark <id>`
records the check.

A linked entry is **pinned** (`source.tag` / `source.commit`). The daily
*Resolve linked mods* workflow looks for newer releases or tags and opens a pull
request that moves the pin; the new version reaches players when it is merged.

A `linked-source` mod also has a **file list**, `files/<id>.json`: the files in
GitHub's archive of its pinned commit, with their sizes and CRC-32. Those archives
send no byte ranges, so without it Reginald could only update or repair the mod by
downloading it whole; with it, Reginald fetches just the files that differ, one by
one from raw.githubusercontent.com. The resolver writes the list whenever it moves a
pin (`scripts/list_files.py` by hand); the build adds it to its entry as
`download.files` with its sha256, and leaves out a list made for another commit.

**Where the Reginald patch definition comes from** (`definition.type`):

| Type | Meaning |
|---|---|
| `in-mod` | The mod's download carries it, at `definition.path`. |
| `hosted` | A small zip of its own (`definition.url`, checked against `definition.sha256`) - a fix ships without re-uploading the mod. |
| `generated` | Reginald writes a bare `main.xml` with the entry's `base`. |

## Versions

`version` is the author's own, shown as is. `revision` counts our repacks of a
hosted mod (Newer `1.30` with revision 1 is `1.30-1`). `date` orders versions -
version strings are too inconsistent between authors to be compared.

## Categories

`category`: `mod` (a mod to play), `demo` (an unfinished release), `base` (a base to
build mods on - NSMBWer+, PropelParts, NewerGEM), `ongoing` (a mod in development,
listed without a download). `length`, from the Horizon wiki:
`short` (1-2 worlds), `medium` (3-5), `long` (6-7), `full` (8+), or `null`. Only mods
with levels are listed: a Riivolution mod without a Stage folder (a practice tool, a
character model) has nothing to edit.

An `ongoing` entry has `source.type` `none` and no `download`, `mod` or `definition`.
Reginald shows it with an Open Page button for its first page in `links` (`website`,
`page`, `announcement`, `wiki`, `video`, `discord`), or a disabled In Development
when it has none. When it is released, it becomes a normal entry. Every value in
`links` is an https address.

`listed`: where the mod is known from - `wiki` (the Horizon wiki's list of mods, or a
page of its own there), `discord` (posted on the NSMB Hacking Domain or Horizon
servers), `github`, `archive` (the archive.org mirror the wiki links). Reginald shows
these, with the kinds other than `mod`, as the mod's categories.

## Icons

`icons/<id>.png` is the mod's icon in Reginald's Patch Manager: a PNG of at most
128 x 128 pixels and 256 KB. Reginald shows it in a 2:1 box (76 x 38 and 48 x 24), the
shape of a title logo, so 128 x 64 is the size to make. The build adds it to its entry
with its sha256 - the entry itself needs no change. Reginald fetches an icon once and
again only when its sha256 changes; a mod without one shows its initials.

`scripts/extract_icons.py` makes them from the mods themselves: the title logo in
`openingTitle.arc`, read from the release zip with range requests, cropped and scaled.
For a mod hosted where no program can download (`external`), give it the file:
`--local <id>=<zip or folder>`.

## Releases

One release per hosted mod version, tagged `<id>/<version>-<revision>`, with two
assets: the mod, and its definition alone. `scripts/publish_hosted.py` makes one
and updates the entry.

## Adding or changing a mod

Edit or add `entries/<id>.json` and open a pull request; the *Catalog* workflow
checks it. The fields are described in `scripts/build_catalog.py`. Notes on
values that were measured rather than known are in [`REVIEW.md`](REVIEW.md).

## Ownership

Every mod belongs to its authors, named in its entry. Mods are hosted here only
where they are no longer maintained or not on GitHub, and always with credit and
a link to their origin. Authors who want a mod changed, linked instead of hosted,
or removed: please open an issue.
