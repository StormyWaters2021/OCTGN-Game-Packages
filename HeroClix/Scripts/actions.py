ACTION_MARKER = ("Action", "action_marker")
ACTION_MARKERX2 = ("2x Action", "action_marker_x2")

def add_action(card, x=0, y=0):
    mute()
    if ACTION_MARKER in card.markers:
        card.markers[ACTION_MARKER] = 0
        card.markers[ACTION_MARKERX2] = 1
        notify("{} gives {} a second Action token.".format(me, card))
    
    elif ACTION_MARKERX2 in card.markers: 
        whisper("{} already has two Action tokens.".format(card))
        return
        
    else:
        card.markers[ACTION_MARKER] = 1
        notify("{} gives {} an Action token.".format(me, card))


def remove_action(card, x=0, y=0):
    mute()
    if ACTION_MARKERX2 in card.markers:
        card.markers[ACTION_MARKERX2] = 0
        card.markers[ACTION_MARKER] = 1
        notify("{} removes the second Action token from {}.".format(me, card))
    elif ACTION_MARKER in card.markers: 
        card.markers[ACTION_MARKER] = 0
        notify("{} clears all Action tokens from {}.".format(me, card))


def take_one_damage(card, x=0, y=0):
    clicks = [a for a in card.alternates]
    current_click = card.alternate
    current_index = clicks.index(current_click)
    if current_index == len(card.alternates) - 1:
        notify("{} is already on its last click.".format(card.Name))
    else:
        current_index += 1
        card.alternate = card.alternates[current_index]
        notify("{} takes one damage and goes to click {}.".format(card, current_index))
        

def get_map_position(gamemap):
    if gamemap.size == "16x16":
        return (-800, -700)


def load_map(group, x=0, y=0):
    mute()
    guid, quantity = askCard({"Unit Type":"Map"}, title="Select a Map")
    if guid is None:
        return
        
    card = table.create(guid, 0, 0, quantity = 1, persist = False)
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
    
    
def table_config(args):
    mute()
    if args.player != me:
        return
    for card in args.cards:
        fix_position(card)
        
    for card in table:
        if card.properties["Unit Type"] == "Map":
            card.index = 0

def is_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] == "Map"

def is_not_map(card, x=0, y=0):
    mute()
    return card[0].properties["Unit Type"] != "Map"
