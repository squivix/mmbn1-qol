"""Renders every area label offline into labels.bin (read by main.asm). Also writes preview.png.

labels.bin layout (all little-endian, offsets relative to blob start):
  lookup:  { u8 area, u8 subarea, u16 pad, u32 record_offset } ... terminated by area == 0xFF
  record:  u8 width_tiles, u8[3] pad,
           u16 tilemap[4][width]          (BG0 entries, palette 13)
           (align 4) u8 tiles[2][width][32] (the two middle rows: frame + text, 4bpp)

Glyphs (glyphs.json) were captured from the game's own string renderer with font 0x08613AA8;
frame_tiles.bin are the Zenny box tiles 0x2B0-0x2BC from the pause-menu VRAM.
"""
import json
import os
import struct

from PIL import Image

from names import AREAS

HERE = os.path.dirname(os.path.abspath(__file__))
TILE_BASE = 0x2CA        # BG0 tile index for the middle rows (VRAM 0x0600D940); see main.asm
PAL = 0xD000             # palette 13
MAX_TILES = 17           # 30 columns minus the 13-column menu panel
TEXT_FG, TEXT_SHADOW = 1, 3

GLYPHS = json.load(open(os.path.join(HERE, 'glyphs.json')))['glyphs']['font1']
FRAME = open(os.path.join(HERE, 'frame_tiles.bin'), 'rb').read()

# Zenny box tilemap (top-right, 9x4); the label box is this mirrored vertically and widened.
ZENNY = [[0xD6B0, 0xD6B1, 0xD6B2, 0xD6B3, 0xD2B4, 0xD2B3, 0xD2B3, 0xD2B2, 0xD2B1],
         [0xD6B5, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6],
         [0xDEB5, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6, 0xD2B6],
         [0xDEB0, 0xD6B9, 0xD6BA, 0xD6BB, 0xD2BC, 0xD2BB, 0xD2BB, 0xD2BA, 0xD2B9]]


def frame_rows(wt):
    rows = [r[:5] + [r[5]] * (wt - 9) + r[5:] for r in ZENNY]
    return [[e ^ 0x800 for e in r] for r in rows[::-1]]


def tile_pixels(entry):
    t = (entry & 0x3FF) - 0x2B0
    b = FRAME[t * 32:(t + 1) * 32]
    px = [[(b[y * 4 + x // 2] >> (4 * (x & 1))) & 15 for x in range(8)] for y in range(8)]
    if entry & 0x400:
        px = [r[::-1] for r in px]
    if entry & 0x800:
        px = px[::-1]
    return px


def glyph_columns(text):
    cols = []
    for ch in text:
        if ch == ' ':
            cols += [[0] * 16] * 3
            continue
        b = bytes.fromhex(GLYPHS[ch])
        cell = [[(b[h * 32 + y * 4 + x // 2] >> (4 * (x & 1))) & 15 for x in range(8)]
                for h in range(2) for y in range(8)]
        xs = [x for y in range(16) for x in range(8) if cell[y][x] == 3]
        for x in range(min(xs), max(xs) + 1):
            cols.append([1 if cell[y][x] == 3 else 0 for y in range(16)])
        cols.append([0] * 16)
    return cols[:-1]


def render(text):
    cols = glyph_columns(text)
    tw = len(cols)
    wt = max(9, (tw + 18 + 7) // 8)
    if wt > MAX_TILES:
        raise SystemExit(f'label too wide ({tw}px, {wt} tiles): {text!r}')
    rows = frame_rows(wt)
    # middle two rows as a pixel canvas (16 x wt*8), starting from the frame graphics
    canvas = [[0] * (wt * 8) for _ in range(16)]
    for r in (1, 2):
        for tx, e in enumerate(rows[r]):
            px = tile_pixels(e)
            for y in range(8):
                for x in range(8):
                    canvas[(r - 1) * 8 + y][tx * 8 + x] = px[y][x]
    x0 = 12 + ((wt * 8 - 16) - tw) // 2
    for d, color in ((1, TEXT_SHADOW), (0, TEXT_FG)):
        for x, col in enumerate(cols):
            for y, on in enumerate(col):
                if on and 0 <= y + d < 16:
                    canvas[y + d][x0 + x + d] = color
    tiles = bytearray()
    for r in range(2):
        for tx in range(wt):
            for y in range(8):
                row = canvas[r * 8 + y][tx * 8:tx * 8 + 8]
                tiles += bytes(row[i] | (row[i + 1] << 4) for i in range(0, 8, 2))
    tilemap = [rows[0], [PAL | (TILE_BASE + i) for i in range(wt)],
               [PAL | (TILE_BASE + wt + i) for i in range(wt)], rows[3]]
    return wt, tilemap, bytes(tiles), canvas


def main():
    entries = [(a, s, name) for a in sorted(AREAS) for s, name in sorted(AREAS[a].items())]
    unique = sorted({n for _, _, n in entries})
    lookup_size = (len(entries) + 1) * 8
    records, offsets, blob_tail = {}, {}, bytearray()
    for name in unique:
        wt, tilemap, tiles, canvas = render(name)
        rec = bytearray(struct.pack('<B3x', wt))
        for row in tilemap:
            rec += struct.pack(f'<{wt}H', *row)
        while len(rec) % 4:
            rec += b'\0'
        rec += tiles
        offsets[name] = lookup_size + len(blob_tail)
        blob_tail += rec
        records[name] = (wt, canvas)
    blob = bytearray()
    for a, s, name in entries:
        blob += struct.pack('<BBxxI', a, s, offsets[name])
    blob += struct.pack('<BBxxI', 0xFF, 0xFF, 0)
    blob += blob_tail
    open(os.path.join(HERE, 'labels.bin'), 'wb').write(blob)

    # preview sheet of every label's middle rows, for eyeballing
    pal = {0: (40, 40, 40), 1: (255, 246, 205), 3: (49, 57, 57), 0xE: (90, 106, 106)}
    img = Image.new('RGB', (MAX_TILES * 8, 18 * len(unique)), (20, 20, 20))
    for i, name in enumerate(unique):
        wt, canvas = records[name]
        for y in range(16):
            for x in range(wt * 8):
                img.putpixel((x, i * 18 + y), pal.get(canvas[y][x], (200, 120, 40)))
    img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(os.path.join(HERE, 'preview.png'))
    widest = max(unique, key=lambda n: records[n][0])
    print(f'labels.bin: {len(entries)} areas, {len(unique)} labels, {len(blob)} bytes; widest {widest!r} ({records[widest][0]} tiles)')


if __name__ == '__main__':
    main()
