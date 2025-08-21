P1_POSITIONS = {
    "Arthur": (-640, 355),
    "Patsy": (-580, 355),
    "max_x": 0,
    "min_x": 0,
    "max_y": 0,
    "min_y": 0,
    "starting_stacks": [
    (-245, 350),
    (-80, 350),
    (80, 350),
    (-315, 250),
    (-155, 250),
    (5, 250),
    (165, 250),
    (-245, 160),
    (-80, 160),
    (80, 160),
    (-180, 65),
    (-20, 65),
    (-10, -25),
    (150, -25),
    ]
}

P2_POSITIONS = {
    "Arthur": (585, -435),
    "Patsy": (530, -435),
    "max_x": 0,
    "min_x": 0,
    "max_y": 0,
    "min_y": 0,
    "starting_stacks": [
    (130, -410),
    (-30, -410),
    (-195, -410),
    (200, -320),
    (40, -320),
    (-120, -320),
    (-280, -320),
    (130, -215),
    (-30, -215),
    (-195, -215),
    (70, -125),
    (-95, -125),
    (-100, -40),
    (-260, -40),
    ]
}

# def game_started():
    # if me._id != 1:
        # return
    # if len(players) > 4:
        # _extapi.notify("No more than 4 players are supported.".format(), ChatColors.Red)
        # return
    # if len(players) > 2:
        # table.board = 'multi'


def deck_loaded(args):
    if args.player != me:
        return
    shuffle(me.Deck, 0, 0)
    if not arthur_patsy():
        _extapi.whisper("Automated setup cancelled. You will need to manually set up or reset the game.".format(), ChatColors.Orange)
        return
    else:
        _extapi.notify("{} has selected their starting Arthur and Patsy.".format(me), ChatColors.Blue)
    
    if not starting_stacks():
        _extapi.whisper("Automated setup cancelled. You will need to manually set up or reset the game.".format(), ChatColors.Orange)
        return
    else:
        _extapi.notify("{} has placed their starting cards.".format(me), ChatColors.Blue)
    drawN(7)
    deck_loaded = int(getGlobalVariable("players_loaded"))
    deck_loaded += 1
    setGlobalVariable("players_loaded", str(deck_loaded))


def loaded_check(args):
    if int(getGlobalVariable("players_loaded")) != len(players):
        return
    if args.name != "players_loaded":
        return
    pos = my_position()
    for card in table: 
        if card.controller == me:
            if card.position == pos["Arthur"]:
                card.isFaceUp = True
            elif card.position == pos["Patsy"]:
                card.isFaceUp = True
            else:
                pass
            if me.isInverted:
                card.highlight = "#ffff00"
            else:
                card.highlight = "#0000ff"
    # complete_setup()
        

# def complete_setup():
    # if me._id != 1:
        # return
    # random = rnd(0, len(players) - 1)
    # setActivePlayer(players[random])
    # setPhase(1)


def arthur_patsy(*args):
    mute()
    arthurs = [c for c in me.Deck if "arthur" in c.setuptags]
    patsys = [c for c in me.Deck if "patsy" in c.setuptags]

    if not starting_card(arthurs, "Arthur"):
        return False
    if not starting_card(patsys, "Patsy"):
        return False
    return True
                

def starting_card(list, kind):
    dlg = cardDlg(list)
    dlg.max = 1
    dlg.min = 1
    dlg.title = "Choose your {}.".format(kind)
    dlg.text = "Select a Card"
    cards = dlg.show()
    
    if cards == None:
        if confirm("Do you want to skip choosing your {}?".format(kind)):
            return False
    
    pos = my_position()  
    x, y = pos[kind]
    
    for card in cards:
        card.moveToTable(x, y, True)
    return True


def starting_stacks():
    if len(me.Deck) < 14:
        return False
    pos = my_position()
    for n in range(14):
        x, y = pos["starting_stacks"][n]
        card = me.Deck.top()
        card.moveToTable(x, y, True)
    return True
        


def my_position():
    if me.isInverted:
        return P2_POSITIONS
    else:
       return P1_POSITIONS

