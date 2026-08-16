MAP_POSITIONS = {
    "16x16": (-800, -800),
    "16x24": (-800, -1200),
    "24x24": (-1200, -1200)
}


MAP_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
MAP_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']


def load_map(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"Map"}, title="Select a Map")
    if guid is None:
        return
        
    card = table.create(guid, 0, 0, quantity = 1, persist = False)
    _position_map(card)
    

def rotate_map(card, x=0, y=0):
    mute()
    if card.orientation == 0:
        card.orientation = 2
    else:
        card.orientation = 0
    card.index = 0


def _get_map_position(gamemap):
    if gamemap.size in MAP_POSITIONS.keys():
        return MAP_POSITIONS[gamemap.size]


def _position_map(gamemap):
    mute()
    x, y = _get_map_position(gamemap)
    gamemap.moveToTable(x, y)
    gamemap.anchor = True
    gamemap.sendToBack()


def _check_map_rotation():
    mute()
    maps = []
    
    for m in table:
        if m.properties["Unit Type"] == "Map":
            maps.append(m)
    if len(maps) > 1:
        notify("Multiple maps detected. Please remove all but one.")
        return -1
    elif len(maps) < 1:
        notify("No map detected. Please load a map.")
        return -1
    else:
        return maps[0].orientation


def _report_movement(x, y):
    mute()

    gamemap = None
    rotation = _check_map_rotation()

    if rotation == -1:
        return

    for card in table:
        if card.properties["Unit Type"] == "Map":
            gamemap = card

    width, height = gamemap.size.split("x")
    width = int(width)
    height = int(height)

    rows = MAP_NUMBERS[:height]
    columns = MAP_LETTERS[:width]

    if rotation == 2:
        columns = columns[::-1]
        rows = rows[::-1]

    if gamemap.position != _get_map_position(gamemap):
        _position_map(gamemap)

    aax, aay = _get_map_position(gamemap)

    offsetx = int(round((x - aax) / 100))
    offsety = int(round((y - aay) / 100))

    if offsetx > width - 1 or offsety > height - 1:
        return
    if offsetx < 0 or offsety < 0:
        return

    intersection = columns[offsetx] + rows[offsety]

    return intersection