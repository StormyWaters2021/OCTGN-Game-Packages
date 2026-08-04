def position(card, x=0, y=0):
    position = card.position
    whisper("Position = {}.".format(str(position)))
    
    
def fail_check(*args):
    return False