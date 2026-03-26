"""
Generate a cute frog on a lily pad pixel art.
Recreated from reference image. Maps to quilt patch numbers.
"""
from PIL import Image, ImageDraw

COLS = 250  # quilt grid columns

# Color palette
T  = None            # transparent
DG = "#1A6B3C"       # dark green (outlines, shadows)
MG = "#3E8B57"       # medium green (mid-tones)
LG = "#7EC87E"       # light green (body)
VL = "#B5E6A3"       # very light green (belly highlights)
YG = "#C8E6A0"       # yellow-green (lightest highlight)
BK = "#222222"       # black (eyes, mouth)
W  = "#FFFFFF"       # white (eye shine)
PK = "#F28C9A"       # pink (blush cheeks)
BL = "#4A9FD9"       # blue (water)
LB = "#7BBFEA"       # light blue (water highlight)
YL = "#F9C74F"       # yellow (crown/flower)
DY = "#E8A830"       # darker yellow (crown base)
LP = "#5EAD5E"       # lily pad green
DL = "#2D7A2D"       # dark lily pad

# 18 wide × 18 tall frog on lily pad
frog = [
    # 0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17
    [T,  T,  T,  T,  DG, DG, DG, DG, T,  T,  DG, DG, DG, DG, T,  T,  T,  T ],  # row 0: eye bumps top
    [T,  T,  T,  DG, DG, MG, MG, DG, DG, DG, DG, MG, MG, DG, DG, T,  T,  T ],  # row 1: eye bumps
    [T,  T,  T,  DG, BK, BK, MG, DG, MG, MG, DG, MG, BK, BK, DG, T,  T,  T ],  # row 2: eyes top
    [T,  T,  T,  DG, BK, W,  BK, DG, LG, LG, DG, BK, W,  BK, DG, T,  T,  T ],  # row 3: eyes with shine
    [T,  T,  T,  DG, BK, BK, BK, DG, YG, YG, DG, BK, BK, BK, DG, T,  T,  T ],  # row 4: eyes bottom
    [T,  T,  DG, DG, LG, LG, LG, LG, LG, LG, LG, LG, LG, LG, DG, DG, T,  T ],  # row 5: upper face
    [T,  T,  DG, LG, LG, PK, LG, LG, LG, LG, LG, LG, PK, LG, LG, DG, T,  T ],  # row 6: cheeks + blush
    [T,  T,  DG, LG, LG, LG, LG, BK, BK, BK, LG, LG, LG, LG, LG, DG, T,  T ],  # row 7: mouth
    [T,  T,  DG, DG, LG, LG, LG, LG, LG, LG, LG, LG, LG, LG, DG, DG, T,  T ],  # row 8: chin
    [T,  T,  DG, MG, DG, DG, LG, LG, VL, VL, LG, LG, DG, DG, MG, DG, YL, T ],  # row 9: upper body + crown
    [T,  BL, DG, MG, MG, DG, LG, VL, VL, VL, VL, LG, DG, MG, MG, DG, YL, YL],  # row 10: body + crown
    [T,  BL, DG, DG, MG, DG, LG, VL, YG, YG, VL, LG, DG, MG, DG, DG, DY, T ],  # row 11: belly highlight
    [BL, BL, DG, MG, DG, LG, LG, LG, VL, VL, LG, LG, LG, DG, MG, DG, T,  T ],  # row 12: lower body
    [BL, BL, BL, DG, DG, LG, MG, LG, LG, LG, LG, MG, LG, DG, DG, T,  T,  T ],  # row 13: hands/feet
    [BL, BL, BL, DG, LP, LP, DG, LP, LP, LP, LP, DG, LP, LP, LP, DG, T,  T ],  # row 14: lily pad top
    [T,  BL, BL, DG, LP, LP, LP, LP, DL, LP, LP, LP, LP, LP, LP, DG, BL, T ],  # row 15: lily pad mid
    [T,  BL, BL, BL, DG, DG, LP, LP, LP, LP, LP, LP, DG, DG, DG, BL, BL, T ],  # row 16: lily pad bottom
    [T,  T,  BL, BL, BL, BL, DG, DG, DG, DG, DG, DG, BL, BL, BL, BL, T,  T ],  # row 17: water bottom
]


def count_pixels(grid):
    return sum(1 for row in grid for cell in row if cell is not None)

def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_patch_number(row, col):
    return (row * COLS) + col + 1

pixel_count = count_pixels(frog)
print(f"Total pixels: {pixel_count}")

# Show per-row counts
for i, row in enumerate(frog):
    rc = sum(1 for c in row if c is not None)
    print(f"  Row {i}: {rc} pixels")

# Generate image
grid = frog
rows = len(grid)
cols = max(len(r) for r in grid)
pixel_size = min(13, 250 // max(rows, cols))
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

fname = "/home/user/quilttracker/pixel_art_frog.png"
img.save(fname)
print(f"\nImage saved: {fname} ({width}×{height}px)")

# Patch mapping - place at row 60, col 115
START_ROW = 60
START_COL = 115

color_names = {
    DG: "Dark Green (outline)",
    MG: "Medium Green (mid-tone)",
    LG: "Light Green (body)",
    VL: "Very Light Green (belly)",
    YG: "Yellow-Green (highlight)",
    BK: "Black (eyes/mouth)",
    W:  "White (eye shine)",
    PK: "Pink (blush)",
    BL: "Blue (water)",
    LB: "Light Blue (water)",
    YL: "Yellow (crown)",
    DY: "Dark Yellow (crown)",
    LP: "Lily Pad Green",
    DL: "Dark Lily Pad",
}

print(f"\n{'=' * 65}")
print(f"  CUTE FROG ON LILY PAD")
print(f"  Total pixels: {pixel_count}")
print(f"  Grid size: {cols}×{rows}")
print(f"  Quilt position: Row {START_ROW}, Col {START_COL}")
start_patch = get_patch_number(START_ROW, START_COL)
end_patch = get_patch_number(START_ROW + rows - 1, START_COL + cols - 1)
print(f"  Patch range: #{start_patch} – #{end_patch}")
print(f"{'=' * 65}")

# Collect all patches
all_patches = []
patches_by_color = {}
for r, row in enumerate(grid):
    for c, color in enumerate(row):
        if color is not None:
            pnum = get_patch_number(START_ROW + r, START_COL + c)
            all_patches.append((pnum, color))
            patches_by_color.setdefault(color, []).append(pnum)

print(f"\n  COLOR SUMMARY:")
for color, pnums in sorted(patches_by_color.items(), key=lambda x: -len(x[1])):
    name = color_names.get(color, color)
    print(f"    {color}  {name}: {len(pnums)} patches")

print(f"\n{'─' * 65}")
print(f"  COMPLETE PATCH LIST — Patch # | Color Hex | Color Name")
print(f"{'─' * 65}")
for pnum, color in all_patches:
    name = color_names.get(color, color)
    print(f"  Patch #{pnum:<6} │ {color}  │ {name}")
