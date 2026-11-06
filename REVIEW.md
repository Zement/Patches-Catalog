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
