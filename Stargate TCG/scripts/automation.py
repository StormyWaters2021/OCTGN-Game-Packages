def overrideCardsMoved(args):
    mute()
    for i in range(0, len(args.cards)):
        card = args.cards[i]
        if args.toGroups[i] == table:
            fromGroup = card.group
            card.moveToTable(args.xs[i], args.ys[i], not args.faceups[i])
            if fromGroup != table:
                card.index = args.indexs[i]
                if args.faceups[i]:
                    notify("{} plays {}.".format(me, card))
                else:
                    card.peek()
                    notify("{} plays {} as a complication.".format(me, card))
        else:
            group = card.group
            index = args.indexs[i]
            toGroup = args.toGroups[i]
            card.moveTo(toGroup, index)
            if toGroup.name in ["Hand", "Team", "Villain Score Pile", "Discard"]:
                notify("{} moves {} to {} from {}.".format(me, card, toGroup.name, group.name))
            elif index == 0 and toGroup:
                notify("{} moves {} to {} (top) from {}.".format(me, card, toGroup.name, group.name))
            elif index + 1 >= len(toGroup):
                notify("{} moves {} to {} (bottom) from {}.".format(me, card, toGroup.name, group.name))
            else:
                notify("{} moves {} to {} ({} from top) from {}.".format(me, card, toGroup.name, index, group.name))


def registerTeam(args = None):
    mute()
    #### Verify deck contents
    validDeck = True
    maxteam = 4
    whisper("~~~VALIDATING DECKS~~~")
    if tyler_check(me.Team):
        maxteam = 5
    if len(me.Team) != maxteam:
        whisper("Team Error: You need exactly 4 Team Characters. ({} of 4)".format(len(me.Team)))
        validDeck = False
    deckCount = {}
    experience = 0
    for c in me.Team:
        deckCount[c.Name] = deckCount.get(c.Name, 0) + 1
        experience += int(c.Cost)  #add the card's cost to the victory total
    for x in deckCount:
        if deckCount[x] > 1:
            whisper("Team Error: You can only have one {} in your Team. ({} of 1)".format(x, deckCount[x]))
            validDeck = False
    heroCount = sum(1 for c in me.Deck if c.Type in heroTypes)
    if heroCount < 20:
        whisper("Deck Error: You need at least 20 Hero cards in your deck. ({} of 20)".format(heroCount))
        validDeck = False
    villainCount = sum(1 for c in me.Deck if c.Type in villainTypes)
    if villainCount < 20:
        whisper("Deck Error: You need at least 20 Villain cards in your deck. ({} of 20)".format(villainCount))
        validDeck = False
    for c in me.Deck:
        deckCount[c.Name] = deckCount.get(c.Name, 0) + 1
    for x in deckCount:
        if deckCount[x] > 3:
            whisper("Deck Error: You can have at most 3 {} in your Deck. ({} of 3)".format(x, deckCount[x]))
            validDeck = False
    if len(me.piles["Mission Pile"]) != 12:
        whisper("Mission Pile Error: You need exactly 12 Missions. ({} of 12)".format(len(me.piles["Mission Pile"])))
        validDeck = False
    deckCount = {}
    for c in me.piles["Mission Pile"]:
        deckCount[c.Name] = deckCount.get(c.Name, 0) + 1
    for x in deckCount:
        if deckCount[x] > 1:
            whisper("Mission Error: You can only have one {} in your Mission Pile. ({} of 1)".format(x, deckCount[x]))
            validDeck = False
    deckCount = {}
    for c in me.piles["Mission Pile"]:
        for stat in ["Culture", "Science", "Ingenuity", "Combat"]:
            if c.properties[stat] != "":
                deckCount[stat] = deckCount.get(stat, 0) + 1
    for x in deckCount:
        if deckCount[x] != 3:
            whisper("Mission Error: You need exactly 3 {} missions in your Mission Pile. ({} of 3)".format(x, deckCount[x]))
            validDeck = False
    if validDeck:
        notify("{} loaded a legal deck ({} experience).".format(me, experience))
        #### Store the loaded card IDs
        me.Deck.shuffle()
        me.piles["Mission Pile"].shuffle()
    return validDeck


def tyler_check(group):
    tyler = False
    for card in group:
        if card.controller == me:
            if card.model == TYLER:
                tyler = True
    return tyler


def toggle_sort(*args):
    if me.getGlobalVariable("sort_hand") == "True":
        me.setGlobalVariable("sort_hand", "False")
        whisper("Hand sorting disabled.")
    else:
        me.setGlobalVariable("sort_hand", "True")
        whisper("Hand sorting enabled.")


def show_if_host(*args):
    if me._id == 1:
        return True
    else:
        return False


def toggle_phase(*args):
    if getGlobalVariable("phase_actions") == "True":
        setGlobalVariable("phase_actions", "False")
        whisper("Phase actions disabled.")
    else:
        setGlobalVariable("phase_actions", "True")
        whisper("Phase actions enabled.")


def toggle_notes(*args):
    if getGlobalVariable("phase_notes") == "True":
        setGlobalVariable("phase_notes", "False")
        whisper("Phase notes disabled.")
    else:
        setGlobalVariable("phase_notes", "True")
        whisper("Phase notes enabled.")
        
        
def _sort_hand(args = None):
    if me.getGlobalVariable("sort_hand") != "True":
        return
    hand = list(me.Hand) # Freeze current order so we can do a stable regroup
    heroes   = [c for c in hand if c.Allegiance == "Hero"]
    villains = [c for c in hand if c.Allegiance == "Villain"]
    others   = [c for c in hand if c.Allegiance not in ("Hero", "Villain")]
    desired = others + villains + heroes

    for i, card in enumerate(desired):
        card.moveTo(me.Hand, i)


            