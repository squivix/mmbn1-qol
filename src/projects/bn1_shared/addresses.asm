; BN1 addresses per region. build.ps1 passes REGION ("us" / "eu") from base_rom.txt.
; EU addresses were mapped from US with tools/sigport.py and checked by hand: code is shifted
; (+0x4 / +0xC / +0x14C depending on the bank); RAM layout and the ROM data bank are identical.

.if REGION == "us"          ; Mega Man Battle Network (USA)    AREE  CRC32 1D347971
    BX_R2               equ 0x080004C4  ; an existing "bx r2" halfword, used as a long-call veneer
    BLIT_MAP            equ 0x080022BC  ; (x, y, layer, src, w, h) -> BG tilemap
    CC_HOOK             equ 0x08016328  ; Custom Screen grid: icon copy for one slot
    COPY_WORDS          equ 0x0809DF50  ; (src, dst, CpuSet-style ctrl)
    AL_HOOK             equ 0x08019414  ; pause menu: Zenny box drawer
    CHIPCODES_SPACE     equ 0x087BD1D8  ; start of free space
    AREALABELS_SPACE    equ 0x087C0000
.elseif REGION == "eu"      ; Mega Man Battle Network (Europe) AREP  CRC32 1A7FB4FA
    BX_R2               equ 0x080004C8
    BLIT_MAP            equ 0x080022C8
    CC_HOOK             equ 0x08016334
    COPY_WORDS          equ 0x0809E09C
    AL_HOOK             equ 0x08019560
    CHIPCODES_SPACE     equ 0x087C1760  ; EU has more data at the end of the ROM
    AREALABELS_SPACE    equ 0x087C4000
.else
    .error "REGION must be us or eu (set it in base_rom.txt)"
.endif

; Same in both regions
ICON_STAGE      equ 0x030025E0      ; Custom Screen icons, 15 slots * 0x80 bytes, later sent to VRAM
HAND_SLOTS      equ 0x02004910      ; slot -> folder pile index (0xFF = empty)
AREA            equ 0x02000214      ; u8 area, u8 subarea
