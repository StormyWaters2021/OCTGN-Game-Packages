P1_REFERENCE = (262, 53)
P2_REFERENCE = (-322, -138)

P1_MAINFRAME = (-255, 110)
P2_MAINFRAME = (195, -195)


REFERENCES = ["37e28e6f-cc45-43bc-8a0e-782d88e5bd1c", "782ab4c5-1a75-4bb2-b947-1f1026fe019a", "d4644fbb-d5c1-4047-8fa8-40c601c07096"]

def make_references():
    mute()
    if me._id != 1:
        return
    x, y = P1_REFERENCE
    for guid in REFERENCES:
        card = table.create(guid, x, y, persist=False)
        card.anchor = True
        y += 93
    x, y = P2_REFERENCE
    for guid in REFERENCES:
        card = table.create(guid, x, y, persist=False)
        card.anchor = True
        y -= 92
    show_changelog()
    
        
def deck_loaded(args):
    mute()
    if args.player != me:
        return    
    counter = 0
    stored_card = None
    # loaded_decks = int(getGlobalVariable("decks_loaded"))
    
    if me.isInverted:
        x, y = P2_MAINFRAME
    else:
        x, y = P1_MAINFRAME
    
    for card in me.Cyberdeck:
        if card.Type == "MAINFRAME":
            stored_card = card
            counter += 1
    if counter != 1:
        whisper("Error locating MAINFRAME. Please find it manually.")
    else:
        stored_card.moveToTable(x, y, True)

    for pile in [DECK, RAM]:
        shuffle(pile)
        



