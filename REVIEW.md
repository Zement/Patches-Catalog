# Review notes

Measured by `catalog_v2_seed.py` (G-c.3/4) from each zip's file list - nothing
was downloaded - and the code again by `reclassify_code.py` (G-c.5) against
every Newer release. Guesses, for Zement to confirm or correct in `entries/`.

`code` is told from the mod's `DLCode*.bin` files by their CRC-32 and size,
not by a folder name:

| code | means | base guessed |
|---|---|---|
| `newer-1.30`, `newer-1.2.0`, ... | that Newer release's code, unchanged | Newer |
| `newer-custom` | Newer-sized code of its own (rebuilt; may add sprites) | Newer |
| `loader` | Newer's loader with a few KB of patches of its own - no Newer code | retail |
| `kamek` | Kamek code without Newer's loader | retail |
| `None` | no code | retail |

## Newer Super Mario Bros. Wii (`newer-smbw`)

- base: `retail`, code: `newer-1.30`, definition: `in-mod`
- hosted on this repository from Zement's rebuilt package (upstream sprites.py, spritegamedata.json)

## Another Mario Wii (`another-mario-wii`)

- base: `retail`, code: `kamek`, definition: `generated`
- code of its own (kamek): its definition may need more than the base
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Awesomer Super Luigi Mini (`awesomer-super-luigi-mini`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## New Mario Bros Cannon (`new-mario-bros-cannon`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Chilly Super Mario Bros. Wii (`chilly-super-mario-bros-wii`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Cliffs Of Spring (`cliffs-of-spring`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Cliff Mario Wii (`cliff-mario-wii`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Deluxe Mario Wii (`deluxe-mario-wii`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Devil Mario Winter Special (`devil-mario-winter-special`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- the XML reaches outside its folder: kitiku mwsp
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Epic Super Bowser World (`epic-super-bowser-world`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Ghostly Super Ghost Boos Wii (`ghostly-super-ghost-boos-wii`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Koopa Country (`koopa-country`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Lava SMBW Apocalypse (`lava-smbw-apocalypse`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Mario and the Mysterious Meteorite (`mario-and-the-mysterious-meteorite`)

- base: `newer-smbw`, code: `newer-1.30`, definition: `generated`
- base guessed as Newer (code: newer-1.30)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## MidnightWii (`midnightwii`)

- base: `newer-smbw`, code: `newer-1.2.0`, definition: `generated`
- base guessed as Newer (code: newer-1.2.0)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Marios Final Adventure Wii (`marios-final-adventure-wii`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## MLG Super Luigi Bros Wii (`mlg-super-luigi-bros-wii`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)
- XML path corrected to MLG Super Luigi Bros Wii/riivolution/MLGLuigiE.xml (the zip ships only this one; the PAL XML was taken out - playing on PAL may need it back)

## Marios New Adventure Demo (`marios-new-adventure-demo`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Mario Wii Other World (`mario-wii-other-world`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)
- XML path corrected to New Super Mario Bros Wii Other World/riivolution/OtherE.xml (the zip ships only this one; the PAL XML was taken out - playing on PAL may need it back)

## New Super Mario Bros. Wii 4 (`new-super-mario-bros-wii-4`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Newer Apocalypse (`newer-apocalypse`)

- base: `newer-smbw`, code: `newer-1.0.3`, definition: `generated`
- base guessed as Newer (code: newer-1.0.3)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Newer SUMMER SUN (`newer-summer-sun`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Dark Moon Reverse (`dark-moon-reverse`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## NewerSMB2 (`newersmb2`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Newer Alpine Dream (`newer-alpine-dream`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## NewerLAA (`newerlaa`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## NewerSMB7 (`newersmb7`)

- base: `newer-smbw`, code: `newer-1.1.1`, definition: `generated`
- base guessed as Newer (code: newer-1.1.1)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Newer FALLING LEAF (`newer-falling-leaf`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Newer Holiday Special (`newer-holiday-special`)

- base: `retail`, code: `loader`, definition: `generated`
- code of its own (loader): its definition may need more than the base
- base guessed as retail (Newer's loader with a few KB of patches, no Newer code)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## NSMBW2: The Next Levels (`nsmbw2-the-next-levels`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## NSMBWer+ (`nsmbwer-plus`)

- base: `newer-smbw`, code: `newer-custom`, definition: `in-mod`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)

## SLWii The Emissary (`slwii-the-emissary`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Super Mario Bros. Extreme Adventure (`super-mario-bros-extreme-adventure`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Starlight ADVENTURE (`starlight-adventure`)

- base: `newer-smbw`, code: `newer-1.30`, definition: `generated`
- base guessed as Newer (code: newer-1.30)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Super Luigi Land Wii (`super-luigi-land-wii`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Super Luigi Seasonal Shore (`super-luigi-seasonal-shore`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## SMMA+ (`smma`)

- base: `retail`, code: `None`, definition: `generated`
- the XML reaches outside its folder: sample
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Super Mario Snowy Season (`super-mario-snowy-season`)

- base: `newer-smbw`, code: `newer-1.2.0`, definition: `generated`
- base guessed as Newer (code: newer-1.2.0)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)
- XML path corrected to Snowy Season Riivo/riivolution/SnowySeason.xml (the zip ships only this one; the PAL XML was taken out - playing on PAL may need it back)

## Super Mario Super Star (`super-mario-super-star`)

- base: `newer-smbw`, code: `newer-1.2.0`, definition: `generated`
- base guessed as Newer (code: newer-1.2.0)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Super Mario Vacation (`super-mario-vacation`)

- base: `retail`, code: `None`, definition: `generated`
- base guessed as retail (no Newer loader)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

## Ultimate Super Luigi Wii (`ultimate-super-luigi-wii`)

- base: `newer-smbw`, code: `newer-custom`, definition: `generated`
- code of its own (newer-custom): its definition may need more than the base
- base guessed as Newer (code: newer-custom)
- no definition in the zip: needs one written (G-c Reply 2, answer 4)

# G-c.8 - from the discovery report (Reply 9)

Reply 9 decisions: rehost old mods, link active ones; only mods with levels (a Stage folder); `category` and `length` on every entry, filtered in the Patch Manager later.

- `midnightwii` is **Mario's Midnight Adventure** (renamed; the id stays).
- `smma` -> **`super-mario-mushroom-adventure-plus`** (a short id collides).
- Awesomer Super Luigi Mini: the 2013 version is defunct; its new version is on Horizon (2024-03-10, the index showed "Awesome Super Luigi World peaks") - needs its download link.
- Newer Luigi Country Wii (`koopa-country`), Newer SunMoon Vacation (`super-mario-vacation`), Super Luigi Wii: The Emissary (`slwii-the-emissary`): the same mods, newer posts on Horizon without a link in the index.
- New Super Luigi Wii Another Timeline and Super Luigi Midnight Isle are mods of their own (no download found yet).
- NSMBWer+ became **PropelParts** (`propelparts`, linked); `nsmbwer-plus` stays as the old release. The NSMBWer+ copies on GitHub are left out.
- Super Mario Bros. Extreme Adventure is also on GitHub (TeamAlternative2023/SMBEA, TeamAlternative2026/Super-Mario-Bros-Extreme-Adventure, release 1.301 - the catalog's version): the entry could become linked-release to the newer repository.
- Left out as tools without levels: Practice Mode, ILs Mod, NSMBW TAS mod, BetterIGT, ShakeWithB, BetterSMBW, Advanced Physics Patch, Pipe Randomizer.

## New entries (73)

Made by `_workspace/tools/g_c/convert_candidates.py` from each zip's file list (GitHub: the source tree). Names, authors and categories are read, not known - check them. **Def**: `in-mod` = the mod ships a Reginald definition.

| id | Name | Source | Code | Def | Size |
|---|---|---|---|---|---|
| `a-new-kaizo-era-wip` | A New Kaizo Era WIP | hosted archive.org | None | generated | 67 MB |
| `andy-afros-8-new-super-mario-bros-wii` | Andy Afros 8 New Super Mario Bros.Wii | hosted archive.org | kamek | generated | 289 MB |
| `bowsers-new-recruit` | Bowsers New Recruit | hosted archive.org | newer-custom | generated | 456 MB |
| `chaos-station-v2` | Chaos Station v2 | linked-release Stecca6663/ChaosStation-Wii | None | generated | 282 MB |
| `clarissa-s-crack-hack` | Clarissa's crack hack | hosted archive.org | None | generated | 308 MB |
| `clue4u-s-ultra-epic-mod-demo` | Clue4u's Ultra Epic Mod Demo!!! | hosted archive.org | None | generated | 7 MB |
| `coldpipes-colder-pipe-colors` | Coldpipes - Colder Pipe Colors | hosted archive.org | None | generated | 6 MB |
| `cooler-super-mario-bros-land-demo-1-savannah` | COOLER Super Mario Bros. Land Demo 1 Savannah | hosted archive.org | newer-custom | generated | 179 MB |
| `custom-super-mario-bros-wii-halloween-special` | Custom Super Mario Bros. Wii Halloween Special | hosted archive.org | newer-1.2.0 | generated | 302 MB |
| `depot-smbw-smdylan-edition-2024-latest` | Depot SMBW SMDylan Edition 2024 Latest | hosted archive.org | None | generated | 203 MB |
| `evil-dark-moon` | Evil Dark Moon | hosted archive.org | newer-custom | generated | 428 MB |
| `familiar-super-mario-bros-wii` | Familiar Super Mario Bros Wii | hosted archive.org | None | generated | 7 MB |
| `forever-alone-beta` | Forever Alone (BETA) | hosted archive.org | None | generated | 31 MB |
| `harder-mario-bros-meltdown` | Harder Mario Bros. Meltdown | hosted archive.org | None | generated | 12 MB |
| `harder-mario-bros-wii` | Harder Mario Bros. Wii | hosted archive.org | None | generated | 15 MB |
| `impossible-new-super-mario-bros-wii` | Impossible New Super Mario Bros. Wii | hosted archive.org | None | generated | 16 MB |
| `koopatlas-2-0` | Koopatlas 2.0 | linked-source Ethan-mariofan/Koopatlas-2.0 | newer-custom | generated |  |
| `luigi-s-quest` | Luigi's Quest | hosted archive.org | newer-custom | generated | 573 MB |
| `mario-goes-to-the-store-buys-a-gallon-of-milk` | Mario Goes to the Store & buys a Gallon of Milk | hosted archive.org | newer-custom | generated | 465 MB |
| `marios-ultimate-2d-adveture-2` | Marios Ultimate 2D Adveture 2 | hosted archive.org | newer-custom | generated | 564 MB |
| `mini-super-mario-bros-wii` | Mini Super Mario Bros Wii | hosted archive.org | None | generated | 9 MB |
| `new-epic-super-ultimate-64-minecraft` | New Epic Super Ultimate 64 Minecraft | hosted archive.org | newer-custom | generated | 258 MB |
| `new-super-luigi-wii` | New Super Luigi Wii | linked-release TheRealQueenPixella/New-Super-Luigi-Wii | None | generated | 10 MB |
| `new-super-mario-bros-and-the-8-worlds` | New Super Mario Bros And The 8 Worlds | hosted archive.org | newer-custom | generated | 278 MB |
| `new-super-mario-bros-delta-unfinished` | New Super Mario Bros Delta (unfinished) | hosted archive.org | None | generated | 310 MB |
| `new-super-mario-bros-theta-demo` | New Super Mario Bros. Theta DEMO | hosted archive.org | None | generated | 180 MB |
| `new-super-mario-bros-u-wii-demo` | New Super Mario Bros. U Wii Demo | hosted archive.org | newer-custom | generated | 155 MB |
| `new-super-mario-bros-wii-legacy-demo` | New Super Mario Bros. Wii Legacy Demo | hosted archive.org | newer-1.0.3 | generated | 263 MB |
| `new-super-mario-bros-wii-new-horizons` | New Super Mario Bros. Wii: New Horizons | linked-release TheRealQueenPixella/NSMBW-New-Horizons | newer-custom | generated | 190 MB |
| `new-super-mario-bros-wii-only-up` | New Super Mario Bros.Wii ONLY UP! | hosted archive.org | None | generated | 6 MB |
| `new-super-mario-bros-wiimix-world-1-demo` | New Super Mario Bros. Wiimix WORLD 1 DEMO | hosted archive.org | None | generated | 8 MB |
| `new-super-mario-bros-wiinter` | New Super Mario Bros Wiinter | hosted archive.org | newer-custom | generated | 526 MB |
| `new-super-mario-lost-worlds` | New Super Mario Lost Worlds | linked-source N-I-N-0/NSMLW-Riivolution-Patch | newer-custom | in-mod |  |
| `new-super-spike-wii-release` | New Super Spike Wii Release | hosted archive.org | None | generated | 117 MB |
| `new-super-tropix-bros-wii` | New Super Tropix Bros Wii | hosted archive.org | newer-custom | generated | 544 MB |
| `newer-evolution-mbw` | Newer Evolution MBW | linked-release mrmile/NewerEvoMBW-mod | newer-custom | generated | 1074 MB |
| `newer-super-luigi-dark-moon` | Newer Super Luigi Dark Moon | hosted archive.org | newer-custom | generated | 331 MB |
| `newer-super-mario-and-the-sweet-adventure` | Newer Super Mario And The Sweet Adventure | hosted archive.org | newer-custom | generated | 558 MB |
| `newergem` | NewerGEM | linked-source Developers-Collective/NewerGEM | newer-custom | in-mod |  |
| `newest-super-mario-bros-wii` | Newest Super Mario Bros Wii | hosted archive.org | newer-1.2.0 | generated | 439 MB |
| `novastar-wii` | NovaStar Wii | hosted archive.org | newer-1.30 | generated | 336 MB |
| `nsmb2-1-1-remade-in-nsmbw` | NSMB2 1-1 Remade in NSMBW | hosted archive.org | None | generated | 0 MB |
| `nsmb2-1-castle-remade-in-nsmbw` | NSMB2 1-Castle Remade in NSMBW | hosted archive.org | None | generated | 1 MB |
| `nsmbw-grand-star-mode` | NSMBW Grand Star Mode | hosted archive.org | None | generated | 300 MB |
| `nsmbw-quebec-edition` | NSMBW - QUEBEC EDITION | hosted archive.org | newer-custom | generated | 424 MB |
| `nsmbw-the-green-stars` | NSMBW The Green Stars | linked-source NuoKart/NSMBW-The-Green-Stars | None | generated |  |
| `nsmbw-the-new-worlds-2-levels-only` | NSMBW The New Worlds (2 Levels only) | hosted archive.org | newer-1.30 | generated | 473 MB |
| `ok-super-mario-bros-wii` | OK Super Mario Bros. Wii | hosted archive.org | None | generated | 166 MB |
| `poisons-adventure` | Poisons Adventure | linked-release PoisonRised253/NSMBW-Modifiers | loader | generated | 46 MB |
| `propelparts` | PropelParts | linked-source PropelParts-org/PropelParts | None | in-mod |  |
| `revised-super-mario-bros-wii` | Revised Super Mario Bros. Wii | hosted archive.org | None | generated | 25 MB |
| `revolution-64-remastered` | Revolution 64 (Remastered) | hosted archive.org | newer-1.2.0 | generated | 464 MB |
| `rvlution-revived-2025` | RVlution revived 2025 | hosted archive.org | newer-1.0.3 | generated | 259 MB |
| `rvlution-wii` | RVLution Wii | hosted archive.org | newer-1.0.3 | generated | 257 MB |
| `smbwonder-1-1-reimagined-in-nsmbw` | SMBWonder 1-1 Reimagined in NSMBW | hosted archive.org | None | generated | 1 MB |
| `stretchy-mushies-custom-level-v1` | Stretchy Mushies Custom Level v1 | hosted archive.org | None | generated | 7 MB |
| `stupid-super-mario-bros-wii-beta` | Stupid Super Mario Bros Wii (BETA) | hosted archive.org | None | generated | 192 MB |
| `sunnysmbw` | SunnySMBW | hosted archive.org | None | generated | 55 MB |
| `sunshine-super-mario-bros-paradise` | Sunshine Super Mario Bros Paradise | hosted archive.org | newer-custom | generated | 616 MB |
| `super-mario-bob-omb-blast-boss-rush` | Super Mario Bob-omb Blast Boss Rush | hosted archive.org | newer-custom | generated | 311 MB |
| `super-mario-bob-omb-blast-demo` | Super Mario Bob-omb Blast Demo | hosted archive.org | newer-custom | generated | 195 MB |
| `super-mario-bros-world-adventure` | Super Mario Bros World Adventure | linked-source Ethan-mariofan/Super-Mario-Bros-World-Adventure | newer-custom | generated |  |
| `super-mario-dimension-demo` | Super Mario Dimension Demo | hosted archive.org | loader | generated | 275 MB |
| `super-mario-green-star-groove-demo-version-2` | Super Mario Green Star Groove Demo Version 2 | hosted archive.org | newer-custom | generated | 297 MB |
| `super-mario-insane-islands` | Super Mario Insane Islands | hosted archive.org | newer-custom | generated | 713 MB |
| `super-mario-jungle-jam` | Super Mario Jungle Jam | hosted archive.org | None | generated | 70 MB |
| `super-mario-new-2d-lands-world-1` | Super Mario New 2D Lands World 1 | hosted archive.org | newer-custom | generated | 584 MB |
| `the-curse-of-black-toad-all-regions` | The Curse of Black Toad All regions | hosted archive.org | None | generated | 23 MB |
| `the-legend-of-yoshi` | The Legend Of Yoshi | hosted archive.org | None | generated | 151 MB |
| `thiagomod-trio` | ThiagoMod Trio | hosted archive.org | None | generated | 36 MB |
| `timmybroswii` | TimmyBrosWii | hosted archive.org | None | generated | 6 MB |
| `ultimate-super-minecraft-tp` | Ultimate Super Minecraft TP | hosted archive.org | None | generated | 146 MB |
| `you-super-mario-bros-me-summer-special` | You Super Mario Bros Me Summer Special | hosted archive.org | None | generated | 105 MB |

## Skipped (49)

| What | Why |
|---|---|
| CLF78/NSMASR-v2 | no NSMBW XML with its Stage folder |
| TeamAlternative2023/SMBEA | the catalog has this mod already (another copy) |
| mkwcat/nsmbw-project | no levels (its XML maps no Stage folder) |
| Blue Toad over Yellow Toad | its XML maps a Stage folder the zip does not have |
| Clue4u's Ultra Epic Mod SECOND DEMO!!! | another version or copy of a mod already in |
| Depot SMBW SMDylan Edition 2024 v1.1.2 | another version or copy of a mod already in |
| Depot SMBW SMDylan Edition 2024 v1.1.1 | another version or copy of a mod already in |
| Different Yoshi Colors | no levels (its XML maps no Stage folder) |
| Evil Dark Moon 1.1 | another version or copy of a mod already in |
| Evil Dark Moon 1.0 | another version or copy of a mod already in |
| Harder Mario Bros. Meltdown v1.0.0 | another version or copy of a mod already in |
| Hoshimachi Suisei and Iono in NSMBW | its XML maps a Stage folder the zip does not have |
| Midis Super Mario Bros. Wii Just a Little Adventure | no levels (its XML maps no Stage folder) |
| Ness AND Lucas in New Super Mario Bros Wii! | its XML maps a Stage folder the zip does not have |
| New Super Cartoon Beatbox Battles Wii | its XML maps a Stage folder the zip does not have |
| New Super Luigi Wii - DEMO link | its XML maps a Stage folder the zip does not have |
| New Super Mario Bros. Wii 4 made by Orange-Yoshi3.3 | its XML maps a Stage folder the zip does not have |
| New Super Mario Bros Wiinter v1.0 | another version or copy of a mod already in |
| Newer Evolution Mario Bros Wii - Part 1 | another version or copy of a mod already in |
| Newer Beta Goldwood Forest World Map | no levels (its XML maps no Stage folder) |
| Newer Super Mario Bros Wii 7 | an older release of Newer (newer-smbw) |
| Newer Super Mario Bros. Wii V1.30 | an older release of Newer (newer-smbw) |
| Newer Super Mario Bros Wii v1.2.0 | an older release of Newer (newer-smbw) |
| Newer Super Mario Bros. Wii v1.1.1 | an older release of Newer (newer-smbw) |
| Newer Super Mario Bros. Wii v1.0.3 | an older release of Newer (newer-smbw) |
| Newer Super Mario Bros. Wii v1.0.2 | an older release of Newer (newer-smbw) |
| Newer Super Mario Bros. Wii v1.0.1 | an older release of Newer (newer-smbw) |
| Newer Super Mario Bros. Wii v1.0.1 Patch | an older release of Newer (newer-smbw) |
| NewerGEM | another version or copy of a mod already in |
| Newest Super Mario Bros WII V1.02 | another version or copy of a mod already in |
| NewSuperGanondorfWii | its XML maps a Stage folder the zip does not have |
| Normal Super Mario Bros. Wii Demo | its XML maps a Stage folder the zip does not have |
| NSMBW Superstar Mode Version 2 Demo | its XML maps a Stage folder the zip does not have |
| NSMBWerPlus | NSMBWer+ (nsmbwer-plus) |
| NSMBwii-HashedDemo | its XML maps a Stage folder the zip does not have |
| Parappa Frog Hats v2 | its XML maps a Stage folder the zip does not have |
| Playable Funky Kong! | its XML maps a Stage folder the zip does not have |
| Quagsire over Mario (From GameBanana) | no levels (its XML maps no Stage folder) |
| Riivolution NSMBW Wario & Waluigi | its XML maps a Stage folder the zip does not have |
| Snowy Super Luigi. Wii | its XML maps a Stage folder the zip does not have |
| Sonic over Mario Riivolution | its XML maps a Stage folder the zip does not have |
| Stanley in NSMB Wii (From GameBanana) | its XML maps a Stage folder the zip does not have |
| Super Classic Mario Bros. Wii | its XML maps a Stage folder the zip does not have |
| Super Mario Adventure Awaits | its XML maps a Stage folder the zip does not have |
| Super Mario Green Star Groove Demo | another version or copy of a mod already in |
| Super Sonic Over Mario (Riivolution) (byVictorFco) (From Gam | its XML maps a Stage folder the zip does not have |
| Yellow Toad over Blue Toad v0.3 | its XML maps a Stage folder the zip does not have |
| Yellow Toad over Blue Toad v0.2 | its XML maps a Stage folder the zip does not have |
| Yellow Toad over Blue Toad v0.1 | its XML maps a Stage folder the zip does not have |
