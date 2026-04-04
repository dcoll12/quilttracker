"""
Ultra-premium pixel art designs for $3,500-$10,000 donations.
$20/patch. Big, detailed showpieces.
"""
from PIL import Image, ImageDraw

COLS = 250
PATCH_VALUE = 20
T = None

RED    = "#F94144"; ORANGE = "#F3722C"; AMBER  = "#F8961E"
PEACH  = "#F9844A"; YELLOW = "#F9C74F"; GREEN  = "#90BE6D"
TEAL   = "#43AA8B"; DTEAL  = "#4D908E"; SLATE  = "#577590"
BLUE   = "#277DA1"; WHITE  = "#FFFFFF"; BLACK  = "#333333"
PINK   = "#FF69B4"; PURPLE = "#9B59B6"; LPURP  = "#DDA0DD"
DGREEN = "#1A6B3C"; MGREEN = "#3E8B57"; LGREEN = "#7EC87E"
VLGRN  = "#B5E6A3"; BROWN  = "#8B4513"; LBROWN = "#D2691E"
TAN    = "#DEB887"; GRAY   = "#999999"; LGRAY  = "#CCCCCC"
SKYBL  = "#87CEEB"; CORAL  = "#FF7F50"; MAROON = "#8B0000"
NAVY   = "#1B3A5C"; GOLD   = "#DAA520"; DBLUE  = "#1E5FA8"
LBLUE  = "#5BA3CF"; SAND   = "#F5DEB3"; DGRAY  = "#555555"

designs = {}

# ─── 1. WHALE (20×12, ~175 patches = $3,500) ───
designs["Whale"] = {
    "desc": "Majestic blue whale",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     DBLUE, DBLUE, DBLUE, DBLUE, DBLUE, T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     DBLUE, DBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  DBLUE, DBLUE, T,     T,     T,     T],
        [T,     T,     T,     T,     T,     DBLUE, DBLUE, BLUE,  BLUE,  BLUE,  LBLUE, LBLUE, BLUE,  BLUE,  BLUE,  BLUE,  DBLUE, T,     T,     T],
        [T,     T,     T,     DBLUE, DBLUE, BLUE,  BLUE,  BLUE,  BLUE,  LBLUE, LBLUE, LBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  DBLUE, T,     T],
        [T,     DBLUE, DBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  LBLUE, LBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  DBLUE, T],
        [DBLUE, DBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLACK, BLUE,  BLUE,  BLUE,  DBLUE, T],
        [DBLUE, BLUE,  BLUE,  DBLUE, BLUE,  BLUE,  BLUE,  LBLUE, LBLUE, LBLUE, LBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  DBLUE, T,     T],
        [T,     DBLUE, DBLUE, T,     DBLUE, BLUE,  BLUE,  BLUE,  LBLUE, LBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  DBLUE, T,     T,     T],
        [T,     T,     T,     T,     T,     DBLUE, DBLUE, BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  DBLUE, DBLUE, T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     DBLUE, DBLUE, DBLUE, DBLUE, DBLUE, DBLUE, DBLUE, T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     SKYBL, SKYBL, SKYBL, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     SKYBL, SKYBL, SKYBL, T,     T,     T,     T,     T,     T],
    ]
}

