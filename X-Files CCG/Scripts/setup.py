P1_POSITIONS = {
    "xfile": {"x": 570, "y": 370},
    "agent": {"x": -475, "y": 365},
    "agent_mod": 145,
}

P2_POSITIONS = {
    "xfile": {"x": -705, "y": -565},
    "agent": {"x": 335, "y": -555},
    "agent_mod": -145,
    
}

def game_started():
    if me._id != 1:
        return
    if len(players) > 4:
        _extapi.notify("No more than 4 players are supported.".format(), ChatColors.Red)
        return
    if len(players) > 2:
        table.board = 'multi'


def deck_loaded(args):
    if args.player != me:
        return
    shuffle(me.Deck, 0, 0)
    if not starting_agents():
        _extapi.whisper("Automated setup cancelled. You will need to manually set up or reset the game.".format(), ChatColors.Orange)
        return
    else:
        _extapi.notify("{} has selected their starting Agents.".format(me), ChatColors.Blue)
    
    if not starting_xfile():
        _extapi.whisper("No X-File selected. Please right-click the table to select one.".format(), ChatColors.Orange)
        return
    else:
        _extapi.notify("{} has selected their X-File.".format(me), ChatColors.Green)
    drawN(7)
    deck_loaded = int(getGlobalVariable("players_loaded"))
    deck_loaded += 1
    setGlobalVariable("players_loaded", str(deck_loaded))


def loaded_check(args):
    if int(getGlobalVariable("players_loaded")) != len(players):
        return
    if args.name != "players_loaded":
        return
    for card in table: 
        if card.controller == me:
            if card.XFile != "True":
                card.isFaceUp = True
    complete_setup()
        

def complete_setup():
    if me._id != 1:
        return
    random = rnd(0, len(players) - 1)
    setActivePlayer(players[random])
    setPhase(1)


def starting_agents(*args):
    mute()
    rp = 0
    pos = []
    agents = [c for c in me.Deck if c.Type == "Agent"]
    
    starting_agents = False
    cards = []
    
    while not starting_agents:
    
        dlg = cardDlg(agents)
        dlg.max = 999
        dlg.title = "Choose your starting Agents."
        dlg.text = "Select a Card"
        cards = dlg.show()
        
        if cards == None:
            if confirm("Do you want to skip choosing your starting agents?"):
                return False
        
        elif cards != None:
            for card in cards:
                rp += int(card.Cost.split()[0])
            if rp > 20:
                whisper("Starting Agents must have a total RP cost of 20 or less.")
            else:
                starting_agents = True      
  
    if me.isInverted:
        pos = P2_POSITIONS
    else:
        pos = P1_POSITIONS
    
    x = pos["agent"]["x"]
    y = pos["agent"]["y"]
    
    for card in cards:
        card.moveToTable(x, y, True)
        x += pos["agent_mod"]

    shuffle(me.Deck, 0, 0)        
    return True
                

def starting_xfile(*args):
    mute()
    if me.isInverted:
        x = P2_POSITIONS["xfile"]["x"]
        y = P2_POSITIONS["xfile"]["y"]
    else:
        x = P1_POSITIONS["xfile"]["x"]
        y = P1_POSITIONS["xfile"]["y"]
    xfile_picked = False
    while not xfile_picked:
        card, _ = askCard({"XFile":"True"}, title = "Choose your X-File:")
        if card != None:
            xfile_picked = True
            me.setGlobalVariable("starting_xfile", "1")
        elif card == None:
            if confirm("Do you want to skip choosing your X-File card?"):
                return False
    xfile = table.create(card, x, y, quantity = 1, persist = True)
    xfile.isFaceUp = False
    xfile.peek()
    addXfile(xfile, x = 0, y = 0)
    return True
    
    
def no_starting_xfile(*args):
    if me.getGlobalVariable("starting_xfile") == "0":
        return True
    else:
        return False
    
# def position(card, x=0, y=0):
    # position = card.position
    # whisper("Position = {}.".format(str(position)))