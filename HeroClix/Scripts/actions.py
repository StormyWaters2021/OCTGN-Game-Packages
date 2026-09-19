def double_click(card, x=0, y=0):
    mute()
    
    if card.properties["Unit Type"] == "Dice":
        roll_dice(table, 0, 0)
        return
    
    if card.model == LOS_GUID:
        _reset_los(card)
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


def add_custom_marker(card, x=0, y=0):
    mute()
    marker, qty = askMarker()
    if qty == 0:
        return
    card.markers[marker] += qty
    notify("{} puts a {} counter on {}.".format(me, marker[0], card))
    

def remove_action(card, x=0, y=0):
    mute()
    
    if ACTION_MARKER in card.markers:
        card.markers[ACTION_MARKER] -= 1
        notify("{} removes an Action token from {}.".format(me, card))


def _get_click_name(card):
    mute()
    click_name = None
    if "Click" in card.alternate:
        click_name = card.alternate.replace("Click", "Click ")
    elif card.alternate == "KO":
        click_name = "KO"
    
    return click_name
    

def _advance_dial(card):
    mute()
    
    multi_click = _multidial_active_check(card)
    if multi_click is None:
        return False
    if multi_click is not False:
        active_card = _find_multidial_active(card, multi_click)
    
        if active_card is None:
            whisper("The active dial could not be found.")
            return False
        
        card = active_card
    
    clicks = [a for a in card.alternates]
    current_click = card.alternate
    current_index = clicks.index(current_click)
    if current_index == len(card.alternates) - 1:
        return False
    else:
        current_index += 1
        card.alternate = card.alternates[current_index]
        return True


def _retreat_dial(card):
    mute()
    
    multi_click = _multidial_active_check(card)
    if multi_click is None:
        return False
    if multi_click is not False:
        active_card = _find_multidial_active(card, multi_click)
    
        if active_card is None:
            whisper("The active dial could not be found.")
            return False
        
        card = active_card
    
    clicks = [a for a in card.alternates]
    current_click = card.alternate
    current_index = clicks.index(current_click)
    if current_index <= 1:
        return False
    else:
        current_index -= 1
        card.alternate = card.alternates[current_index]
        return True


def take_one_damage(card, x=0, y=0):
    mute()
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
    if _advance_dial(card):
        click_name = _get_click_name(card)
        if click_name:
            notify("{} advances to {}.".format(card, click_name))


def take_x_damage(card, x=0, y=0):
    mute()
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
    original_card = card
    multi_click = _multidial_active_check(card)
    if multi_click is None:
        return False
    if multi_click is not False:
        active_card = _find_multidial_active(card, multi_click)
    
        if active_card is None:
            whisper("The active dial could not be found.")
            return False
        
        card = active_card
    
    damage = askInteger("How many clicks of damage?", 0)
    clicks = [a for a in card.alternates]
    current_click = card.alternate
    current_index = clicks.index(current_click)
    
    if current_index == len(card.alternates) - 1:
        notify("{} is already on its last click.".format(original_card.Name))
        return

    if current_index + damage >= len(card.alternates):
        card.alternate = "KO"
        notify("{} is KO'd!".format(original_card))

    else:
        old_click = _get_click_name(card)
        current_index += damage
        card.alternate = card.alternates[current_index]
        new_click = _get_click_name(card)
        notify("{} advances from {} to {}.".format(original_card, old_click, new_click))


def heal_one_damage(card, x=0, y=0):
    mute()
    if card.properties["Unit Type"] in NO_ACTIONS:
        return
    if _retreat_dial(card):
        click_name = _get_click_name(card)
        if click_name:
            notify("{} reverses to {}.".format(card, click_name))


def snap_to_grid(card):
    mute()

    x, y = card.position
    x, y = _compensate_report_for_rotation(card, x, y)

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
    card.sendToFront()
    
  
def table_config(args):
    mute()

    if args.player != me:
        return

    movement_report = ""

    for idx, card in enumerate(args.cards):
        card.target(False)
        
        if card.model == LOS_GUID:
            _reset_los(card)
        
        if args.fromGroups[idx] != table and args.toGroups[idx] == table:
            make_model(card)

        if is_map([card], 0, 0):
            if args.toGroups[idx] == table:            
                snap_to_grid(card)
                _sync_map_rotation(card)
                card.sendToBack() 

        elif card.model in MULTI_DIAL_LIST:
            base = _find_multidial_base(card.model)

            if card.model == base and card.alternate != "":
                _move_multidial(card, args.xs[idx], args.ys[idx])

        else:
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


