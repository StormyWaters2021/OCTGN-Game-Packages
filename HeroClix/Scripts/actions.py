ACTION_MARKER = ("Action", "action_marker")

PAC_GUID = "7db159f2-1eb2-425f-aaac-5492e36d755b"
PAC_POSITIONS = (-1500, -210)

DICE_POSITIONS = [(-950, -50), (-950, 50)]
DICE_GUID = "fdbd1ec7-702f-4c29-bd6f-3f628af80a39"

NO_ACTIONS = ["PAC", "Dice", "Map", "Terrain"]

RED = "#ff0000"


def double_click(card, x=0, y=0):
    mute()
    
    if card.properties["Unit Type"] == "Dice":
        roll_dice(table, 0, 0)
        return
    
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
        
    add_action(card)


def add_action(card):
    mute()
    
    
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
    
    elif card.markers[ACTION_MARKER] >=2: 
        whisper("{} already has two Action tokens.".format(card))
        return
    
    else:
        card.markers[ACTION_MARKER] += 1
        notify("{} gives {} an Action token.".format(me, card))


def remove_action(card, x=0, y=0):
    mute()
    
    if ACTION_MARKER in card.markers:
        card.markers[ACTION_MARKER] -= 1
        notify("{} removes an Action token from {}.".format(me, card))


def take_one_damage(card, x=0, y=0):
    mute()
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
    clicks = [a for a in card.alternates]
    current_click = card.alternate
    current_index = clicks.index(current_click)
    if current_index == len(card.alternates) - 1:
        notify("{} is already on its last click.".format(card.Name))
    else:
        current_index += 1
        card.alternate = card.alternates[current_index]
        notify("{} takes one damage and goes to click {}.".format(card, current_index))

def take_x_damage(card, x=0, y=0):
    mute()
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
    damage = askInteger("How many clicks of damage?", 0)
    clicks = [a for a in card.alternates]
    current_click = card.alternate
    current_index = clicks.index(current_click)
    
    if current_index == len(card.alternates) - 1:
        notify("{} is already on its last click.".format(card.Name))

    if current_index + damage >= len(card.alternates):
        card.alternate = card.alternate = "KO"
        notify("{} is KO'd!".format(card))

    else:
        current_index += damage
        card.alternate = card.alternates[current_index]
        notify("{} takes {} damage and goes to click {}.".format(card, damage, current_index))


def heal_one_damage(card, x=0, y=0):
    mute()
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
    clicks = [a for a in card.alternates]
    current_click = card.alternate
    current_index = clicks.index(current_click)
    if current_index <= 1:
        notify("{} is already on its first click.".format(card.Name))
    else:
        current_index -= 1
        card.alternate = card.alternates[current_index]
        notify("{} heals one damage and goes to click {}.".format(card, current_index))


def get_map_position(gamemap):
    if gamemap.size == "16x16":
        return (-800, -700)


def load_map(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"Map"}, title="Select a Map")
    if guid is None:
        return
        
    card = table.create(guid, 0, 0, quantity = 1, persist = False)
    position_map(card)


def position_map(card):
    mute()
    x, y = get_map_position(card)
    card.moveToTable(x, y)
    card.anchor = True
    card.index = 0

def rotate_map(card, x=0, y=0):
    mute()
    if card.orientation == 0:
        card.orientation = 2
    else:
        card.orientation = 0
    card.index = 0

def fix_position(card):
    mute()

    x, y = card.position

    x_remainder = x % 100
    if x_remainder <= 50:
        x -= x_remainder
    else:
        x += 100 - x_remainder

    y_remainder = y % 100
    if y_remainder <= 50:
        y -= y_remainder
    else:
        y += 100 - y_remainder

    card.moveToTable(x, y)
    card.index = 999
    
    
def table_config(args):
    mute()
    if args.player != me:
        return
    
    for card in args.cards:
        if is_map([card], 0, 0):
            position_map(card)
        else:
            idx = args.cards.index(card)
            if args.toGroups[idx] == table:
                fix_position(card)
            if args.fromGroups[idx] != table:
                make_model(card)


def make_model(card):
    mute()
    if card.properties["Unit Type"] == "Bystander":
        return
    offset = -100
    if me.isInverted:
        offset = 100
    if "Click1" in card.alternates:
        guid = card.model
        x, y = card.position
        fig = table.create(guid, x + offset, y)
        fig.alternate = "Click1"


def is_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] == "Map"

def is_not_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] != "Map"


DICE_FACES = {
    1: "Face1",
    2: "Face2",
    3: "Face3",
    4: "Face4",
    5: "Face5",
    6: "",
}


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
        dice.anchor


def _grab_dice(card):
    mute()
    p = card.controller
    remoteCall(p, "_pass_dice", [card, me])


def _pass_dice(card, player):
    mute()
    card.controller = player


def roll_single_die(group, x=0, y=0):
    mute()
    for card in table:
        if card.size == "Dice":
            if card.controller != me:
                _grab_dice(card)
        
    count = 0
    results = ""
    
    for card in table:
        if card.size == "Dice":
            if count < 1:
                face = rnd(1, 6)
                card.alternate = DICE_FACES[face]
                count += 1
                results += str(face)
    
    notify("{} rolled {} on a single die.".format(me, results))
    

def roll_d20(group, x=0, y=0):
    mute()
    roll = rnd(1, 20)
    notify("{} rolled {} on a d20.".format(me, roll))


def roll_dice(group, x=0, y=0):
    mute()

    for card in table:
        if card.size == "Dice":
            if card.controller != me:
                _grab_dice(card)
        
    total = 0
    results = ""
    
    for card in table:
        if card.size == "Dice":
            face = rnd(1, 6)
            card.alternate = DICE_FACES[face]
            total += face
            results += str(face) + ", "
    
    notify("{} rolled {}with a total of {}.".format(me, results, total))
    

def create_pac():
    mute()
    count = 0
    for card in table:
        if card.size == "PAC":
            count += 1
    if count >= 1:
        whisper("PAC is already on the table.")
        return
    else:
        x, y = PAC_POSITIONS
        table.create(PAC_GUID, x, y)
        

def create_bystander(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"Bystander"}, title="Generate a Bystander:")
    if guid is None:
        return
        
    card = me.Team.create(guid, quantity)
    
    
def create_terrain(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"Terrain"}, title="Generate a Terrain Tile:")
    if guid is None:
        return
    card = me.Team.create(guid, quantity)


def create_one_shot(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"One Shot"}, title="Generate a One Shot:")
    if guid is None:
        return
    card = me.Team.create(guid, quantity)

    
    
def flip_card(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))
        
        
def setup_table():
    mute()
    if me._id != 1:
        return
    create_dice()
    create_pac()