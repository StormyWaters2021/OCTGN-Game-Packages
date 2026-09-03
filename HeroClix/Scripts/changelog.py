changelog = {
    1000020: ("1.0.0.20", "3 September 2026", [
        "Thunderbolts and Hasbro Iconix added! Use the image downloader to get the new units!"
        ]),
    1000019: ("1.0.0.19", "2 September 2026", [
        "VENOM GALACTUS HAS ARRIVED! Use the image downloader plugin to fetch the new images for this test build.",
        "Venom Galactus brings the second HUGE 3x6 model, with four independent dials!",
        "As with the physical unit, you need to select which dial is active, so right-click to make that selection!",
        "You can also control Venom Galactus' Cosmic Hunger independently."
        "Please report any issues to info@tcgbuilder.net!"
        ]),
    1000018: ("1.0.0.18", "31 August 2026", [
        "GALACTUS HAS ARRIVED! Use the image downloader plugin to fetch the new images for this test build.",
        "Adding Galactus, a Herald, or the Elemental Converter to your team will create a massive, multi-click model.",
        "The game treats the A and B clicks as one long row of clicks.",
        "To use the others, right click on Galactus and you will see options for the Converter and Herald."
        "Please report any issues to info@tcgbuilder.net!"
        ]),
    1000017: ("1.0.0.17", "26 August 2026", [
        "Added a Test Menu to the right-click menu. Here you can see things I am testing, so please provide feedback!",
        ]),
    1000016: ("1.0.0.16", "24 August 2026", [
        "Added a handful of actual map images - right click a map to swap if available.",
        ]),
    1000015: ("1.0.0.15", "16 August 2026", [
        "Fixed minor display issues with cards rendering in the wrong size.",
        "Corrected some issues with some terrain markers not being built correctly",
        ]),
    1000014: ("1.0.0.14", "16 August 2026", [
        "Fixed graphical and positional issues with 1x2 models. They now rotate around a single end and properly report that end as being the position.",
        "Fixed model generation code for inverted players, so the models should generate in the correct position for both sides of the table.",
        ]),
    1000013: ("1.0.0.13", "16 August 2026", [
        "Added Line of Sight tool - Experimental.",
        "Shift-click and drag from one model to another to drop a line through the center of both. Zooming in first can prevent errors.",
        "Double-click the line once you are done checking Line of Sight - if you don't, the line 'card' can interfere with gameplay.",
        ]),
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