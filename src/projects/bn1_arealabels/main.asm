; BN1 (US AREE): show the current area name in a box at the bottom-right of the pause menu,
; like BN2. prebuild.py renders every label into labels.bin (see names.py for the names).
.gba
.relativeinclude on
.open ROM_IN, ROM_OUT, 0x08000000
.include "../bn1_shared/addresses.asm"
.include "arealabels.asm"
.close
