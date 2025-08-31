SIDEWAYS = ["Castle", "Event", "Land", "Taunt", "Village",]
REVEAL_DESTINATION_LIST = ["Dead Cart", "In My Hand", "Eliminated", ]
REVEAL_COLOR_LIST = ['#000000', '#000000', '#000000', ]


# ~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ MOVE CARDS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~ #

TABLESPACE = (-335, 95)
TABLESPACEINV = (235, -105)


def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles their {}.".format(me, group.name))


def shuffle_into_deck(card, x=0, y=0):
    mute()
    card.moveTo(me.Deck)
    shuffle(me.Deck)
    _extapi.notify("{} shuffles {} into their deck.".format(me, card), ChatColors.Black)


def shuffle_all_into_deck(group, x=0, y=0):
    mute()
    for card in group:
        card.moveTo(me.Deck)
    shuffle(me.Deck)
    _extapi.notify("{} shuffles all the cards in {} into their deck.".format(me, group.name), ChatColors.Black)
  
  
def draw(group, x=0, y=0):
    mute()
    if len(group) < 1:
        return
    card = group.top()
    card.moveTo(me.hand)
    _extapi.notify("{} draws a card.".format(me), ChatColors.Black)
    
    
def drawN(number):
    mute()
    for _ in range(number):
        card = me.Deck.top()
        card.moveTo(me.hand)
    _extapi.notify("{} draws {} cards.".format(me, number), ChatColors.Black)


def discard(card, x = 0, y = 0):
    mute()
    card.moveTo(me.piles["Dead Cart"])
    _extapi.notify("{} discards {}.".format(me, card), ChatColors.Red)


def random_discard(*args):
    mute()
    if len(me.Hand) < 1:
        return
    random = rnd(0, len(me.Hand) - 1)
    card = me.Hand[random]
    _extapi.notify("{} randomly chooses {}.".format(me, card), ChatColors.Red)
    discard(card)
    

def remove_from_game(card, x = 0, y = 0):
    mute()
    card.moveTo(me.Eliminated)
    _extapi.notify("{} eliminates {}.".format(me, card), ChatColors.Red)


def moveFaceDown(card, x=0, y=0):
    mute()
    if not me.isInverted:
        x, y = TABLESPACE
    else:
        x, y = TABLESPACEINV
    card.moveToTable(x, y, True)
    card.peek()
    notify("{} plays a card face down.".format(me))
    

def flipCard(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))
    x,y = card.position
    card.moveToTable(x, y)


def rotate_card(card, rot):
    if card.controller == me:
        card.orientation = rot


def tap_untap(card, x = 0, y = 0):
    mute()
    if card.orientation == 0:
        card.orientation = 1
    else: card.orientation = 0
    

