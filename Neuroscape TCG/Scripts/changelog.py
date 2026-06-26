changelog = {
    1000001: ("1.0.0.1", "26 June 2026", [ 
        "Added functionality for Drone tokens."
        ]),
    1000000: ("1.0.0.0", "25 June 2026", [ 
        "Initial release",
        "Welcome to Neuroscape TCG!",
        "Before you start playing, you will need to download card images. "
        "Open the OCTGN Deck Editor, click on the Plugins menu at the top, and select Download Images. "
        "Once that is done, jump in and start playing! Preconstructed decks are available in the Game menu at the top, under 'Load Prebuilt Deck'. "
        "You can build and download your own decks from TCGBuilder.net or using OCTGN's built-in deck editor. "
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