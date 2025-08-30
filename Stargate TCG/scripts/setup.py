def game_setup(args = None):
    mute()
    whisper("ID: {}".format(me._id))
    if args != None and args.player != me:  #only execute this event if its your own deck
        return    
    if not registerTeam():
        return
    if not confirm("Would you like to use automated setup?"):
        notify("{} cancelled automated setup. Please setup manually.".format(me))
        return
    pull_team()
    if len(players) < 2:
        return
    set_victory(0, 0)
    if int(getGlobalVariable("players_loaded")) > 1:
        if me._id == 1:
            complete_setup()
        else:
            player = [p for p in players if p._id == 1][0]
            remoteCall(player, "complete_setup", [])
    
    
def pull_team():
    pos = get_my_position()
    n = int(getGlobalVariable("players_loaded"))
    x, y = pos["team"]
    for card in me.Team:
        card.moveToTable(x, y, False)
        x += (73 * pos["invert_mod"])
    setGlobalVariable("players_loaded", str(n+1))


def set_victory(check, victory = 0):
    mute()
    tyler = tyler_check(table)
    if check == 0:
        for card in table:
            if card.controller == me:
                victory += int(card.Cost)
        if tyler: 
            victory = int(victory / 2)
        player = [p for p in players if p != me][0]
        remoteCall(player, "set_victory", [1, victory])
    elif check == 1:
        me.counters['Experience Win'].value = victory
    else:
        return
    
    
def complete_setup():
    mute()
    first = determine_first()
    opp = [p for p in players if p != me][0]
    if first != me:
        setup_stop_char()
        setPhase(1)
    else:
        remoteCall(opp, "setup_stop_char", [])
        remoteCall(opp, "setPhase", [1])
    drawN(8)
    remoteCall(opp, "drawN", [8])
    
    
def determine_first():
    host = 0
    opp = 0
    winner = None
    opponent = [p for p in players if p != me][0]
    for card in table:
        if card.controller == me:
            host += int(card.Cost)
        else:
            opp += int(card.Cost)
    if host > opp:
        winner = me
    elif opp > host:
        winner = opponent
    else:
        n = rnd(0, 1)
        winner = players[n]
    notify("{} will be the first player.".format(winner))
    setActivePlayer(winner)
    return winner
    
    
def setup_stop_char():
    mute()
    stopped_team = False
    team_members = [c for c in table if c.controller != me]
    
    while not stopped_team:
        dlg = cardDlg(team_members)
        dlg.max = 1
        dlg.title = "Choose a Team Character to stop."
        dlg.text = "Select a Card"
        cards = dlg.show()
        
        if cards == None:
            if confirm("Do you want to skip choosing a character to stop?"):
                return False
        
        elif cards != None:
            card = cards[0]
            remoteCall(card.controller, "stop", [card])
            stopped_team = True