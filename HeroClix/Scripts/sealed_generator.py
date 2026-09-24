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
    set_name = clean_set_name(set_names[choice - 1])

    choose_product(set_id, set_name)


def choose_product(set_id, set_name):
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

    if product == "case":
        choice = confirm("Are you sure you want to open a case? This may take a few moments to process.")
        if not choice:
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

    create_product(response, set_name)


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

    set_name = get_set_name_from_code(code)
    create_product(response, set_name)


def clean_set_name(set_name):
    prefixes = [
        "Marvel HeroClix: ",
        "DC HeroClix: ",
        "HeroClix: ",
    ]

    for prefix in prefixes:
        if set_name.startswith(prefix):
            return set_name[len(prefix):]

    return set_name


def get_set_name_from_code(code):
    code_parts = code.split("-")

    if len(code_parts) < 2:
        return ""

    set_code = code_parts[1].upper()
    url = API_BASE + "/octgn/sets?gameid=" + GAME_GUID
    response, status = webRead(url)

    if status != 200 or response.startswith("ERROR"):
        return ""

    lines = response.splitlines()

    for line in lines:
        parts = line.split("\t")

        if len(parts) >= 4:
            if parts[0] == "SET" and parts[2].upper() == set_code:
                return clean_set_name(parts[3])

    return ""


def create_product(response, set_name=""):
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

    display_name = product_name

    if set_name != "" and product_name != "":
        display_name = set_name + " " + product_name

    if display_name != "":
        notify("{} has opened a {}.".format(me, display_name))
    else:
        notify("{} has opened a sealed product.".format(me))

    if product_code != "":
        if display_name != "":
            whisper("{} code: {}".format(display_name, product_code))
        else:
            whisper("Sealed product code: {}".format(product_code))


def show_error(response):
    error_message = "The sealed product server returned an error."

    lines = response.splitlines()

    for line in lines:
        parts = line.split("\t")

        if len(parts) >= 2:
            if parts[0] == "MESSAGE":
                error_message = parts[1]

    whisper(error_message)
