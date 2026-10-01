; BN1: show each chip's code letter on its icon in the Custom Screen.
; Addresses come from ../bn1_shared/addresses.asm (include it first).

; --- Hook the Custom Screen grid icon copy -----------------------------------
; Vanilla CC_HOOK (US 0x08016328):
;   ldr r2,=ICON_STAGE / lsl r1,r1,7 / add r1,r1,r2   ; r1 = stage + slot*0x80
;   ldr r2,=0x04000020 / bl COPY_WORDS                ; copy 0x20 words of icon
; We keep the first three, make the pool word for the 4th load our hook, and
; turn the bl into a bl to the "bx r2" veneer. r6 == 1 means a real chip icon.
.org CC_HOOK + 0x4C                 ; literal pool word loaded at CC_HOOK+6
    .word   icon_hook|1
.org CC_HOOK + 8
.thumb
    bl      BX_R2

.org CHIPCODES_SPACE
.align 4
.thumb
; in: r0 = icon src, r1 = dst in ICON_STAGE, r6 = 1 if real chip
icon_hook:
    push    r4-r7,r14
    mov     r4, r1                  ; dst
    ldr     r2, =0x04000020
    ldr     r3, =COPY_WORDS|1
    bl      @@call_r3
    cmp     r6, 1
    bne     @@done

    ; slot = (dst - ICON_STAGE) / 0x80; code = pile[HAND_SLOTS[slot]].code
    ldr     r0, =ICON_STAGE
    sub     r0, r4, r0
    lsr     r0, r0, 7
    ldr     r1, =HAND_SLOTS
    ldrb    r0, [r1, r0]
    cmp     r0, 0xFF
    beq     @@done
    mov     r1, r10
    ldr     r1, [r1, 8]
    ldr     r1, [r1, 0x30]          ; folder pile (id, code) pairs
    lsl     r0, r0, 1
    add     r1, r1, r0
    ldrb    r0, [r1, 1]             ; code 0x00..0x1A
    cmp     r0, 0x1A
    bhi     @@done

    ; dst[i] = (dst[i] & ~mask[i]) | val[i], 32 words
    lsl     r0, r0, 8               ; 0x100 bytes per glyph
    ldr     r1, =glyphs
    add     r1, r1, r0              ; r1 = val, r1+0x80 = mask
    mov     r5, 0
@@loop:
    ldr     r2, [r4, r5]
    add     r1, 0x80
    ldr     r3, [r1, r5]
    bic     r2, r3
    sub     r1, 0x80
    ldr     r3, [r1, r5]
    orr     r2, r3
    str     r2, [r4, r5]
    add     r5, 4
    cmp     r5, 0x80
    blt     @@loop

@@done:
    pop     r4-r7
    pop     r0
    bx      r0
@@call_r3:
    bx      r3
.pool

.align 4
glyphs:
    .import "glyphs.bin"

; The area-label mod's data follows (AREALABELS_SPACE); never overlap it.
.if . > AREALABELS_SPACE
    .error "chip-code data overflows into the area-label mod's space"
.endif
