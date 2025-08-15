# ~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ MOVE CARDS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~ #


def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles their {}.".format(me, group.name))


def shuffle_into_deck(card, x=0, y=0):
    mute()
    card.moveTo(me.Deck)
    shuffle(me.Deck)
    _extapi.notify("{} shuffles {} into their deck.".format(me, card), ChatColors.Black)
    

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
    card.moveTo(me.Discard)
    _extapi.notify("{} discards {}.".format(me, card), ChatColors.Red)


def remove_from_game(card, x = 0, y = 0):
    mute()
    card.moveTo(me.Eliminated)
    _extapi.notify("{} eliminates {}.".format(me, card), ChatColors.Red)


def moveFaceDown(card, x=0, y=0):
    mute()
    card.moveToTable(0, 0, True)
    card.peek()
    notify("{} plays a card face down.".format(me))
    

def flipCard(card, x = 0, y = 0):
    mute()
    if card.type == "X-File":
        if not confirm("You are about to turn an X-File face-up. Are you sure?"):
            return
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))


def rotate_right(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        card.orientation = (card.orientation + 1) % 4
        notify("{} rotates {}.".format(me, card.Name))


def rotate_left(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        card.orientation = (card.orientation - 1) % 4
        notify("{} rotates {}.".format(me, card.Name))


def random_dead(group, x=0, y=0):
    players = getPlayers()
    if not players: return

    # askChoice returns 1-based index (0 = cancel)
    idx = askChoice("Which player's Dead Cards do you want to take from?",
                    [p.name for p in players])
    if idx < 1: 
        return

    target = players[idx - 1]
    if target == me:
        c = _random_card_from_pile(me.piles['Dead Cards'])
        if c: c.moveTo(me.hand)
    else:
        # Ask the chosen opponent to give a random card from *their* Dead Pile to me
        remoteCall(target, 'giveRandomFromDeadTo', [me._id])


def _random_card_from_pile(pile):
    cards = [c for c in pile]
    if not cards:
        whisper("That pile is empty.")
        return None
    card = cards[rnd(0, len(cards) - 1)]
    return card


def giveRandomFromDeadTo(requesterPid):
    requester = Player(requesterPid)
    c = _random_card_from_pile(me.piles['Dead Cards'])
    if not c: 
        return
    c.moveToTable(0, 0)
    c.controller = requester
    notify("{} takes a random card from {}'s Dead Cards.".format(requester, me))
    remoteCall(requester, "grab_passed_card", [c])


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
        

def show_cards(cards):
    
        
    
 
# ~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ OPPO CARDS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~ #

def opp_draw(group, x=0, y=0):
    mute()
    if len(players) < 1:
        return
    opp = [p for p in players if p != me]    
    remoteCall(opp[0], "passFaceDown", [opp[0].Deck.top(), me])


def passFaceDown(card, opponent):
    mute()
    card.moveToTable(0, 0, True)
    card.controller = opponent
    remoteCall(opponent, "grab_passed_card", [card])
    
    
def grab_passed_card(card):
    card.moveTo(me.Hand)


def reveal_hand(group, x=0, y=0):
    opps = [p for p in getPlayers() if p != me]
    if not opps or not me.hand: return

    opp = opps[0] if len(opps) == 1 else opps[askChoice("Choose opponent:", [p.name for p in opps]) - 1]
    if not opp: return

    remoteCall(opp, 'pickCardToDiscard', [[c for c in me.hand], me])


def pickCardToDiscard(cards, owner):
    dlg = cardDlg(cards)
    dlg.title = "Opponent's Hand"
    dlg.text = "Choose a card for your opponent to discard:"
    chosen = dlg.show()
    if chosen:
        remoteCall(owner, 'discard', [chosen[0]])


# ~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ CREATE CARDS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~~~ #

def create_in_pile(group, x, y):
    mute()
    guid, quantity = askCard()
    if guid is not None:
        group.create(guid, quantity)
        notify("{} created a card in their {}.".format(me, group))
        
    
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
    
def addMarker(card, marker):
   mute()
   card.markers[marker] += 1


def remMarker(card, marker):
   mute()
   if card.markers[marker] < 1:
        return False
   card.markers[marker] -= 1
   return True
   
    
def addDamage(card, x = 0, y = 0):
   mute()
   marker = ("Damage", "dam_marker")
   addMarker(card, marker)
   notify("{} adds a damage marker to {}.".format(me, card))
   
   
def remDamage(card, x = 0, y = 0):
   mute()
   marker = ("Damage", "dam_marker")
   check = remMarker(card, marker)
   if check: notify("{} removes a damage marker from {}.".format(me, card))
   else: notify("{} has no damage markers to remove.".format(card))
   
   
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