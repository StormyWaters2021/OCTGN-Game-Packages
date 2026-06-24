changelog = {
    1000401: ("1.0.4.1", "23 June 2026", [ 
        "Overhaul of card names to eliminate duplicates.",
        "Fix some minor typos."
        ]),    
    1000400: ("1.0.4.0", "21 June 2026", [ 
        "Added a changelog dialog that displays when a game is started.",
        "Added NZ 10 - Mortal Combat set.",
        "Typo corrections.",
        ]),
        }


def show_changelog():
    mute()
    #### LOAD UPDATES
    v1, v2, v3, v4 = gameVersion.split('.')  ## split apart the game's version number
    v1 = int(v1) * 1000000
    v2 = int(v2) * 10000
    v3 = int(v3) * 100
    v4 = int(v4)
    button_list = ["Hide until next update", "Show again next launch"]
    currentVersion = v1 + v2 + v3 + v4  ## An integer interpretation of the version number, for comparisons later
    lastVersion = getSetting("lastVersion", convertToString(currentVersion - 1))  ## -1 is for players experiencing the system for the first time
    lastVersion = int(lastVersion)
    for log in sorted(changelog):  ## Sort the dictionary numerically
        if lastVersion < log:  ## Trigger a changelog for each update they haven't seen yet.
            stringVersion, date, text = changelog[log]
            updates = '\n\n- '.join(text)
            choice = askChoice("What's new in {} ({}):\n\n-{}".format(stringVersion, date, updates), button_list)
            if choice == 1:
                setSetting("lastVersion", convertToString(currentVersion))  ## Store's the current version to a setting