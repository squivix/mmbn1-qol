; BN1 (US AREE): show each chip's code letter on its icon in the Custom Screen.
; Run gen_glyphs.py first (build.ps1 does this automatically via prebuild.py).
.gba
.relativeinclude on
.open ROM_IN, ROM_OUT, 0x08000000
.include "../bn1_shared/addresses.asm"
.include "chipcodes.asm"
.close
