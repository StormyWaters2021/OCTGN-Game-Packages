attach_dict = {}


def attach_card(args):
    if args.player != me:
        return
    if args.fromCard is None:
        return
    if args.toCard is None:
        return
    attach_dict[args.fromCard] = args.toCard
    whisper("Full Dict: {}, From: {}, To: {}.".format(attach_dict, args.fromCard, args.toCard))
    notify("{} attaches {} to {}.".format(me, args.fromCard, args.toCard))
    
    
    update_attached_position()
    clear_attach_targets()


def update_attached_position():
    cards = list(attach_dict.keys())
    if len(cards) < 1:
        return
    for card in cards:
        x, y = attach_dict[card].position
        card.moveToTable(x+20, y+20)


def clear_attach_targets():
    for card in table:
        if card.controller == me:
            card.target(active = False)