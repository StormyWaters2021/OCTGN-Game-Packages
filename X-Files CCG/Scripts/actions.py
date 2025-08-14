def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles their {}.".format(me, group.name))


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
    card.moveTo(me.piles["Removed from Game"])
    _extapi.notify("{} removes {} from the game.".format(me, card), ChatColors.Red)
    

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
        
        
def moveFaceDown(card, x=0, y=0):
    mute()
    card.moveToTable(0, 0, True)
    card.peek()
    notify("{} plays a card face down.".format(me))
    
    
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
   
   
def addXfile(card, x = 0, y = 0):
   mute()
   marker = ("X-File", "xfile_marker")
   addMarker(card, marker)   


def addGameEffect(card, x=0, y=0):
   mute()
   marker = ("Game Effect", "00000000-0000-0000-0000-000000000005")
   addMarker(card, marker)
   notify("{} adds a Game Effect marker to {}.".format(me, card))
   
   
def remGameEffect(card, x=0, y=0):
   mute()
   marker = ("Game Effect", "00000000-0000-0000-0000-000000000005")
   check = remMarker(card, marker)
   if check: notify("{} removes a Game Effect marker from {}.".format(me, card))
   else: notify("{} has no Game Effect markers to remove.".format(card))


def addRP(card, x=0, y=0):
   mute()
   marker = ("RP", "rp_marker")
   addMarker(card, marker)
   notify("{} adds an RP marker to {}.".format(me, card))
   
   
def remRP(card, x=0, y=0):
   mute()
   marker = ("RP", "rp_marker")
   check = remMarker(card, marker)
   if check: notify("{} removes an RP marker from {}.".format(me, card))
   else: notify("{} has no RP markers to remove.".format(card))

   
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