# Source

armips assembly for the patches in this repo. Building reproduces the released patches byte for byte.

## Layout

| Folder | Patch |
|---|---|
| `projects/bn1_chipcodes` | chip codes on the Custom Screen (`chipcodes.asm`; `gen_glyphs.py` draws the code letters) |
| `projects/bn1_arealabels` | area names in the pause menu (`arealabels.asm`; `prebuild.py` renders every label from `names.py`) |
| `projects/bn1_qol` | both |
| `projects/bn1_shared/addresses.asm` | US / EU addresses |

`glyphs.json` (the game's font) and `frame_tiles.bin` (the Zenny box tiles) were captured from the game; the
area-label patch contains the same pixels.

## Building (Windows)

You need:
- Python 3 with Pillow (`pip install pillow`)
- [armips](https://github.com/Kingcom/armips) v0.11 at `tools/armips/armips.exe`
- [Floating IPS](https://github.com/Alcaro/Flips) at `tools/flips/flips.exe`
- your own clean ROMs at `roms/bn1_us.gba` and `roms/bn1_eu.gba` (see the main README for the checksums)

Then, from this folder:

```powershell
.\tools\build.ps1 bn1_qol              # build\bn1_qol_us.gba/.bps and build\bn1_qol_eu.gba/.bps
.\tools\build.ps1 bn1_chipcodes -Region us
```