# ─── 2. PANDA (18×18, ~200 patches = $4,000) ───
designs["Panda"] = {
    "desc": "Cute giant panda",
    "grid": [
        [T,     T,     T,     BLACK, BLACK, T,     T,     T,     T,     T,     T,     T,     T,     BLACK, BLACK, T,     T,     T],
        [T,     T,     BLACK, BLACK, BLACK, BLACK, T,     T,     T,     T,     T,     T,     BLACK, BLACK, BLACK, BLACK, T,     T],
        [T,     T,     BLACK, BLACK, BLACK, BLACK, T,     T,     T,     T,     T,     T,     BLACK, BLACK, BLACK, BLACK, T,     T],
        [T,     T,     T,     BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, T,     T,     T],
        [T,     T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T],
        [T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T],
        [T,     WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, T],
        [T,     WHITE, WHITE, BLACK, BLACK, WHITE, BLACK, BLACK, WHITE, WHITE, BLACK, BLACK, WHITE, BLACK, BLACK, WHITE, WHITE, T],
        [T,     WHITE, WHITE, BLACK, WHITE, WHITE, WHITE, BLACK, WHITE, WHITE, BLACK, WHITE, WHITE, WHITE, BLACK, WHITE, WHITE, T],
        [T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T],
        [T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T],
        [T,     T,     WHITE, WHITE, WHITE, WHITE, BLACK, T,     T,     T,     BLACK, WHITE, WHITE, WHITE, WHITE, T,     T,     T],
        [T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T],
        [T,     T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T],
        [T,     T,     T,     T,     BLACK, BLACK, WHITE, WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, T,     T,     T,     T,     T],
        [T,     T,     T,     BLACK, BLACK, BLACK, BLACK, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, BLACK, T,     T,     T,     T],
        [T,     T,     T,     BLACK, BLACK, BLACK, T,     T,     T,     T,     T,     BLACK, BLACK, BLACK, T,     T,     T,     T],
        [T,     T,     T,     T,     BLACK, T,     T,     T,     T,     T,     T,     T,     BLACK, T,     T,     T,     T,     T],
    ]
}

# ─── 3. OCTOPUS (20×20, ~250 patches = $5,000) ───
designs["Octopus"] = {
    "desc": "Kawaii octopus",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T,     T],
        [T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     CORAL, CORAL, WHITE, WHITE, CORAL, CORAL, CORAL, CORAL, CORAL, WHITE, WHITE, CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     CORAL, CORAL, WHITE, BLACK, CORAL, CORAL, CORAL, CORAL, CORAL, WHITE, BLACK, CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, PINK,  PINK,  PINK,  CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     CORAL, CORAL, PINK,  CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, PINK,  CORAL, CORAL, CORAL, T,     T,     T],
        [T,     T,     T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T,     T,     T],
        [T,     T,     CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, CORAL, T,     T],
        [T,     CORAL, CORAL, T,     CORAL, CORAL, T,     CORAL, CORAL, T,     T,     CORAL, CORAL, T,     CORAL, CORAL, T,     CORAL, CORAL, T],
        [CORAL, CORAL, T,     T,     CORAL, CORAL, T,     CORAL, CORAL, T,     T,     CORAL, CORAL, T,     CORAL, CORAL, T,     T,     CORAL, CORAL],
        [CORAL, T,     T,     CORAL, CORAL, T,     T,     T,     CORAL, CORAL, CORAL, CORAL, T,     T,     T,     CORAL, CORAL, T,     T,     CORAL],
        [CORAL, T,     CORAL, CORAL, T,     T,     T,     T,     T,     CORAL, CORAL, T,     T,     T,     T,     T,     CORAL, CORAL, T,     CORAL],
        [CORAL, CORAL, CORAL, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     CORAL, CORAL, CORAL],
        [T,     CORAL, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     CORAL, T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
    ]
}

