; BN1 (US AREE): show the current area name in a box at the bottom-right of the pause menu,
; like BN2. prebuild.py renders every label into labels.bin (see names.py for the names).
; Addresses come from ../bn1_shared/addresses.asm (include it first). The data goes at
; AREALABELS_SPACE, after the chip-code mod's, so both mods fit in one ROM.
; BG0 tiles 0x2CA..0x2EB (max 17*2). Only BG0 can address 0xC000-0xDFFF (BG1/2 tiles end at 0x8000,
; BG3's at 0xC000, screens start at 0xE000); the menu uses 0x240-0x2BC and the overworld leaves data in
; 0x2BD-0x2C8, so start after that. (0x0600A000 was first tried and corrupted BG3 field tiles.)
LABEL_VRAM      equ 0x06008000 + 0x2CA*32
BOX_Y           equ 16

; --- Hook the Zenny box drawer (pause menu, every frame) ---------------------
; AL_HOOK+0: push {r5,lr}            (kept)
; AL_HOOK+2: ldrb r0,[r5,4] / sub r0,4 / cmp r0,0 / ble <pop {r5,pc}> / mov r1,0x1E
; AL_HOOK+C: sub r0,r1,r0 ...        (resume here; expects r0 = slide offset, r1 = 0x1E)
.org AL_HOOK + 2
.thumb
    ldr     r7, [pc, 4]
    bx      r7
    nop
.org AL_HOOK + 8
    .word   label_hook|1

.org AREALABELS_SPACE
.align 4
.thumb
label_hook:
    ldrb    r0, [r5, 4]
    sub     r0, 4
    cmp     r0, 0
    ble     @@skip
    push    r0, r5
    bl      draw_label
    pop     r0, r5
    mov     r1, 0x1E
    ldr     r7, =(AL_HOOK + 0xC)|1
    bx      r7
@@skip:                             ; vanilla: ble -> pop {r5,pc}
    pop     r5
    pop     r7
    bx      r7

; in: r0 = slide offset (1 = just appearing, 9+ = fully in)
draw_label:
    push    r14
    cmp     r0, 9
    ble     @@clamped
    mov     r0, 9
@@clamped:
    mov     r6, r0

    ; find (area, subarea) in the lookup table
    ldr     r3, =AREA
    ldrb    r1, [r3]
    ldrb    r2, [r3, 1]
    ldr     r3, =labels
@@find:
    ldrb    r4, [r3]
    cmp     r4, 0xFF
    beq     @@ret                   ; no label for this area
    cmp     r4, r1
    bne     @@next
    ldrb    r4, [r3, 1]
    cmp     r4, r2
    beq     @@found
@@next:
    add     r3, 8
    b       @@find
@@found:
    ldr     r4, [r3, 4]
    ldr     r3, =labels
    add     r4, r4, r3              ; r4 = record
    ldrb    r7, [r4]                ; r7 = width in tiles

    ; upload the two middle rows (wt*2 tiles) to VRAM
    lsl     r0, r7, 3
    add     r0, 4
    add     r0, r0, r4              ; src = record + 4 + tilemap (wt*4*2 bytes)
    ldr     r1, =LABEL_VRAM
    lsl     r2, r7, 6               ; wt * 2 * 32 bytes
@@copy:
    ldmia   r0!, {r3}
    stmia   r1!, {r3}
    sub     r2, 4
    bgt     @@copy

    ; x = 30 - offset*wt/9 so the box slides in with the Zenny box and ends flush right
    mov     r0, r6
    mul     r0, r7
    mov     r1, 9
    swi     6                       ; r0 = r0 / r1
    mov     r1, 30
    sub     r0, r1, r0
    mov     r1, BOX_Y
    mov     r2, 0
    add     r3, r4, 4               ; tilemap
    mov     r4, r7
    mov     r5, 4
    ldr     r7, =BLIT_MAP|1
    bl      @@call_r7
@@ret:
    pop     r0
    bx      r0
@@call_r7:
    bx      r7
.pool

.align 4
labels:
    .import "labels.bin"
