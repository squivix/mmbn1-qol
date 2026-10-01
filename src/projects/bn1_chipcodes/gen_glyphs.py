"""Generates glyphs.bin: for each chip code (A-Z, *) a 16x16 4bpp overlay for a chip icon,
as 128 bytes of pixel values followed by 128 bytes of nibble masks (2x2 tiles, row-major, like the icons).

The letter is a 3x5 glyph with a 1px outline, placed at the icon's bottom-right inside the frame.
Palette indices are from the custom-screen icon palette (BG bank 13): 5 = white, 1 = near-black.
"""
import os

FONT = {
    'A': '010 101 111 101 101', 'B': '110 101 110 101 110', 'C': '011 100 100 100 011',
    'D': '110 101 101 101 110', 'E': '111 100 110 100 111', 'F': '111 100 110 100 100',
    'G': '011 100 101 101 011', 'H': '101 101 111 101 101', 'I': '111 010 010 010 111',
    'J': '001 001 001 101 010', 'K': '101 101 110 101 101', 'L': '100 100 100 100 111',
    'M': '101 111 111 101 101', 'N': '110 101 101 101 101', 'O': '010 101 101 101 010',
    'P': '110 101 110 100 100', 'Q': '010 101 101 110 011', 'R': '110 101 110 101 101',
    'S': '011 100 010 001 110', 'T': '111 010 010 010 010', 'U': '101 101 101 101 111',
    'V': '101 101 101 101 010', 'W': '101 101 111 111 101', 'X': '101 101 010 101 101',
    'Y': '101 101 010 010 010', 'Z': '111 001 010 100 111', '*': '101 010 111 010 101',
}
ORDER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ*'   # chip code values 0x00..0x1A
FG, OUTLINE = 5, 1
GX, GY = 10, 8                          # top-left of the 3x5 glyph within the 16x16 icon


def overlay(ch):
    rows = FONT[ch].split()
    on = lambda x, y: 0 <= y < 5 and 0 <= x < 3 and rows[y][x] == '1'
    px = {}
    for y in range(-1, 6):
        for x in range(-1, 4):
            if on(x, y):
                px[(GX + x, GY + y)] = FG
            elif any(on(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                px[(GX + x, GY + y)] = OUTLINE
    val, mask = bytearray(128), bytearray(128)
    for (x, y), c in px.items():
        tile = (y // 8) * 2 + (x // 8)
        i = tile * 32 + (y % 8) * 4 + (x % 8) // 2
        shift = 4 * (x & 1)
        val[i] |= c << shift
        mask[i] |= 0xF << shift
    return bytes(val) + bytes(mask)


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'glyphs.bin')
    with open(out, 'wb') as f:
        for ch in ORDER:
            f.write(overlay(ch))
    print(f'wrote {out} ({len(ORDER)} glyphs)')
