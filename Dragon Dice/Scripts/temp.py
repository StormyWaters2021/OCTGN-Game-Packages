def check_coord(die, x=0, y=0):
    notify(str(die.position))
    

def dice_in_corners(*args):
    # Creates a die in each corner of each zone to see where they are located

    offset = 0
    
    guid = "03fd8d5d-c983-4806-b344-4b33b5b82f48"
    # Full set of locations defined in your coordinate dicts
    all_locations = [
        "Home Terrain",
        "Frontier Terrain",
        "Home Army",
        "Campaign Army",
        "Horde Army",
        "Summoning Pool",
        "Reserves",
        "DUA",
        "BUA",
    ]

    locations = all_locations

    # Helper to place at corners for a given coord dict (P1 or P2)
    def _place_for_coord_dict(coord_dict, label):
        for loc in locations:
            if loc not in coord_dict:
                continue

            x1, y1, x2, y2 = coord_dict[loc]

            left   = min(x1, x2)
            right  = max(x1, x2)
            top    = min(y1, y2)
            bottom = max(y1, y2)

            l = left + offset
            r = right - offset
            t = top + offset
            b = bottom - offset

            table.create(guid, l, t)  # top-left
            table.create(guid, r, t)  # top-right
            table.create(guid, l, b)  # bottom-left
            table.create(guid, r, b)  # bottom-right

    # Place for both sides explicitly, no invert_check involved
    _place_for_coord_dict(P1_COORDS, "P1")
    _place_for_coord_dict(P2_COORDS, "P2")