def rotate_right(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        rotate_card(card, (card.orientation + 1) % 4)


def rotate_left(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        rotate_card(card, (card.orientation - 1) % 4)


def fix_rotation(args):
    if args.player != me:
        return
    for card in args.cards:
        if card.controller != me:
            continue
        if not card.isFaceUp:
            continue
        if card.group != table:
            continue
        for i in SIDEWAYS:
            if i in card.properties["Card Type"]:
                card.orientation = 3


def random_dead(group, x=0, y=0):
    mute()
    players = getPlayers()
    if not players: return

    # askChoice returns 1-based index (0 = cancel)
    idx = askChoice("Which player's Dead Cart do you want to take from?",
                    [p.name for p in players])
    if idx < 1: 
        return

    target = players[idx - 1]
    if target == me:
        c = _random_card_from_pile(me.piles['Dead Cart'])
        if c: c.moveTo(me.hand)
    else:
        # Ask the chosen opponent to give a random card from *their* Dead Pile to me
        remoteCall(target, '_giveRandomFromDeadTo', [me])


def _random_card_from_pile(pile):
    mute()
    cards = [c for c in pile]
    if not cards:
        whisper("That pile is empty.")
        return None
    card = cards[rnd(0, len(cards) - 1)]
    return card


def _giveRandomFromDeadTo(requester):
    mute()
    c = _random_card_from_pile(me.piles['Dead Cart'])
    if not c: 
        return
    c.moveToTable(0, 0)
    c.controller = requester
    notify("{} takes a random card from {}'s Dead Cart.".format(requester, me))
    remoteCall(requester, "_grab_passed_card", [c])


def look_at_top(group, player):
    mute()
    top = []
    top.append(me.group.top())
    cards = cardDlg(top)
    dlg.title = "Here is the top card."
    dlg.text = "Select a Card"
    
    if player == me:
        choice = cards.show()
        
    else:
        remoteCall(player, "show_cards", [cards])
        

# ~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ OPPO CARDS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~ #

def opp_draw(group, x=0, y=0):
    mute()
    if len(players) < 1:
        return
    opp = [p for p in players if p != me]    
    remoteCall(opp[0], "_passFaceDown", [opp[0].Deck.top(), me])


def _passFaceDown(card, opponent):
    mute()
    card.moveToTable(0, 0, True)
    card.controller = opponent
    remoteCall(opponent, "_grab_passed_card", [card])
    
    
def _grab_passed_card(card):
    mute()
    card.moveTo(me.Hand)


def reveal_hand(group, x=0, y=0):
    mute()
    opps = [p for p in getPlayers() if p != me]
    if not opps or not me.hand: return

    opp = opps[0] if len(opps) == 1 else opps[askChoice("Choose opponent:", [p.name for p in opps]) - 1]
    if not opp: return

    remoteCall(opp, '_pickCardToDiscard', [[c for c in me.hand], me])


def _pickCardToDiscard(cards, owner):
    mute()
    destination = 0
    choice_list = REVEAL_DESTINATION_LIST
    colors_list = REVEAL_COLOR_LIST
    
    dlg = cardDlg(cards)
    dlg.title = "Opponent's Hand"
    dlg.text = "Choose cards from your opponent's hand:"
    dlg.max = 9999
    chosen = dlg.show()
    if not chosen:
        notify("No card chosen, reveal cancelled.")
        return
    else:
        destination = askChoice("Where do you want the card(s) to go?", choice_list, colors_list)
    if destination == 0:
        notify("No destination chosen, reveal cancelled.")
        return
    elif destination == 1:
        for card in chosen:
            remoteCall(owner, 'discard', [card])
    elif destination == 2:   
        for card in chosen:
            remoteCall(owner, "_passFaceDown", [card, me])
            _extapi.notify("{} puts {} in their hand.".format(me, card), ChatColors.Black)
    elif destination == 3:
        for card in chosen:
            remoteCall(owner, "remove_from_game", [card])
    else:
        notify("An error occurred. Please try again.")

# ~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ CREATE CARDS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~~~ #

def create_in_pile(group, x = 0, y = 0):
    mute()
    guid, quantity = askCard()
    if guid is not None:
        group.create(guid, quantity)
        notify("{} created a card in their {}.".format(me, group.name))
        
    
def createUp(group, x, y):
    mute()
    guid, quantity = askCard()
    if guid is not None:
        card = table.create(guid,x,y,quantity, persist = True)
        notify("{} created {}.".format(me, card))


def createDown(group, x, y):
    mute()
    guid, quantity = askCard()
    if guid is not None:
        table.create(guid,x,y,quantity, persist = True).isFaceUp = False
        notify("{} created a face-down card.".format(me))


# ~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ MARKERS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~ #

def custom_marker(card, x=0, y=0):
    marker, qty = askMarker()
    if qty == 0: return
    card.markers[marker] += qty


def addMarker(card, marker):
   mute()
   card.markers[marker] += 1


def remMarker(card, marker):
   mute()
   if card.markers[marker] < 1:
        return False
   card.markers[marker] -= 1
   return True
   
    
def plusCombat(card, x = 0, y = 0):
   mute()
   marker = ("+ Combat", "pluscombat")
   addMarker(card, marker)
   notify("{} adds a + Combat marker to {}.".format(me, card))
   
   
def remPlusCombat(card, x = 0, y = 0):
   mute()
   marker = ("+ Combat", "pluscombat")
   check = remMarker(card, marker)
   if check: notify("{} removes a + Combat marker from {}.".format(me, card))
   else: notify("{} has no + Combat markers to remove.".format(card))


def minusCombat(card, x = 0, y = 0):
   mute()
   marker = ("- Combat", "minuscombat")
   addMarker(card, marker)
   notify("{} adds a - Combat marker to {}.".format(me, card))
   
   
def remMinusCombat(card, x = 0, y = 0):
   mute()
   marker = ("- Combat", "minuscombat")
   check = remMarker(card, marker)
   if check: notify("{} removes a - Combat marker from {}.".format(me, card))
   else: notify("{} has no - Combat markers to remove.".format(card))   
   

def plusWits(card, x = 0, y = 0):
   mute()
   marker = ("+ Wits", "pluswits")
   addMarker(card, marker)
   notify("{} adds a + Wits marker to {}.".format(me, card))
   
   
def remPlusWits(card, x = 0, y = 0):
   mute()
   marker = ("+ Wits", "pluswits")
   check = remMarker(card, marker)
   if check: notify("{} removes a + Wits marker from {}.".format(me, card))
   else: notify("{} has no + Wits markers to remove.".format(card))


def minusWits(card, x = 0, y = 0):
   mute()
   marker = ("- Wits", "minuswits")
   addMarker(card, marker)
   notify("{} adds a - Wits marker to {}.".format(me, card))
   
   
def remMinusWits(card, x = 0, y = 0):
   mute()
   marker = ("- Wits", "minuswits")
   check = remMarker(card, marker)
   if check: notify("{} removes a - Wits marker from {}.".format(me, card))
   else: notify("{} has no - Wits markers to remove.".format(card))   
   
# ~~~~~~~~~~~~~~~~~~ #
# ~~~~~ RANDOM ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~ #
    
def rollDie(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls a d6: {}.".format(me, n))


def rollX(group, x=0, y=0):
    mute()
    x = askInteger("Random number from 1 to...", 0)
    n = rnd(1, x)
    notify("{} rolled a die with {} sides: {}".format(me,x,n))


def coinFlip(group, x=0, y=0):
    mute()
    n = rnd(1,2)
    if n == "1": notify("{} flipped a coin and the result was heads.".format(me))
    else: notify("{} flipped a coin and the result was tails.".format(me))

    
# ~~~~~~~~~~~~~~~~~~~~~~ #    
# ~~~~~ HIGHLIGHTS ~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~ #   
    
def red(card, x = 0, y = 0):
    mute()
    card.highlight = "#ff0000"

def orange(card, x = 0, y = 0):
    mute()
    card.highlight = "#ff9900"

def yellow(card, x = 0, y = 0):
    mute()
    card.highlight = "#ffff00"

def green(card, x = 0, y = 0):
    mute()
    card.highlight = "#00ff00"

def blue(card, x = 0, y = 0):
    mute()
    card.highlight = "#0000ff"

def purple(card, x = 0, y = 0):
    mute()
    card.highlight = "#9900ff"

def white(card, x = 0, y = 0):
    mute()
    card.highlight = "#ffffff"

def clear(card, x = 0, y = 0):
    mute()
    card.highlight = None
    

# ~~~~~~~~~~~~~~~~~ #
# ~~~~~ PAWNS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~ #

PAWNS = {
"red": "27c8f09c-5fbe-4ae4-9c5c-9784c8ad99af",
"orange": "ac71af19-acf8-48d9-8716-4ed1a8635eab",
"yellow": "caa4df3c-caad-4de1-8a01-c5a746a34ccb",
"green": "42096792-a189-4f0d-beb8-0ff69748c04a",
"blue": "038274fc-b9b7-418b-9bff-9ec495471a78",
"purple": "b81cb8bd-e0e0-47e5-9845-570cf25c101c",
"pink": "e0c662d3-d076-47f9-8a5c-dd05238b8991",
"rainbow": "fa30c6a3-0045-4d50-bedd-2788e446eea6",
"black": "a6c3682e-e9ed-40cf-b658-0e26a4d25c9c",
"grey": "b312e61c-8df4-49f3-a6cb-5880ec93abcb",
}

NEWT = "4261224c-6e22-4619-bed5-d02de9c437ec"
SEARCHED = "efad4eaa-ea5f-46c3-9908-bf67e7df50a8"

def create_pawn(color, x = 0, y = 0):
    mute()
    card = table.create(PAWNS[color], x, y, persist = False)
    card.properties["Card Type"] = "{}'s Pawn".format(me.name)
    card.highlight = "#ffffff"
    notify("{} creates a {} pawn.".format(me, color))


def create_newt(group, x=0, y=0):
    mute()
    card = table.create(NEWT, x, y, persist = False)
    notify("{} creates A NEWT?!".format(me))
    
    
def create_searched(group, x=0, y=0):
    mute()
    card = table.create(SEARCHED, x, y, persist = False)
    
    
def redpawn(group, x=0, y=0):
    create_pawn("red", x, y)

def orangepawn(group, x=0, y=0):
    create_pawn("orange", x, y)

def yellowpawn(group, x=0, y=0):
    create_pawn("yellow", x, y)

def greenpawn(group, x=0, y=0):
    create_pawn("green", x, y)

def bluepawn(group, x=0, y=0):
    create_pawn("blue", x, y)
    
def purplepawn(group, x=0, y=0):
    create_pawn("purple", x, y)

def pinkpawn(group, x=0, y=0):
    create_pawn("pink", x, y)
  
def rainbowpawn(group, x=0, y=0):
    create_pawn("rainbow", x, y)
    
def blackpawn(group, x=0, y=0):
    create_pawn("black", x, y)
    
def greypawn(group, x=0, y=0):
    create_pawn("grey", x, y)