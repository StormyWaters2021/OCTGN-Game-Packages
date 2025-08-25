def pull_team():
    pos = get_my_position()
    n = int(getGlobalVariable("players_loaded"))
    x, y = pos["team"]
    for card in me.Team:
        card.moveToTable(x, y, True)
        x += (73 * pos["invert_mod"])
    setGlobalVariable("players_loaded", str(n))    