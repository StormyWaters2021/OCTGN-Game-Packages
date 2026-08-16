def double_click(card, x=0, y=0):
    mute()
    
    if card.properties["Unit Type"] == "Dice":
        roll_dice(table, 0, 0)
        return
    
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
        
    add_action(card)


def calculate_attack(card, x=0, y=0):
    mute()
    total = askInteger("What is your attack value?", 0)
    roll = roll_dice("quiet", 0, 0)
    notify("{} attacks with a value of {} and a roll of {} for a total of {}.".format(card, total, roll, total+roll))


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



def snap_to_grid(card):
    mute()

    x, y = card.position

    x_remainder = x % GRID_SIZE
    if x_remainder <= GRID_SIZE / 2:
        x -= x_remainder
    else:
        x += GRID_SIZE - x_remainder

    y_remainder = y % GRID_SIZE
    if y_remainder <= GRID_SIZE / 2:
        y -= y_remainder
    else:
        y += GRID_SIZE - y_remainder
    
    newx, newy = _compensate_for_rotation(card, x, y)
    card.moveToTable(newx, newy)
    card.index = 999
    

def _compensate_for_rotation(card, x, y):
    mute()
    if card.orientation == 1:
        if card.size in NOT_SQUARE_SIZES:
            return (x, y + GRID_SIZE)
    return (x, y)

def _compensate_report_for_rotation(card, x, y):
    mute()
    if card.orientation == 1:
        if card.size in NOT_SQUARE_SIZES:
            return (x, y - GRID_SIZE)
    return (x, y)

  
def table_config(args):
    mute()
    if args.player != me:
        return
    
    movement_report = ""
    
    for card in args.cards:
        if is_map([card], 0, 0):
            _position_map(card)
        else:
            idx = args.cards.index(card)
            
            if args.toGroups[idx] == table:
                snap_to_grid(card)
                x = args.xs[idx]
                y = args.ys[idx]
                startx, starty = _compensate_report_for_rotation(card, x, y)
                start_position = _report_movement(startx, starty)
                if start_position != None:
                    movement_report += card.name + " moves from " + start_position + " to "
                    x, y = card.position
                    newx, newy = _compensate_report_for_rotation(card, x, y)
                    end_position = _report_movement(newx, newy)
                    if end_position != None:
                        movement_report += end_position + "."
                        notify(movement_report)
            if args.fromGroups[idx] != table:
                make_model(card)
            

def rotate_model(card, x=0, y=0):
    mute()
    rotation = card.orientation
    if rotation == 0:
        card.orientation = 1
    else:
        card.orientation = 0

def make_model(card):
    mute()
    # if card.properties["Unit Type"] == "Bystander":
        # return
    offset = -100
    if me.isInverted:
        offset = 100
    if "Click1" in card.alternates:
        guid = card.model
        x, y = card.position
        fig = table.create(guid, x + offset, y)
        fig.alternate = "Click1"
    elif "Tile" in card.alternates:
        guid = card.model
        x, y = card.position
        fig = table.create(guid, x + offset, y)
        fig.alternate = "Tile"


def is_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] == "Map"

def is_not_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] != "Map"

def is_one_shot(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] == "One Shot"


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
    if group != "quiet":
        notify("{} rolled {}with a total of {}.".format(me, results, total))
    return total
    

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
    guid, quantity = askCard({"Unit Type":"Terrain Marker"}, title="Generate a Terrain Tile:")
    if guid is None:
        return
    card = me.Team.create(guid, quantity)


def create_one_shot(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"One Shot"}, title="Generate a One Shot:")
    if guid is None:
        return
    card = me.Team.create(guid, quantity)


def create_character_filtered(group, x=0, y=0):
    mute()
    lookup_dict = {}
    
    message = "Look up characters by:"
    buttonList = ["Keywords", "Team Abilities", ]
    colorList = ['#FF0000' for i in buttonList]
    filter_choice = askChoice(message, buttonList, colorList)
    if filter_choice == 0:
        return
    new_key = buttonList[filter_choice - 1] + " Search"
    
    message = "Choose one:"
    buttonList = [i for i in FILTER_CHOICE_LIST[filter_choice - 1]]
    colorList = ['#FF0000' for i in buttonList]
    choice = askChoice(message, buttonList, colorList)
    if choice == 0:
        return
    
    search = "| " + buttonList[choice - 1] + " |"
    
    lookup_dict[new_key] = search
    
    guid_list = queryCard(properties = lookup_dict, exact = False)
    if len(guid_list) == 0:
        whisper("No matches found.")
        return
    
    chosen_card, quantity = askCard(properties = {"Model": guid_list}, operator = "or", title = "Select a Character: ")
    if chosen_card is None:
        return
    
    me.Team.create(chosen_card, quantity)
    

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
    initializeGame()
    if me._id != 1:
        return
    create_dice()
    create_pac()