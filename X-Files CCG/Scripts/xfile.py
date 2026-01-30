CHECKLIST = {
    "Set": "02 - The Truth is Out There",
    "Affiliation": [
        "Alien",
        "Evolutionary",
        "Government",
        "Occult",
        "Primordial",
    ],
    "Method": [
        "Manipulation",
        "Possession",
        "Subterfuge",
        "Threats",
        "Violence",
    ],
    "Motive": [
        "Control",
        "Ideology",
        "Knowledge",
        "Security",
        "Survival",
    ],
    "Result": [
        "Abduction",
        "Death",
        "Insanity",
        "Manipulation of Evidence",
        "Physiological Imbalance",
    ],
}


ELIM_COLOR = "#FF2700"
AFFIL_COLOR = "#1976D2"
METH_COLOR = "#7B1FA2"
MOTI_COLOR = "#F57C00"
RESU_COLOR = "#689F38"


CATEGORY_COLORS = [
    ("Affiliation", AFFIL_COLOR),
    ("Method",     METH_COLOR),
    ("Motive",     MOTI_COLOR),
    ("Result",     RESU_COLOR),
]


def get_eliminated_list():
    raw = me.getGlobalVariable("eliminated_options")
    if not raw:
        return []
    return [i for i in raw.split(",") if i]


def get_button_list():
    return (
        CHECKLIST["Affiliation"]
        + CHECKLIST["Method"]
        + CHECKLIST["Motive"]
        + CHECKLIST["Result"]
    )


def browse_possibile_xfiles(*args):
    eliminated_options = get_eliminated_list()
    affiliation = [i for i in CHECKLIST["Affiliation"] if i not in eliminated_options]
    method = [i for i in CHECKLIST["Method"] if i not in eliminated_options]
    motive = [i for i in CHECKLIST["Motive"] if i not in eliminated_options]
    result = [i for i in CHECKLIST["Result"] if i not in eliminated_options]

    askCard(properties = {"Affiliation": affiliation, "Method": method, "Motive": motive, "Result": result, "XFile": "True"}, operator = "and", title = "Choose card")


def get_color_list(templist, removelist):
    color_list = []
    elim_list = get_eliminated_list()

    for cat_name, base_color in CATEGORY_COLORS:
        for item in CHECKLIST[cat_name]:
            color = base_color
            if item in elim_list or item in templist:
                if item not in removelist:
                    color = ELIM_COLOR
            color_list.append(color)

    return color_list


def check_list_display(*args):
    check_list_builder([], [])


def check_list_builder(templist, removelist):
    color_list = get_color_list(templist, removelist)
    my_list = get_eliminated_list()
    button_list = get_button_list()

    effective_elim = set(my_list + templist)
    effective_elim.difference_update(removelist)

    allowed_affiliation = [i for i in CHECKLIST["Affiliation"] if i not in effective_elim]
    allowed_method      = [i for i in CHECKLIST["Method"]      if i not in effective_elim]
    allowed_motive      = [i for i in CHECKLIST["Motive"]      if i not in effective_elim]
    allowed_result      = [i for i in CHECKLIST["Result"]      if i not in effective_elim]

    total_props = {
        "XFile": "True",
        "Affiliation": allowed_affiliation,
        "Method":      allowed_method,
        "Motive":      allowed_motive,
        "Result":      allowed_result,
    }
    total_guids = queryCard(properties=total_props, exact=True)
    total_remaining = len(total_guids)


    def get_category_for_option(option):
        for cat in ["Affiliation", "Method", "Motive", "Result"]:
            if option in CHECKLIST[cat]:
                return cat
        return None

    display_list = []
    for option in button_list:

        if option in effective_elim:
            count = 0
        else:
            category = get_category_for_option(option)

            props = {
                "XFile": "True",
                "Affiliation": allowed_affiliation,
                "Method":      allowed_method,
                "Motive":      allowed_motive,
                "Result":      allowed_result,
            }

            if category is not None:
                props[category] = option

            guids = queryCard(properties=props, exact=True)
            count = len(guids)

        display_list.append("{} ({})".format(option, count))

    choice = askChoice(
        "Total remaining X-Files: {}\n\n"
        "What options do you want to eliminate?\n"
        "(Numbers show remaining X-File cards)".format(total_remaining),
        display_list,
        color_list,
        customButtons=["Confirm", "Cancel"]
    )

    if choice == 0 or choice == -2:
        whisper("Checklist closed. No changes saved.")
        return
    elif choice > 0:
        selected = button_list[choice - 1]
        if selected not in my_list + templist:
            templist.append(selected)
        elif selected in my_list + templist:
            removelist.append(selected)
        check_list_builder(templist, removelist)
    elif choice == -1:
        my_list = [i for i in my_list + templist if i not in removelist]
        me.setGlobalVariable("eliminated_options", ','.join(my_list))
        whisper("Changes saved.")
