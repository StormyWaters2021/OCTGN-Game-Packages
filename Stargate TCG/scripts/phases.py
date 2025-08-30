NUMBER_PHASES = 3

PHASE_NOTES = {
    "Power Phase": "Both players gain 3 Power, plus 1 Power for each glyph beneath the hero player's characters. Power not spent this turn is lost at the end of the turn.",
    "Mission Phase": "The hero player plays their top Mission. Both players alternate taking actions, then determine the success or failure of the Mission. The hero player may choose to continue playing Missions after the first is resolved.",
    "Debrief Phase": "Both players ready all stopped cards. Then all failed Missions are placed on the bottom of the hero player's Mission pile. Both players refill their hands to 8 cards (or discard down to 8 if appropriate.",
}


def phase_process():
    if getActivePlayer() != me:
        return
    if currentPhase()[1] >= NUMBER_PHASES:
        if len(players) == 1:
            return
        _set_power(0)
        players[1].setActive()
        notify("{} passes the turn.".format(me))
    else:
        setPhase(currentPhase()[1]+1)
        

def _set_power(power):
    mute()
    me.counters['Power'].value = power
    notify("{} sets their Power to {}.".format(me, power))
    if getActivePlayer() == me:
        remoteCall(players[1], "_set_power", [power])


def phase_actions(args):
    if getActivePlayer() != me:
        return
    if getGlobalVariable("phase_actions") != "True":
        return
    notes = False
    if getGlobalVariable("phase_notes") == "True":
        notes = True
        
    phase = currentPhase()[0]
    whisper("Phase: {}".format(phase))
    if phase == "Power Phase": # gain power
        if notes:
            notify(PHASE_NOTES["Power Phase"])
    elif phase == "Mission Phase": # get top mission
        start_mission_phase()
        if notes:
            notify(PHASE_NOTES["Mission Phase"])
    elif phase ==  "Debrief Phase":
        # start_debrief_phase()
        if notes:
            notify(PHASE_NOTES["Debrief Phase"])
    else:
        return


def start_mission_phase(decide = False):
    pos = get_my_position()
    if decide:
        x, y = pos["failed_mission"]
        failed_mission(x, y, pos["invert_mod"])
    x, y = pos["mission"]
    mission = me.piles["Mission Pile"].top()
    mission.moveToTable(x, y, False)
    mission.anchor = True
    
    
def failed_mission(x=0, y=0, invert_mod=1):
    global fail_offset
    for card in table:
        if card.controller == me:
            if card.position == pos["mission"]:
                card.moveToTable(x + (invert_mod * 20), y)
                card.orientation = 1
    fail_offset += 1