def rotate_model(card, x=0, y=0):
    mute()

    old_x, old_y = card.position
    offsetx, offsety = _rotation_offset(card)

    

    if card.properties["Unit Type"] == "Character":
        new_orientation = 1 if card.orientation == 0 else 0
    else:
        new_orientation = (card.orientation + 1) % 4

    new_x = old_x
    new_y = old_y

    if card.size in NOT_SQUARE_SIZES:
        if card.orientation in (0, 2):
            new_x += offsetx
            new_y += offsety
        else:
            new_x -= offsetx
            new_y -= offsety

    if card.model in MULTI_DIAL and card.alternate != "":
        secondary_models = MULTI_DIAL[card.model]

        for secondary in table:
            if secondary.model not in secondary_models:
                continue

            if secondary.position != (old_x, old_y):
                continue

            secondary.orientation = new_orientation
            secondary.moveToTable(new_x, new_y)

    card.orientation = new_orientation
    card.moveToTable(new_x, new_y)


def flip_card(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))        


def make_model(card):
    mute()
    x, y = card.position
    if card.isInverted():
        offsetx = card.width
        offsety = card.height - GRID_SIZE
    else:
        offsetx = -GRID_SIZE
        offsety = 0
        
    base = _find_multidial_base(card.model)
    if base is not None:
        _create_multidial(base, x, y + 200)
        return
        
    if "Click1" in card.alternates:
        guid = card.model
        fig = table.create(guid, x + offsetx, y + offsety)
        fig.alternate = "Click1"
    elif "Tile" in card.alternates:
        guid = card.model
        fig = table.create(guid, x + offsetx, y + offsety)
        fig.alternate = "Tile"
    elif len(card.alternates) > 0 and card.alternates[1].size == "1x1":
        guid = card.model
        fig = table.create(guid, x + offsetx, y + offsety)
        fig.alternate = fig.alternates[1]


def duplicate_model(card, x=0, y=0):
    mute()
    guid = card.model
    alt = card.alternate
    fig = table.create(guid, x + 150, y)
    fig.alternate = alt
    notify("{} creates a copy of {}.".format(me, card))


def delete_card(card, x = 0, y = 0):
    mute()
    choice = confirm("Are you sure you want to delete this object? This cannot be undone.")
    if choice:
        card.delete()


def swap_to_wreck(card, x=0, y=0):
    mute()
    if card.model not in WRECKABLE.keys():
        return

    x, y = card.position
    wreck = table.create(WRECKABLE[card.model], x, y)
    wreck.alternate = wreck.alternates[1]
    card.delete()

##########################
##     Check Types      ##
##########################

def is_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] == "Map"

def is_not_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] != "Map"

def is_one_shot(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] == "One Shot"

def _is_wreckable(card, x=0, y=0):
    return card[0].model in WRECKABLE.keys()
    
def has_map_image(card, x=0, y=0):
    mute()
    if "Image" in card[0].alternates:
        return True
    else:
        return False

def _is_arena_cap(card, x=0, y=0):
    mute()
    return card[0].model == ARENA_CAP

##########################
##    Create Objects    ##
##########################

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


def _make_color_list(buttonlist):
    mute()
    colorlist = []
    count = 0
    for i in buttonlist:
        colorlist.append(BUTTON_COLORS[count])
        count += 1
        if count == len(BUTTON_COLORS):
            count = 0
    return colorlist


def create_character_filtered(group, x=0, y=0):
    mute()
    lookup_dict = {}
    
    message = "Look up characters by:"
    buttonList = ["Keywords", "Team Abilities", ]
    colorList = _make_color_list(buttonList)
    filter_choice = askChoice(message, buttonList, colorList)
    if filter_choice == 0:
        return
    new_key = buttonList[filter_choice - 1] + " Search"
    
    message = "Choose one:"
    buttonList = [i for i in FILTER_CHOICE_LIST[filter_choice - 1]]
    colorList = _make_color_list(buttonList)
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
    

def create_arena_tile(card, x=0, y=0):
    x, y = card.position
    table.create(ARENA_TILE, x, y)