# ─── 4. PHOENIX (22×22, ~300 patches = $6,000) ───
designs["Phoenix"] = {
    "desc": "Rising phoenix in flames",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     RED,   RED,   T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     RED,   RED,   ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     RED,   ORANGE,YELLOW,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     RED,   ORANGE,YELLOW,ORANGE,RED,   RED,   T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     RED,   ORANGE,YELLOW,YELLOW,YELLOW,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     RED,   RED,   ORANGE,YELLOW,YELLOW,ORANGE,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     RED,   ORANGE,ORANGE,YELLOW,ORANGE,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     RED,   ORANGE,ORANGE,BLACK, ORANGE,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     RED,   RED,   ORANGE,ORANGE,ORANGE,ORANGE,ORANGE,RED,   RED,   T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     RED,   ORANGE,ORANGE,ORANGE,ORANGE,AMBER, ORANGE,ORANGE,ORANGE,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T],
        [T,     T,     RED,   RED,   ORANGE,ORANGE,RED,   ORANGE,AMBER, AMBER, AMBER, ORANGE,RED,   ORANGE,ORANGE,RED,   RED,   T,     T,     T,     T,     T],
        [T,     RED,   ORANGE,ORANGE,ORANGE,RED,   T,     RED,   ORANGE,AMBER, ORANGE,RED,   T,     RED,   ORANGE,ORANGE,ORANGE,RED,   T,     T,     T,     T],
        [RED,   ORANGE,ORANGE,RED,   RED,   T,     T,     RED,   ORANGE,ORANGE,ORANGE,RED,   T,     T,     RED,   RED,   ORANGE,ORANGE,RED,   T,     T,     T],
        [RED,   ORANGE,RED,   T,     T,     T,     T,     T,     RED,   ORANGE,RED,   T,     T,     T,     T,     T,     RED,   ORANGE,RED,   T,     T,     T],
        [RED,   RED,   T,     T,     T,     T,     T,     T,     RED,   ORANGE,RED,   T,     T,     T,     T,     T,     T,     RED,   RED,   T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     RED,   ORANGE,YELLOW,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     RED,   ORANGE,YELLOW,YELLOW,YELLOW,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     RED,   ORANGE,YELLOW,YELLOW,AMBER, YELLOW,YELLOW,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     RED,   ORANGE,YELLOW,YELLOW,AMBER, AMBER, AMBER, YELLOW,YELLOW,ORANGE,RED,   T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     RED,   ORANGE,YELLOW,AMBER, AMBER, RED,   RED,   RED,   AMBER, AMBER, YELLOW,ORANGE,RED,   T,     T,     T,     T,     T,     T],
        [T,     T,     RED,   ORANGE,YELLOW,AMBER, RED,   RED,   T,     T,     T,     RED,   RED,   AMBER, YELLOW,ORANGE,RED,   T,     T,     T,     T,     T],
        [T,     RED,   ORANGE,YELLOW,AMBER, RED,   T,     T,     T,     T,     T,     T,     T,     RED,   AMBER, YELLOW,ORANGE,RED,   T,     T,     T,     T],
    ]
}

# ─── 5. SAILBOAT (22×20, ~275 patches = $5,500) ───
designs["Sailboat"] = {
    "desc": "Sailboat at sunset",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     AMBER, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, WHITE, T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, WHITE, WHITE, T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     WHITE, T,     BROWN, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     WHITE, WHITE, T,     BROWN, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     WHITE, WHITE, WHITE, T,     BROWN, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T,     T],
        [T,     T,     T,     T,     T,     WHITE, WHITE, WHITE, WHITE, T,     BROWN, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T,     T],
        [T,     T,     T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, T,     BROWN, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     T],
        [T,     T,     T,     WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, T,     BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, T],
        [T,     T,     BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, T,     T],
        [T,     T,     T,     BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, T,     T,     T],
        [T,     T,     T,     T,     BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, T,     T,     T,     T],
        [LBLUE, LBLUE, SKYBL, SKYBL, LBLUE, LBLUE, SKYBL, SKYBL, LBLUE, LBLUE, SKYBL, SKYBL, LBLUE, LBLUE, SKYBL, SKYBL, LBLUE, LBLUE, SKYBL, SKYBL, LBLUE, LBLUE],
        [BLUE,  LBLUE, LBLUE, LBLUE, BLUE,  LBLUE, LBLUE, LBLUE, BLUE,  LBLUE, LBLUE, LBLUE, BLUE,  LBLUE, LBLUE, LBLUE, BLUE,  LBLUE, LBLUE, LBLUE, BLUE,  LBLUE],
        [BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE,  BLUE],
    ]
}

