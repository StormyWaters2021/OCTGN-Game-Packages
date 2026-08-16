LOS_TYPES = {
    (0, 1): 'LOS0x1',
    (1, 10): 'LOS1x10',
    (1, 9): 'LOS1x9',
    (1, 8): 'LOS1x8',
    (1, 7): 'LOS1x7',
    (1, 6): 'LOS1x6',
    (1, 5): 'LOS1x5',
    (2, 9): 'LOS2x9',
    (1, 4): 'LOS1x4',
    (2, 7): 'LOS2x7',
    (3, 10): 'LOS3x10',
    (1, 3): 'LOS1x3',
    (3, 8): 'LOS3x8',
    (2, 5): 'LOS2x5',
    (3, 7): 'LOS3x7',
    (4, 9): 'LOS4x9',
    (1, 2): 'LOS1x2',
    (5, 9): 'LOS5x9',
    (4, 7): 'LOS4x7',
    (3, 5): 'LOS3x5',
    (5, 8): 'LOS5x8',
    (2, 3): 'LOS2x3',
    (7, 10): 'LOS7x10',
    (5, 7): 'LOS5x7',
    (3, 4): 'LOS3x4',
    (7, 9): 'LOS7x9',
    (4, 5): 'LOS4x5',
    (5, 6): 'LOS5x6',
    (6, 7): 'LOS6x7',
    (7, 8): 'LOS7x8',
    (8, 9): 'LOS8x9',
    (9, 10): 'LOS9x10',
    (1, 1): 'LOS1x1',
}


def compute_gcf(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)

LOS_GUID = '056ca248-4adc-43df-9bfd-9cf64571972e'
LOS_OFFSET = 1000

def _draw_los_line(*args):
    mute()
    if me._id != 1:
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

        los_line = "LOS" + str(short) + "x" + str(long) + mirror 
    
    for card in table:
        if card.model == LOS_GUID:
            card.moveToTable(fromx - LOS_OFFSET, fromy - LOS_OFFSET)
            card.alternate = los_line
            card.orientation = rotation