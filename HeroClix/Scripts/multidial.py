GALACTUS = "1fddb83d-8c87-4403-9ea2-eaa2f9d6a58b"
GALACTUS_CONVERTER = "ffce23a6-3530-4c1a-89cc-5df238e5d9ae"
GALACTUS_HERALD = "ef162aa8-ada3-415f-9f2e-062e564adb05"

MULTI_DIAL = {
    GALACTUS: [GALACTUS_CONVERTER, GALACTUS_HERALD],
}

MULTI_DIAL_LIST = [GALACTUS, GALACTUS_CONVERTER, GALACTUS_HERALD, ]


def _is_galactus(cards, x=0, y=0):
    mute()
    if cards[0].alternate == "":
        return False
    return cards[0].model == GALACTUS


def _find_multidial_base(guid):
    if guid in MULTI_DIAL:
        return guid

    for base, values in MULTI_DIAL.items():
        if guid in values:
            return base
    return None


def build_galactus(card, x, y):
    mute()
    _create_multidial(GALACTUS, x, y)
    

def advance_converter(card, x=0, y=0):
    mute()
    _advance_secondary_dial(card, 0)
    
    
def advance_herald(card, x=0, y=0):
    mute()
    _advance_secondary_dial(card, 1)


def _create_multidial(base, x, y):
    mute()
    if base not in MULTI_DIAL.keys():
        return
    
    for guid in MULTI_DIAL[base]:
        card = table.create(guid, x, y, quantity = 1, persist = True)
        card.alternate = card.alternates[1]
        card.anchor = True
    card = table.create(base, x, y, quantity = 1, persist = True)
    card.alternate = card.alternates[1]
    

def _move_multidial(card, old_x, old_y):
    mute()

    if card.model not in MULTI_DIAL:
        return
    
    if card.alternate == "":
        return

    new_x, new_y = card.position
    secondary_models = MULTI_DIAL[card.model]

    for secondary in table:
        if secondary.model not in secondary_models:
            continue

        x, y = secondary.position

        if x == old_x and y == old_y:
            secondary.moveToTable(new_x, new_y)
            snap_to_grid(secondary)

    snap_to_grid(card)


def _advance_secondary_dial(card, dial_list_idx):
    mute()
    if card.alternate == "":
        return
        
    guid = card.model
    
    if guid not in MULTI_DIAL:
        return False

    if dial_list_idx < 0 or dial_list_idx >= len(MULTI_DIAL[guid]):
        return False

    x, y = card.position
    secondary_guid = MULTI_DIAL[guid][dial_list_idx]

    for item in table:
        if item.model == secondary_guid and item.position == (x, y):
            return _advance_dial(item)

    return False
    

