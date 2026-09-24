# Sealed Product Generator for OCTGN

# URL that accepts HTTP GET requests from OCTGN and returns string formatted responses.
API_BASE = "https://sealed.tcgbuilder.net"

# Game GUID to locate correct endpoint
GAME_GUID = "dabf7f85-249a-48ee-9d42-8f59adf60185"

# STRING name of group where pulls should be placed. Must be a PILE, not table. 
PACK_CONTENTS_GROUP = "Team"


def sealed_product(group, x=0, y=0):
    mute()

    message = "Choose One:"
    button_list = [
        "Generate Product by Set",
        "Generate Product by Code",
    ]

    choice = askChoice(message, button_list)

    if choice == 0:
        return

    if choice == 1:
        generate_product_by_set()
    elif choice == 2:
        generate_product_by_code()


def generate_product_by_set():
    url = API_BASE + "/octgn/sets?gameid=" + GAME_GUID

    response, status = webRead(url)

    if status != 200:
        whisper("Unable to contact the sealed product server.")
        return

    if response.startswith("ERROR"):
        show_error(response)
        return

    set_ids = []
    set_names = []

    lines = response.splitlines()

    for line in lines:
        parts = line.split("\t")

        if len(parts) >= 4:
            if parts[0] == "SET":
                set_ids.append(parts[1])
                set_names.append(parts[3])

    if len(set_ids) == 0:
        whisper("No sealed product sets are available for this game.")
        return

    choice = askChoice("Choose a Set:", set_names)

    if choice == 0:
        return

    set_id = set_ids[choice - 1]

    choose_product(set_id)


def choose_product(set_id):
    message = "Choose a Product:"
    button_list = [
        "Case",
        "Brick",
        "Pack",
    ]

    choice = askChoice(message, button_list)

    if choice == 0:
        return

    if choice == 1:
        product = "case"
    elif choice == 2:
        product = "box"
    elif choice == 3:
        product = "pack"
    else:
        return

    url = API_BASE + "/octgn/generate"
    url += "?gameid=" + GAME_GUID
    url += "&set=" + set_id
    url += "&product=" + product

    response, status = webRead(url)

    if status != 200:
        whisper("Unable to generate the sealed product.")
        return

    if response.startswith("ERROR"):
        show_error(response)
        return

    create_product(response)


def generate_product_by_code():
    code = askString("Enter Sealed Product Code:", "")

    if code is None:
        return

    code = code.strip()

    if code == "":
        return

    url = API_BASE + "/octgn/open?code=" + code

    response, status = webRead(url)

    if status != 200:
        whisper("Unable to open the sealed product.")
        return

    if response.startswith("ERROR"):
        show_error(response)
        return

    create_product(response)


def create_product(response):
    pack_group = me.piles[PACK_CONTENTS_GROUP]

    product_code = ""
    product_name = ""

    lines = response.splitlines()

    for line in lines:
        parts = line.split("\t")

        if len(parts) >= 2:
            if parts[0] == "CODE":
                product_code = parts[1]

            elif parts[0] == "DISPLAY":
                product_name = parts[1]

        if len(parts) >= 3:
            if parts[0] == "MODEL":
                model_id = parts[1]
                quantity = int(parts[2])

                pack_group.create(model_id, quantity)

    if product_name != "" and product_code != "":
        whisper("{} generated {}: {}".format(me, product_name, product_code))
    elif product_code != "":
        whisper("{} generated sealed product: {}".format(me, product_code))
    else:
        whisper("{} generated a sealed product.".format(me))


def show_error(response):
    error_message = "The sealed product server returned an error."

    lines = response.splitlines()

    for line in lines:
        parts = line.split("\t")

        if len(parts) >= 2:
            if parts[0] == "MESSAGE":
                error_message = parts[1]

    whisper(error_message)
