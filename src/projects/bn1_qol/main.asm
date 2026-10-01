; BN1 (US AREE) quality-of-life bundle: every BN1 mod in one ROM.
; Each mod also builds on its own from its own folder.
.gba
.relativeinclude on
.open ROM_IN, ROM_OUT, 0x08000000
.include "../bn1_shared/addresses.asm"
.include "../bn1_chipcodes/chipcodes.asm"     ; chip codes on Custom Screen icons
.include "../bn1_arealabels/arealabels.asm"   ; area name in the pause menu
.close
