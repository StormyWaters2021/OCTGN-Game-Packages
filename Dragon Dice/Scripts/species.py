def get_terrain_elements(terrain_list):
    element_list = []
    for die in table: 
        if die._id in terrain_list:
            for element in TERRAIN_ELEMENTS:
                if element in die.Element and element not in element_list:
                    element_list.append(element)
    return element_list


def maneuver_as_save(die):
    result = die.Icons.split(" ")
    if result[1] == "Maneuver" or result[1] in MANEUVER["count"]:
        return int(result[0])
    else: return 0


def melee_as_maneuver(die):
    result = die.Icons.split(" ")
    if result[1] == "Melee" or result[1] in MELEE["count"]:
        return int(result[0])
    else: return 0
        
        
def save_as_melee(die):
    result = die.Icons.split(" ")
    if result[1] == "Save" or result[1] in SAVE["count"]:
        return int(result[0])
    else: return 0


def maneuver_as_melee(die):
    result = die.Icons.split(" ")
    if result[1] == "Maneuver" or result[1] in MANEUVER["count"]:
        return int(result[0])
    else: return 0


def species_check(die, location, action_word):

    immediate = 0  # always-applied bonus that we return
    bonus = 0      # temporary holder for conditional bonuses

    global dwarves
    global feral
    global firewalkers
    global scalders

    terrain_ids = get_terrain_ids(location)
    element_list = get_terrain_elements(terrain_ids)

    # Coral Elves: Save icons may count as Maneuver in Green (Water)
    if die.Species == "Coral Elves" and "Green (Water)" in element_list and action_word == "Save":
        immediate += maneuver_as_save(die)

    # Dwarves:
    # - In Yellow (Earth) during Maneuver, Melee can count as Maneuver (immediate bonus)
    # - In Red (Fire) during Melee, Save can count as Melee, but that bonus is conditional
    #   and stored for later (e.g. counter-attack rules).
    elif die.Species == "Dwarves":
        if "Yellow (Earth)" in element_list and action_word == "Maneuver":
            immediate += melee_as_maneuver(die)
        elif "Red (Fire)" in element_list and action_word == "Melee":
            bonus = save_as_melee(die)
            dwarves += bonus

    # Feral: conditional Maneuver-as-Melee bonus in Blue+Yellow during Melee
    elif die.Species == "Feral" and "Blue (Air)" in element_list and "Yellow (Earth)" in element_list and action_word == "Melee":
        bonus = maneuver_as_melee(die)
        feral += bonus

    # Fire Walkers: conditional Save-as-Melee bonus in Red during Melee
    elif die.Species == "Fire Walkers" and "Red (Fire)" in element_list and action_word == "Melee":
        bonus = save_as_melee(die)
        firewalkers += bonus

    # Goblins: Melee can count as Maneuver in Yellow (Earth) during Maneuver
    elif die.Species == "Goblins" and "Yellow (Earth)" in element_list and action_word == "Maneuver":
        immediate += melee_as_maneuver(die)

    # Lava Elves: Maneuver can count as Save in Red (Fire) during Save rolls
    elif die.Species == "Lava Elves" and "Red (Fire)" in element_list and action_word == "Save":
        immediate += maneuver_as_save(die)

    # Scalders: conditional Maneuver-as-Save bonus in Green (Water) during Save
    elif die.Species == "Scalders" and "Green (Water)" in element_list and action_word == "Save":
        bonus = maneuver_as_save(die)
        scalders += bonus

    # Swamp Stalkers: Maneuver can count as Save in Green (Water) during Save rolls
    elif die.Species == "Swamp Stalkers" and "Green (Water)" in element_list and action_word == "Save":
        immediate += maneuver_as_save(die)

    # If none of the above matched, immediate stays 0.
    return immediate
