changelog = {
    1000011: ("1.0.0.11", "14 August 2026", [
        "Bug fix in changelog.",
        "Added new feature to generate characters. Users can now generate any character in the database, after filtering by either Team Ability or Keyword.",
        "No new images were added with this update.",
        ]),

    1000010: ("1.0.0.10", "13 August 2026", [
        "Added another ~20 sets. Use Image Downloader plugin again to retreive missing images.",
        ]),
    1000007: ("1.0.0.7", "13 August 2026", [
        "Added most of the missing terrain tiles. Use Image Downloader plugin again to retreive missing images.",
        ]),
    1000006: ("1.0.0.6", "13 August 2026", [
        "Replaced main playmat image, added several new options. Right-click the table to swap.",
        ]),
    1000000: ("1.0.0.0", "9 August 2026", [
        "Initial test build",
        ]),
        }

extra_memo = "\n\n## Download images using the OCTGN Deck Builder plugin \n\n## Send feedback to info@tcgbuilder.net"

def initializeGame():
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

    # Migration: 1.0.0.10 was accidentally stored as 10000010
    if lastVersion == 10000010:
        lastVersion = 1000010
        setSetting("lastVersion", convertToString(lastVersion))

    for log in sorted(changelog):  ## Sort the dictionary numerically
        if lastVersion < log:  ## Trigger a changelog for each update they haven't seen yet.
            stringVersion, date, text = changelog[log]
            updates = '\n- '.join(text)
            updates += extra_memo
            choice = askChoice("What's new in {} ({}):\n\n- {}".format(stringVersion, date, updates), button_list)
            if choice == 1:
                setSetting("lastVersion", convertToString(currentVersion))  ## Store's the current version to a setting