
def fail_check(*args):
    return False
    

def position(card, x=0, y=0):
    position = card.position
    whisper("Position = {}.".format(str(position)))
    whisper("isInverted attr: {}".format(card.isInverted))
    whisper("isInverted call: {}".format(card.isInverted()))
    

def _test(unit, x=0, y=0):
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
    unitx, unity = unit.position

    offsetx = int(round((unitx - aax) / 100))
    offsety = int(round((unity - aay) / 100))

    if offsetx > width - 1 or offsety > height - 1:
        return
    if offsetx < 0 or offsety < 0:
        return

    intersection = columns[offsetx] + rows[offsety]

    whisper(intersection)