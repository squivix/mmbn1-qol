Mega Man Battle Network - Quality of Life Patches                       v1.0       
==================================================================================

Two small fixes for Mega Man Battle Network 1 (GBA), borrowed from what the later
games do:

  * Chip codes on the Custom Screen
    Every chip in the Custom Screen shows its code letter in the corner of its icon,
    so you no longer have to move the cursor over each chip to see it. Works for all
    rows (after ADD), and the letter greys out with the chip when it can't be picked.

  * Area names in the pause menu
    The pause menu shows where you are in a box at the bottom-right, like BN2
    ("Internet 3", "Undernet 7", "WWW Comp 2", "Lan's Room", ...). It slides in with
    the Zenny box and uses the game's own font. Covers the whole Net, every comp and
    homepage, and the real-world rooms.


Files
-----
  bn1_qol_us / bn1_qol_eu                 both fixes (use this one)
  bn1_chipcodes_us / bn1_chipcodes_eu     chip codes only
  bn1_arealabels_us / bn1_arealabels_eu   area names only

Each comes as .bps and .ips. "_us" is for the American ROM, "_eu" for the European
one (see below). Apply ONE patch. The separate ones exist in case you only want one
of the fixes.


Required ROM
------------
  _us patches:  Mega Man Battle Network (USA)
                Game code AREE, revision 0, 8,388,608 bytes
                CRC32  1D347971
                SHA-1  a4fbae389654a6611d0597b1e9109cbbd32a132f

  _eu patches:  Mega Man Battle Network (Europe)
                Game code AREP, revision 0, 8,388,608 bytes
                CRC32  1A7FB4FA
                SHA-1  b017b6054ffafc012be9adee785819b17706cabc

The Legacy Collection is not supported.


How to patch
------------
  .bps (recommended - refuses to patch the wrong ROM):
    Floating IPS (Flips), Rom Patcher JS (https://www.marcrobledo.com/RomPatcher.js/),
    or mGBA directly: File > Load patch.
  .ips (for Lunar IPS and older tools - does NOT check the ROM, so verify the CRC32 above;
         a _us patch on the European ROM, or the other way round, will break the game).

Patch a copy of your ROM. Existing save files keep working: the patches change no
save data.


Known limitations
-----------------
  * Area names are shortened in a few places to fit the box (e.g. "Traffic Comp 1"
    instead of "Traffic Light Comp 1", "Plant Elevator").
  * A handful of rarely-visited rooms may have no name; the box is simply not shown there.


Credits
-------
  Area IDs:      vgperson's MMBN Save Editor (github.com/vgperson/MMBNSaveEditor)
  Area names:    The Rockman EXE Zone wiki
  Text table:    Prof. 9's TextPet (github.com/Prof9/TextPet)
  Chip data:     StraDaMa's mmbn-chip-tables (github.com/StraDaMa/mmbn-chip-tables)
  Tools:         armips (Kingcom), Floating IPS (Alcaro), mGBA (endrift), Ghidra
