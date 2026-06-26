# ~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ VARIABLES  ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~ #

DECK = me.Cyberdeck
RAM = me.piles["RAM Deck"]
DISCARD = me.piles["Recycle Bin"]
RFG = me.Purge

TABLESPACE = (-30, 226)
TABLESPACEINV = (-30, -310) 

# ~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~ MOVE CARDS ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~~~~~ #

def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles their {}.".format(me, group.name))


def shuffle_into_deck(card, x=0, y=0):
    mute()
    card.moveTo(DECK)
    shuffle(DECK)
    notify("{} shuffles {} into their deck.".format(me, card))
  
  
def draw(group, x=0, y=0):
    mute()
    if len(group) < 1:
        return
    card = group.top()
    card.moveTo(me.hand)
    notify("{} draws a card.".format(me))
    
    
def drawN(number):
    mute()
    for _ in range(number):
        card = DECK.top()
        card.moveTo(me.hand)
    notify("{} draws {} cards.".format(me, number))


def discard(card, x = 0, y = 0):
    mute()
    card.moveTo(DISCARD)
    notify("{} discards {}.".format(me, card))


def random_discard(*args):
    mute()
    if len(me.Hand) < 1:
        return
    random = rnd(0, len(me.Hand) - 1)
    card = me.Hand[random]
    notify("{} randomly chooses {}.".format(me, card))
    discard(card)
    

def remove_from_game(card, x = 0, y = 0):
    mute()
    card.moveTo(RFG)
    notify("{} eliminates {}.".format(me, card))


def moveFaceUp(card, x=0, y=0):
    mute()
    if not me.isInverted:
        x, y = TABLESPACE
    else:
        x, y = TABLESPACEINV
    card.moveToTable(x, y, False)
    card.target()
    notify("{} plays {}.".format(me, card))


def moveFaceUpRAM(group, x=0, y=0):
    mute()
    if not me.isInverted:
        x, y = TABLESPACE
    else:
        x, y = TABLESPACEINV
    card = RAM.top()
    card.moveToTable(x, y, False)
    card.target()
    notify("{} installs {}.".format(me, card))


def moveFaceDown(card, x=0, y=0):
    mute()
    if not me.isInverted:
        x, y = TABLESPACE
    else:
        x, y = TABLESPACEINV
    card.moveToTable(x, y, True)
    card.peek()
    card.target()
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
    else: 
        card.orientation = 0


def copyCard(card, x = 0, y = 0):
    mute()
    if me.isInverted:
        mod = 10
    else:
        mod = -10
    
    guid = card.model
    token_copy = table.create(guid, x+mod, y+mod, quantity = 1, persist = False)
    notify("{} creates a copy of {}.".format(me, card))
    
    
def createToken(guid):
    mute()
    if not me.isInverted:
        x, y = TABLESPACE
    else:
        x, y = TABLESPACEINV
    
    table.create(guid, x, y, quantity = 1, persist = False)
    notify("{} creates a token.".format(me))


def create_drone(*args):
    createToken("e4cb71a6-e66c-4995-a275-f0a73983471d")

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


def add_invertmf(card, x=0, y=0):
    mute()
    marker = ("INVERT MF", "invert_mf")
    addMarker(card, marker)


def add_invertbf(card, x=0, y=0):
    mute()
    marker = ("INVERT BF", "invert_bf")
    addMarker(card, marker)

   
def add_p1p1(card, x=0, y=0):
    mute()
    marker = ("+1/+1", "plus1plus1")
    addMarker(card, marker)
   
   
def add_n1n1(card, x=0, y=0):
    mute()
    marker = ("-1/-1", "neg1neg1")
    addMarker(card, marker)
    

def add_p1p0(card, x=0, y=0):
    mute()
    marker = ("+1/+0", "plus1plus0")
    addMarker(card, marker)
   
   
def add_p0p1(card, x=0, y=0):
    mute()
    marker = ("+0/+1", "plus0plus1")
    addMarker(card, marker)
    

def add_generic(card, x=0, y=0):
    mute()
    name = askString("Name your counter:", "BLEED")
    if name == None:
        whisper("No name provided, aborting.")
        return
    marker = (name, "generic_marker")
    addMarker(card, marker)

  
# ~~~~~~~~~~~~~~~~~~ #
# ~~~~~ RANDOM ~~~~~ #   
# ~~~~~~~~~~~~~~~~~~ #
    
def rolld20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls a d20: {}.".format(me, n))

    
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