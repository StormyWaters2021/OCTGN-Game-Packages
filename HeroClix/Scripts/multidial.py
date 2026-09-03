GALACTUS = "1fddb83d-8c87-4403-9ea2-eaa2f9d6a58b"
GALACTUS_CONVERTER = "ffce23a6-3530-4c1a-89cc-5df238e5d9ae"
GALACTUS_HERALD = "ef162aa8-ada3-415f-9f2e-062e564adb05"

VENOM_GALACTUS = "fc3fe1ca-34f8-4e92-af49-e14bb0be2ae4"
VG_TENDRILS = "650df7ac-847b-49f9-a785-81b21ed9f63d"
VG_BREAKER = "73e8df4a-9d46-4c56-a993-efd0efe5dafe"
VG_MAW = "1e64fbb4-8e8c-4f27-9a45-fdec59fe1af3"
VG_HUNGER = "c5ab1d84-9c9b-42d1-9356-57f758af7208"

MULTI_DIAL = {
    GALACTUS: [GALACTUS_CONVERTER, GALACTUS_HERALD],
    VENOM_GALACTUS: [VG_TENDRILS, VG_BREAKER, VG_MAW, VG_HUNGER],
            }

MULTI_DIAL_LIST = [item for key, value in MULTI_DIAL.items() for item in [key] + value]


# # GALACTUS # #

def _is_galactus(cards, x=0, y=0):
    mute()
    if cards[0].alternate == "":
        return False
    return cards[0].model == GALACTUS


def build_galactus(card, x, y):
    mute()
    _create_multidial(GALACTUS, x, y)
    

def advance_converter(card, x=0, y=0):
    mute()
    _advance_secondary_dial(card, 0)
    
    
def advance_herald(card, x=0, y=0):
    mute()
    _advance_secondary_dial(card, 1)


def reverse_converter(card, x=0, y=0):
    mute()
    _reverse_secondary_dial(card, 0)
    
    
def reverse_herald(card, x=0, y=0):
    mute()
    _reverse_secondary_dial(card, 1)


# # VENOM GALACTUS # # 

def _is_venom_galactus(cards, x=0, y=0):
    mute()
    if cards[0].alternate == "":
        return False
    return cards[0].model == VENOM_GALACTUS
    

def build_venom_galactus(card, x, y):
    mute()
    _create_multidial(VENOM_GALACTUS, x, y)


def set_venom_galactus_active_dial(card, x=0, y=0):
    mute()
    choiceList = ['Tendrils', 'Planet Breaker', 'Maw', ]
    colorsList = ['#FF0000', '#00FF00', '#0000FF', ] 
    choice = askChoice("Select a dial to become active:", choiceList, colorsList)
    if choice == 0:
        whisper("No dial selected.")
    else:
        card.multidial_active = str(choice-1)
        notify("{} has selected {} to be the active dial.".format(me, choiceList[choice-1]))


def notify_venom_galactus_active_dial(card, x=0, y=0):
    mute()
    dials = ['Tendrils', 'Planet Breaker', 'Maw', ]
    active_dial = _multidial_active_check(card)
    if active_dial is None or active_dial is False:
        return
    else:
        notify("{} is the active dial for {}.".format(dials[active_dial], card))
        

def advance_tendrils(card, x=0, y=0):
    mute()
    _advance_secondary_dial(card, 0)

    
def advance_breaker(card, x=0, y=0):
    mute()
    _advance_secondary_dial(card, 1)


def advance_maw(card, x=0, y=0):
    mute()
    _advance_secondary_dial(card, 2)


def advance_hunger(card, x=0, y=0):
    mute()
    notify("{} advances {}'s Cosmic Hunger.".format(me, card))
    _advance_secondary_dial(card, 3)


def reverse_tendrils(card, x=0, y=0):
    mute()
    _reverse_secondary_dial(card, 0)

    
def reverse_breaker(card, x=0, y=0):
    mute()
    _reverse_secondary_dial(card, 1)


def reverse_maw(card, x=0, y=0):
    mute()
    _reverse_secondary_dial(card, 2)


def reverse_hunger(card, x=0, y=0):
    mute()
    notify("{} reverses {}'s Cosmic Hunger.".format(me, card))
    _reverse_secondary_dial(card, 3)


# # HELPERS # # 

def _multidial_active_check(card):
    if "multidial_active" not in card.properties:
        return False
    if card.multidial_active == "":
        return False
    if card.multidial_active == "None":
        whisper("No active dial selected, please select a dial from the right-click menu first.")
        return None
    num = int(card.multidial_active)
    return num


def _find_multidial_base(guid):
    if guid in MULTI_DIAL:
        return guid

    for base, values in MULTI_DIAL.items():
        if guid in values:
            return base
    return None


def _find_multidial_active(card, dial_number):
    main_guid = card.model
    if main_guid not in MULTI_DIAL.keys():
        return card
    x, y = card.position
    for i in table:
        ix, iy = i.position
        if ix == x and iy == y:
            if i.model == MULTI_DIAL[main_guid][dial_number]:
                return i
    
    
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
    

def _reverse_secondary_dial(card, dial_list_idx):
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
            return _retreat_dial(item)

    return False