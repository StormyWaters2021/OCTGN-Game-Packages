def create_pac():
    mute()
    count = 0
    for card in table:
        if card.size == "PAC":
            count += 1
    if count >= 1:
        whisper("PAC is already on the table.")
        return
    else:
        x, y = PAC_POSITIONS
        table.create(PAC_GUID, x, y)


def setup_table():
    mute()
    initializeGame()
    if me._id != 1:
        return
    create_dice()
    create_pac()