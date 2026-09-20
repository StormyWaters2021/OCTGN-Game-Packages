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


def create_reticle():
    x, y = RETICLE_POSITION
    table.create(RETICLE_GUID, x, y)


def setup_table():
    mute()
    initializeGame()
    if me._id != 1:
        return
    create_dice()
    # create_pac()
    pac_panels()
    create_reticle()
    

def _reset_counter(counter_name):
    me.counters[counter_name].value = 0


def pass_turn(args):
    next_player = args.player
    for card in table:
        if card.properties["Unit Type"] == "Map":
            if card.controller == me:
                card.controller = next_player
    remoteCall(next_player, "_reset_counter", ["Actions Used"])
    next_player.setActive()