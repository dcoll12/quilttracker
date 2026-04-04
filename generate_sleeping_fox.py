"""
Generate a cute sleeping fox pixel art with EXACTLY 250 pixels.
Maps to specific quilt patch numbers on the 250-column grid.
"""
from PIL import Image, ImageDraw

COLS = 250

# Colors
T = None          # transparent
O = "#F3722C"     # dark orange (body)
A = "#F8961E"     # amber/orange (fur)
W = "#FFFFFF"     # white (belly, face)
BK = "#333333"    # black (nose, eyes, outlines)
P = "#F9844A"     # peach (inner ears, cheeks)
Y = "#F9C74F"     # yellow (tail tip)
PK = "#FF69B4"    # pink (blush)
N = "#D2691E"     # brown (paws)

# Sleeping fox curled up - 20 wide × 20 tall = exactly 250 pixels
fox = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, A, A, A, A],  # row 0: tail tip (4)
    [T, T, T, T, T, T, T, T, T, T, T, T, T, A, A, A, Y, Y, A, A],  # row 1: tail (7)
    [T, T, T, T, T, T, T, T, T, T, T, T, A, A, Y, Y, Y, Y, A, T],  # row 2: tail (7)
    [T, T, A, A, T, T, T, T, A, A, A, A, A, A, A, Y, Y, T, T, T],  # row 3: ears + tail (11)
    [T, A, A, A, A, T, T, A, A, A, A, A, A, A, A, A, T, T, T, T],  # row 4: ears (13)
    [T, A, O, P, A, A, T, A, P, O, A, A, A, A, A, A, T, T, T, T],  # row 5: inner ears (13)
    [A, A, O, O, A, A, A, A, O, O, A, A, A, A, A, T, T, T, T, T],  # row 6: head top (15)
    [A, O, O, O, O, O, O, O, O, O, O, A, A, A, T, T, T, T, T, T],  # row 7: head (14)
    [A, O, O, W, W, O, O, W, W, O, O, A, A, T, T, T, T, T, T, T],  # row 8: eyes area (13)
    [A, O, W, BK,W, W, W, W, BK,W, O, O, A, T, T, T, T, T, T, T],  # row 9: closed eyes (13)
    [A, O, O, W, W, W, W, W, W, O, O, A, A, T, T, T, T, T, T, T],  # row 10: cheeks (13)
    [A, O, O, PK,W, W, W, W, PK,O, O, A, A, T, T, T, T, T, T, T],  # row 11: blush (13)
    [A, O, O, O, W, BK,BK,W, O, O, O, A, A, T, T, T, T, T, T, T],  # row 12: nose (13)
    [T, A, A, O, O, W, W, O, O, O, A, A, A, T, T, T, T, T, T, T],  # row 13: chin (13)
    [T, A, A, A, O, O, O, O, O, O, A, O, A, A, A, T, T, T, T, T],  # row 14: body start (15)
    [T, T, T, A, A, O, O, O, O, A, A, O, O, A, A, A, A, A, T, T],  # row 15: body curl (15)
    [T, T, T, A, A, A, A, A, A, O, O, O, O, O, A, A, A, A, T, T],  # row 16: body (15)
    [T, T, T, T, N, N, N, A, O, O, W, W, O, O, O, O, A, A, A, T],  # row 17: paws + belly (15)
    [T, T, T, T, N, N, N, A, O, W, W, W, W, O, O, O, O, A, A, T],  # row 18: paws + belly (15)
    [T, T, T, T, T, A, A, A, A, O, O, O, O, O, O, O, A, A, A, T],  # row 19: bottom (15)
]

def count_pixels(grid):
    return sum(1 for row in grid for cell in row if cell is not None)

def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_patch_number(row, col):
    return (row * COLS) + col + 1

# Count and verify
pixel_count = count_pixels(fox)
print(f"Pixel count: {pixel_count}")

if pixel_count != 250:
    print(f"ERROR: Need exactly 250, got {pixel_count}. Difference: {250 - pixel_count}")
    # Show per-row counts to help debug
    for i, row in enumerate(fox):
        rc = sum(1 for c in row if c is not None)
        print(f"  Row {i}: {rc} pixels")
    exit(1)

print("EXACTLY 250 pixels! Generating image...")

# Generate image
grid = fox
rows = len(grid)
cols = max(len(r) for r in grid)
pixel_size = min(12, 250 // max(rows, cols))
pixel_size = max(pixel_size, 1)

width = cols * pixel_size
height = rows * pixel_size

img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

for r, row in enumerate(grid):
    for c, color in enumerate(row):
        if color is not None:
            rgb = hex_to_rgb(color)
            x1 = c * pixel_size
            y1 = r * pixel_size
            x2 = x1 + pixel_size - 1
            y2 = y1 + pixel_size - 1
            draw.rectangle([x1, y1, x2, y2], fill=rgb + (255,))

fname = "/home/user/quilttracker/pixel_art_sleeping_fox.png"
img.save(fname)
print(f"Image saved: {fname} ({width}×{height}px)")

# Patch mapping - place at row 50, col 110 (center-ish on quilt)
START_ROW = 50
START_COL = 110

print(f"\n{'=' * 60}")
print(f"  SLEEPING FOX - Exactly 250 Patches")
print(f"  Quilt position: Row {START_ROW}, Col {START_COL}")
print(f"  Grid size: {cols}×{rows}")
print(f"{'=' * 60}")

patches_by_color = {}
all_patches = []

for r, row in enumerate(grid):
    for c, color in enumerate(row):
        if color is not None:
            pnum = get_patch_number(START_ROW + r, START_COL + c)
            all_patches.append((pnum, color))
            patches_by_color.setdefault(color, []).append(pnum)

color_names = {
    "#F3722C": "Dark Orange (body)",
    "#F8961E": "Amber (fur)",
    "#FFFFFF": "White (face/belly)",
    "#333333": "Black (eyes/nose)",
    "#F9844A": "Peach (inner ears)",
    "#F9C74F": "Yellow (tail tip)",
    "#FF69B4": "Pink (blush)",
    "#D2691E": "Brown (paws)",
}

print(f"\n  PATCHES BY COLOR:")
for color, pnums in sorted(patches_by_color.items(), key=lambda x: -len(x[1])):
    name = color_names.get(color, color)
    print(f"\n  {color} - {name} ({len(pnums)} patches):")
    line = "    "
    for i, p in enumerate(pnums):
        line += f"#{p} "
        if (i + 1) % 10 == 0:
            print(line)
            line = "    "
    if line.strip():
        print(line)

print(f"\n  COMPLETE PATCH LIST (all 250):")
for i, (pnum, color) in enumerate(all_patches):
    print(f"  Patch #{pnum:>5} → {color}  ({color_names.get(color, '')})")
