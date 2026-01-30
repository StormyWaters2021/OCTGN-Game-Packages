changelog = {
    1020200: ("1.2.2.0", "30 January 2026", [ 
        "Improved roll calculations",
        "Updated terrain rolling algorithms",
        "Improved zone-detection code",
        ]),
    1020105: ("1.2.1.5", "16 April 2024", [ 
        "Added a changelog dialog that displays when a game is started.",
        "Fixed a bug in the roll calculator.",
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