def compute_gcf(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)

LOS_GUID = '0eccc91f-84e5-4426-9860-a5a0f7bf3517'
LOS_OFFSET = 1000
LOS_BASE_X = -1600
LOS_BASE_Y = -150


def create_los():
    mute()
    table.create(LOS_GUID, LOS_BASE_X, LOS_BASE_Y)


def _reset_los(card):
    mute()
    card.alternate = ""
    card.orientation = 0
    card.moveToTable(LOS_BASE_X, LOS_BASE_Y)


def _draw_los_line(args):
    mute()
    if me._id != 1:
        return
    if not args.targeted:
        return

    # We may need to rotate the line later
    rotation = 0
    
    # Get the position of the two characters
    fromx, fromy = args.fromCard.position
    tox, toy = args.toCard.position
    
    # Find the difference between them for determining A or B slopes
    x_diff = tox - fromx
    y_diff = toy - fromy
    
    # Get the absolute value between them
    x_offset = abs(x_diff)
    y_offset = abs(y_diff)
    
    # Convert that to number of spaces along each axis
    x_spaces = x_offset // GRID_SIZE
    y_spaces = y_offset // GRID_SIZE
    
    # Do we need to rotate?
    if y_spaces > x_spaces:
        rotation = 1
    
    # Do we need the mirrored slope?
    same_sign = False
    if x_diff > 0 and y_diff > 0:
        same_sign = True
    if x_diff < 0 and y_diff < 0:
        same_sign = True
    
    # Lines are stored as LOS#x# where the numbers are small to large, so we need to know which is which
    short = min(x_spaces, y_spaces)
    long = max(x_spaces, y_spaces)
    
    if short == 0 and long == 0:
        return
    
    # Get the greatest common factor between the two to reduce our slope
    gcf = compute_gcf(short, long)
    short = short // gcf
    long = long // gcf
    
    # Set the horizontal line if the slope is 0
    if short == 0:
        los_line = "LOS0x1"

    # Set the 45 degree line if the slope is exactly 1
    elif short == long:
        los_line = "LOS1x1"

        if not same_sign:
            rotation = 1
    
    # Otherwise determine if the slope needs to be mirrored
    else:
        if rotation == 0:
            mirror = "A" if same_sign else "B"
        else:
            mirror = "B" if same_sign else "A"

        los_line = "LOS" + str(int(short)) + "x" + str(int(long)) + mirror 
    
    count = 0
    for card in table:
        if card.model == LOS_GUID:
            count += 1
            card.moveToTable(fromx - LOS_OFFSET, fromy - LOS_OFFSET)
            card.alternate = los_line
            card.orientation = rotation
            
    if count < 1:
        line = table.create(LOS_GUID, fromx - LOS_OFFSET, fromy - LOS_OFFSET)
        line.alternate = los_line
        line.orientation = rotation
        