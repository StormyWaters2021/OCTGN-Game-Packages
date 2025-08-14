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

BUTTONLIST = [        
    "Alien",
    "Evolutionary",
    "Government",
    "Occult",
    "Primordial",
    "Manipulation",
    "Possession",
    "Subterfuge",
    "Threats",
    "Violence",
    "Control",
    "Ideology",
    "Knowledge",
    "Security",
    "Survival",
    "Abduction",
    "Death",
    "Insanity",
    "Manipulation of Evidence",
    "Physiological Imbalance",
    ]

ELIM_COLOR = "#FF2700"
AFFIL_COLOR = "#1976D2"
METH_COLOR = "#7B1FA2"
MOTI_COLOR = "#F57C00"
RESU_COLOR = "#689F38"




def browse_possibile_xfiles(*args):
    eliminated_options = me.getGlobalVariable("eliminated_options").split(",")
    affiliation = [i for i in CHECKLIST["Affiliation"] if i not in eliminated_options]
    method = [i for i in CHECKLIST["Method"] if i not in eliminated_options]
    motive = [i for i in CHECKLIST["Motive"] if i not in eliminated_options]
    result = [i for i in CHECKLIST["Result"] if i not in eliminated_options]

    askCard(properties = {"Affiliation": affiliation, "Method": method, "Motive": motive, "Result": result, "XFile": "True"}, operator = "and", title = "Choose card")


def get_color_list(templist, removelist):
    color_list = []
    elim_list = me.getGlobalVariable("eliminated_options").split(",")
    color = ""
    
    for i in CHECKLIST["Affiliation"]:
        color = AFFIL_COLOR
        if i in elim_list or i in templist:
            if i not in removelist:
                color = ELIM_COLOR
        color_list.append(color)
        
    for i in CHECKLIST["Method"]:
        color = METH_COLOR
        if i in elim_list or i in templist:
            if i not in removelist:
                color = ELIM_COLOR
        color_list.append(color) 
        
    for i in CHECKLIST["Motive"]:
        color = MOTI_COLOR
        if i in elim_list or i in templist:
            if i not in removelist:
                color = ELIM_COLOR
        color_list.append(color) 
    
    for i in CHECKLIST["Result"]:
            color = RESU_COLOR
            if i in elim_list or i in templist:
                if i not in removelist:
                    color = ELIM_COLOR
            color_list.append(color)     

    return color_list
    

def check_list_display(*args):
    check_list_builder([], [])


def check_list_builder(templist, removelist):
    color_list = get_color_list(templist, removelist)
    my_list = me.getGlobalVariable("eliminated_options").split(",")
    
    choice = askChoice("What options do you want to eliminate?", BUTTONLIST, color_list, customButtons = ["Confirm", "Cancel"])
    
    if choice == 0 or choice == -2:
        whisper("Checklist closed. No changes saved.")
        return
    elif choice > 0:
        if BUTTONLIST[choice-1] not in my_list + templist:
            templist.append(BUTTONLIST[choice-1])
        elif BUTTONLIST[choice-1] in my_list + templist:
            removelist.append(BUTTONLIST[choice-1])
        check_list_builder(templist, removelist)
    elif choice == -1:
        my_list = [i for i in my_list + templist if i not in removelist]
        me.setGlobalVariable("eliminated_options", ','.join(my_list))
        whisper("Changes saved.")