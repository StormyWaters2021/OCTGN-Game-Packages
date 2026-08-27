# Colors
BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"
YELLOW = "#FFFF00"
ORANGE = "#FFA500"
PURPLE = "#800080"
PINK = "#FFC0CB"
CYAN = "#00FFFF"
GRAY = "#808080"
LIGHT_GRAY = "#D3D3D3"
DARK_GRAY = "#404040"
BROWN = "#A52A2A"
GOLD = "#FFD700"
SILVER = "#C0C0C0"

OVERLAY_ALPHA = "40"

COLOR_OPTIONS = [
    ("Red", RED),
    ("Green", GREEN),
    ("Blue", BLUE),
    ("Yellow", YELLOW),
    ("Orange", ORANGE),
    ("Purple", PURPLE),
    ("Pink", PINK),
    ("Cyan", CYAN),
    ("White", WHITE),
    ("Black", BLACK),
    ("Gray", GRAY),
    ("Light Gray", LIGHT_GRAY),
    ("Dark Gray", DARK_GRAY),
    ("Brown", BROWN),
    ("Gold", GOLD),
    ("Silver", SILVER),
]

OWNER_MARKERS = {
    0: ("P1", "p1_marker"),
    1: ("P2", "p2_marker"),
    2: ("P3", "p3_marker"),
    4: ("P4", "p4_marker"),
}


def p1_marker(card, x=0, y=0):
    mute()
    card.markers[OWNER_MARKERS[0]] += 1

def p2_marker(card, x=0, y=0):
    mute()
    card.markers[OWNER_MARKERS[1]] += 1

def p3_marker(card, x=0, y=0):
    mute()
    card.markers[OWNER_MARKERS[2]] += 1

def p4_marker(card, x=0, y=0):
    mute()
    card.markers[OWNER_MARKERS[3]] += 1


def chooseColor(title):
    names = [name for name, color in COLOR_OPTIONS]
    colors = [color for name, color in COLOR_OPTIONS]

    choice = askChoice(
        title,
        names,
        colors
    )

    if choice == 0:
        return None

    return COLOR_OPTIONS[choice - 1][1]


def setBorder(card, x=0, y=0):
    color = chooseColor("Choose a border color:")

    if color is None:
        return

    card.highlight = color


def clearBorder(card, x=0, y=0):
    card.highlight = None


def setOverlay(card, x=0, y=0):
    color = chooseColor("Choose an overlay color:")

    if color is None:
        return

    card.filter = "#" + OVERLAY_ALPHA + color[1:]


def clearOverlay(card, x=0, y=0):
    card.filter = None
    
    
def _mark_owner(color, card):
    mute()
    