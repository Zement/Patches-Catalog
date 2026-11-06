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
| `hosted` | Mods no longer worked on, and Newer itself. A copy is published here as a release. | A release asset of this repository (or, for now, the old SourceForge catalog). |
| `linked-release` | Mods whose authors publish releases. | The author's own release asset. |
| `linked-source` | Mods kept only as a repository (tags, no release files). | GitHub's archive of the pinned commit. |

A linked entry is **pinned** (`source.tag` / `source.commit`). The daily
*Resolve linked mods* workflow looks for newer releases or tags and opens a pull
request that moves the pin; the new version reaches players when it is merged.

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