# ─── 6. ELEPHANT (22×20, ~300 patches = $6,000) ───
designs["Elephant"] = {
    "desc": "Gentle elephant",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     GRAY,  GRAY,  GRAY,  GRAY,  GRAY,  T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     GRAY,  GRAY,  GRAY,  LGRAY, LGRAY, GRAY,  GRAY,  GRAY,  T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     GRAY,  GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  GRAY,  T,     T,     T,     T,     T],
        [T,     T,     T,     GRAY,  GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  GRAY,  T,     T,     T],
        [T,     T,     GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  T,     T],
        [T,     GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  T],
        [GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, BLACK, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, BLACK, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY],
        [GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY],
        [GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY],
        [GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY],
        [GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  LGRAY, LGRAY, LGRAY, GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY],
        [T,     GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  LGRAY, LGRAY, LGRAY, GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  T],
        [T,     T,     GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  LGRAY, LGRAY, LGRAY, GRAY,  LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  T,     T],
        [T,     T,     T,     GRAY,  GRAY,  LGRAY, LGRAY, GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  LGRAY, LGRAY, LGRAY, GRAY,  GRAY,  T,     T,     T],
        [T,     T,     T,     T,     GRAY,  GRAY,  LGRAY, GRAY,  T,     GRAY,  LGRAY, GRAY,  T,     GRAY,  LGRAY, LGRAY, GRAY,  GRAY,  T,     T,     T,     T],
        [T,     T,     T,     T,     T,     GRAY,  LGRAY, GRAY,  T,     GRAY,  LGRAY, GRAY,  T,     GRAY,  LGRAY, GRAY,  GRAY,  T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     GRAY,  LGRAY, GRAY,  T,     T,     GRAY,  T,     T,     GRAY,  LGRAY, GRAY,  T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     GRAY,  LGRAY, GRAY,  T,     T,     T,     T,     T,     GRAY,  LGRAY, GRAY,  T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     GRAY,  GRAY,  GRAY,  T,     T,     T,     T,     T,     GRAY,  GRAY,  GRAY,  T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     GRAY,  GRAY,  GRAY,  GRAY,  GRAY,  T,     T,     T,     GRAY,  GRAY,  GRAY,  GRAY,  GRAY,  T,     T,     T,     T,     T],
    ]
}

