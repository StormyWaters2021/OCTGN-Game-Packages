def nextPhase(*args):
    if getActivePlayer() != me:
        return
    phase = currentPhase()[1]
    if phase >= 7:
        if len(players) == 1:
            return
        players[1].setActive()
        notify("{} passes the turn.".format(me))
    else:
        setPhase(phase+1)
        phase_name = currentPhase()[0]
        notify("{} advances to the {}.".format(me, phase_name))


def phase_check(number):
    if getActivePlayer() != me:
        return False
    if currentPhase()[1] == number:
        return True
    else: return False
    

# def checkBrief(*args):
    # check = phase_check(1)
    # return check
    

# def checkHeal(*args):
    # check = phase_check(2)
    # return check
    
    
# def checkReq(*args):
    # check = phase_check(3)
    # return check
    
    
# def checkDep(*args):
    # check = phase_check(4)
    # return check
    
    
# def checkCase(*args):
    # check = phase_check(5)
    # return check
    
    
# def checkInv(*args):
    # check = phase_check(6)
    # return check
    
    
# def checkDebrief(*args):
    # check = phase_check(7)
    # return check
    
    
