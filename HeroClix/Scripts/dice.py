def create_dice():
    mute()
    count = 0
    for card in table:
        if card.size == "Dice":
            count += 1
    
    if count != 0:
        return
    
    for p in DICE_POSITIONS:
        x, y = p
        dice = table.create(DICE_GUID, x, y)
        dice.anchor = True


def _grab_dice(card):
    mute()
    p = card.controller
    remoteCall(p, "_pass_dice", [card, me])


def _pass_dice(card, player):
    mute()
    card.controller = player


def roll_d8(group, x=0, y=0):
    mute()
    roll = rnd(1, 8)
    notify("{} rolled {} on a d8.".format(me, roll))
    

def roll_d20(group, x=0, y=0):
    mute()
    roll = rnd(1, 20)
    notify("{} rolled {} on a d20.".format(me, roll))


def roll_single_die(group, x=0, y=0):
    mute()

    dice = []
    
    for card in table:
        if card.size == "Dice":
            dice.append(card)
            if card.controller != me:
                _grab_dice(card)

    face = rnd(1, 6)
    results = str(face)

    # Update the physical die if one exists
    if dice:
        dice[0].alternate = DICE_FACES[face]

    notify("{} rolled {} on a single die.".format(me, results))


def roll_dice(group, x=0, y=0):
    mute()

    dice = []
    
    for card in table:
        if card.size == "Dice":
            dice.append(card)
            if card.controller != me:
                _grab_dice(card)

    total = 0
    results = ""
    
    if len(dice) == 2:
        for card in dice:
            face = rnd(1, 6)
            card.alternate = DICE_FACES[face]
            total += face
            results += str(face) + ", "

    if len(dice) < 2:
        for i in range(2):
            face = rnd(1, 6)
            total += face
            results += str(face) + ", "

    if group != "quiet":
        notify("{} rolled {}with a total of {}.".format(me, results, total))

    return total