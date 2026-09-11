MAP_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', ]
MAP_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', ]


def load_map(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"Map"}, title="Select a Map")
    if guid is None:
        return
        
    card = table.create(guid, 0, 0, quantity = 1, persist = False)
    _position_map(card)
    

def rotate_map(card, x=0, y=0):
    mute()

    rotation = _get_map_rotation()

    if rotation == 0:
        rotation = 2
    else:
        rotation = 0

    _set_map_rotation(rotation)
    _sync_map_rotation(card)
    card.index = 0


def _get_map_position(gamemap):
    width, height = [int(x) for x in gamemap.size.split("x")]
    return -(width * 50), -(height * 50)


def _position_map(gamemap):
    mute()
    x, y = _get_map_position(gamemap)
    gamemap.moveToTable(x, y)
    gamemap.anchor = True
    gamemap.sendToBack()


def _check_map_rotation():
    mute()

    maps = []

    for card in table:
        if card.properties["Unit Type"] == "Map":
            maps.append(card)

    if len(maps) > 1:
        notify("Multiple maps detected. Please remove all but one.")
        return -1

    if len(maps) < 1:
        notify("No map detected. Please load a map.")
        return -1

    return _get_map_rotation()


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

    aax, aay = gamemap.position

    offsetx = int(round((x - aax) / 100))
    offsety = int(round((y - aay) / 100))

    if offsetx > width - 1 or offsety > height - 1:
        return
    if offsetx < 0 or offsety < 0:
        return

    intersection = columns[offsetx] + rows[offsety]

    return intersection
    

def _get_map_rotation():
    return int(getGlobalVariable("map_rotation") or 0)


def _set_map_rotation(rotation):
    setGlobalVariable("map_rotation", str(rotation))
    
    
def _sync_map_rotation(card):
    selected_rotation = _get_map_rotation()

    if card.isInverted():
        if selected_rotation == 0:
            card.orientation = 2
        else:
            card.orientation = 0
    else:
        card.orientation = selected_rotation