# ─── 7. TREE OF LIFE (24×26, ~500 patches = $10,000) ───
designs["Tree of Life"] = {
    "desc": "Majestic tree of life - the ultimate showpiece",
    "grid": [
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     GREEN, GREEN, GREEN, LGREEN,LGREEN,LGREEN,LGREEN,GREEN, GREEN, GREEN, T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     GREEN, GREEN, GREEN, LGREEN,LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,LGREEN,GREEN, GREEN, GREEN, T,     T,     T,     T,     T],
        [T,     T,     T,     T,     GREEN, GREEN, LGREEN,LGREEN,LGREEN,VLGRN, VLGRN, VLGRN, VLGRN, VLGRN, LGREEN,LGREEN,LGREEN,GREEN, GREEN, T,     T,     T,     T,     T],
        [T,     T,     T,     GREEN, GREEN, LGREEN,LGREEN,VLGRN, VLGRN, VLGRN, LGREEN,LGREEN,VLGRN, VLGRN, VLGRN, LGREEN,LGREEN,LGREEN,GREEN, GREEN, T,     T,     T,     T],
        [T,     T,     GREEN, GREEN, LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,GREEN, GREEN, LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,GREEN, GREEN, T,     T,     T,     T],
        [T,     GREEN, GREEN, LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,GREEN, T,     T,     GREEN, LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,GREEN, GREEN, T,     T,     T],
        [T,     GREEN, LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,GREEN, T,     T,     T,     T,     GREEN, LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,GREEN, T,     T,     T],
        [GREEN, GREEN, LGREEN,VLGRN, VLGRN, LGREEN,LGREEN,GREEN, T,     T,     T,     T,     T,     T,     GREEN, LGREEN,LGREEN,VLGRN, VLGRN, LGREEN,GREEN, GREEN, T,     T],
        [GREEN, LGREEN,LGREEN,VLGRN, LGREEN,LGREEN,GREEN, GREEN, T,     T,     T,     T,     T,     T,     GREEN, GREEN, LGREEN,LGREEN,VLGRN, LGREEN,LGREEN,GREEN, T,     T],
        [GREEN, GREEN, LGREEN,LGREEN,LGREEN,GREEN, GREEN, T,     T,     T,     T,     T,     T,     T,     T,     GREEN, GREEN, LGREEN,LGREEN,LGREEN,GREEN, GREEN, T,     T],
        [T,     GREEN, GREEN, LGREEN,GREEN, GREEN, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     GREEN, GREEN, LGREEN,GREEN, GREEN, T,     T,     T],
        [T,     T,     GREEN, GREEN, GREEN, T,     T,     T,     T,     T,     BROWN, BROWN, BROWN, T,     T,     T,     T,     T,     GREEN, GREEN, GREEN, T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, BROWN, LBROWN,BROWN, BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,LBROWN,BROWN, BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     T,     BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, BROWN, T,     T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,LBROWN,BROWN, BROWN, T,     T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,BROWN, LBROWN,LBROWN,BROWN, LBROWN,LBROWN,LBROWN,BROWN, BROWN, T,     T,     T,     T,     T,     T],
        [T,     T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,BROWN, T,     BROWN, BROWN, T,     BROWN, LBROWN,LBROWN,LBROWN,BROWN, BROWN, T,     T,     T,     T,     T],
        [T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,BROWN, T,     T,     T,     T,     T,     T,     BROWN, LBROWN,LBROWN,LBROWN,BROWN, BROWN, T,     T,     T,     T],
        [T,     T,     BROWN, BROWN, LBROWN,BROWN, BROWN, T,     T,     T,     T,     T,     T,     T,     T,     BROWN, BROWN, LBROWN,LBROWN,BROWN, BROWN, T,     T,     T],
        [T,     BROWN, BROWN, BROWN, BROWN, T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     T,     BROWN, BROWN, BROWN, BROWN, BROWN, T,     T],
        [GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN],
        [DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN,DGREEN],
    ]
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def count(grid):
    return sum(1 for row in grid for c in row if c is not None)

def get_patch(start_patch, r, c):
    idx = start_patch - 1
    base_row = idx // COLS
    base_col = idx % COLS
    return (base_row + r) * COLS + (base_col + c) + 1


print("=" * 60)
print("  ULTRA-PREMIUM QUILT DESIGNS")
print(f"  ${PATCH_VALUE} per patch")
print("=" * 60)

START = 10075

for name, d in designs.items():
    grid = d["grid"]
    px = count(grid)
    cost = px * PATCH_VALUE
    rows = len(grid)
    cols = max(len(r) for r in grid)

    ps = min(10, 250 // max(rows, cols))
    w, h = cols * ps, rows * ps
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color:
                rgb = hex_to_rgb(color)
                draw.rectangle([c*ps, r*ps, (c+1)*ps-1, (r+1)*ps-1], fill=rgb+(255,))
    fname = f"/home/user/quilttracker/ultra_{name.lower().replace(' ', '_')}.png"
    img.save(fname)

    print(f"\n{'─' * 60}")
    print(f"  {name} — {d['desc']}")
    print(f"  {cols}×{rows} | {px} patches | ${cost:,}")

print(f"\n{'=' * 60}")
print("  FULL PRICE LIST")
print("=" * 60)
for name, d in sorted(designs.items(), key=lambda x: count(x[1]["grid"])):
    px = count(d["grid"])
    cost = px * PATCH_VALUE
    print(f"  {name:<15} {px:>4} patches   ${cost:>6,}")
print("=" * 60)
