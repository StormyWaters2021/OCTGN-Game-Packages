ACTION_MARKER = ("Action", "action_marker")
ACTION_MARKERX2 = ("2x Action", "action_marker_x2")

def add_action(card, x=0, y=0):
    mute()
    if ACTION_MARKER in card.markers:
        card.markers[ACTION_MARKER] = 0
        card.markers[ACTION_MARKERX2] = 1
        notify("{} gives {} a second Action token.".format(me, card))
    else: 
        card.markers[ACTION_MARKER] = 1
        notify("{} gives {} an Action token.".format(me, card))


def remMarker(card, x=0, y=0):
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