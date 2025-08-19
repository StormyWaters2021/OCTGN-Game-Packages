    
def assign(card, x = 0, y = 0):
    mute()
    if card.filter != None:
        whisper("Cannot assign {}: it is blocked from the mission.".format(card))
    elif not card.isFaceUp:
        whisper("Cannot assign {}: it is incapacitated.".format(card))
    elif card.orientation != Rot0:
        whisper("Cannot assign {}: it is not ready.".format(card))
    else:
        notify("{} assigns {} to the mission.".format(me, card))

def ready(card, x = 0, y = 0):
    mute()
    if card.filter != None:
        card.filter = None
        notify("{} unblocks {}.".format(me, card))
    else:
        if card.orientation != Rot0:
            card.orientation = Rot0
        notify("{} readies {}.".format(me, card))

def block(card, x = 0, y = 0):
    mute()
    if card.filter == None:
        card.filter = "#bb777777"
        notify("{} blocks {} from the mission.".format(me, card))
    else:
        card.filter = None
        whisper("{} unblocks {} from the mission.".format(me, card))

def stop(card, x = 0, y = 0):
    mute()
    if card.orientation != Rot90:
        card.orientation = Rot90
        notify("{} stops {}.".format(me, card))
    else:
        card.orientation = Rot0
        whisper("{} readies {}.".format(me, card))

def incapacitate(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        card.isFaceUp = False
        card.orientation = Rot90
        card.peek()
        notify("{} incapacitates {}.".format(me, card))
    else:
        card.isFaceUp = True
        whisper("{} removes incapacitation from {}.".format(me, card))

def destroy(card, x = 0, y = 0):
    mute()
    src = card.group
    card.moveTo(me.Discard)
    if src == table:
        notify("{} destroys {}.".format(me, card))
    else:
        notify("{} discards {} from their {}.".format(me, card, src.name))

def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} flips {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} flips {} face up.".format(me, card))

def draw(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    group[0].moveTo(me.hand)
    notify("{} draws a card.".format(me))
    
def discardX(group, x = 0, y = 0):
    if len(group) == 0:
        return
    mute()
    count = min(askInteger("Discard how many cards?", 0), len(group))
    if count == None or count == 0:
        return
    for card in group.top(count):
        card.moveTo(card.owner.Discard)
    notify("{} discards {} cards from {} (top).".format(me, count, group.name))

def shuffle(group, x = 0, y = 0):
    if len(group) > 0:
        group.shuffle()

def activateAbility(card, x = 0, y = 0):
    mute()
    notify("{} activates {}'s ability.".format(me, card))

def passTurn(group, x = 0, y = 0):
    mute()
    notify("{} passes.".format(me))
    
def addPromotion(card, x = 0, y = 0):
    mute()
    card.markers[("Promotion", "Promotion")] += 1
    notify("{} adds a promotion counter to {}.".format(me, card))
    
######################################################
##
## SCRIPTS
##
######################################################


def debugToggle(group, x = 0, y = 0):
    mute()
    global DebugMode
    if isDebug() == False:
        notify("{} enables Debug Mode.".format(me))
        setSetting("debugMode", True)
        DebugMode = True
    else:
        notify("{} disables Debug Mode.".format(me))
        setSetting("debugMode", False)
        DebugMode = False
        
DebugMode = True

def isDebug():
    mute()
    global DebugMode
    if DebugMode == None:
        DebugMode = getSetting("debugMode", False)
    return DebugMode

def turnPassed(args):
    mute()
    if me.isActive:
        if me.isInverted:
            table.board = "invert"
        else:
            table.board = ""
        for c in table:
            if c.controller == me:
                if not c.isFaceUp and c.orientation == Rot90:
                    c.isFaceUp = True
                elif c.orientation == Rot90:
                    c.orientation = Rot0
                elif c.filter != None:
                    c.filter = None


