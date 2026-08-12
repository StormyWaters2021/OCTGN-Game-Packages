import re


def importHCUnits(group, x=0, y=0):
    url = askString("Paste HCUnits team URL:", "")
    if not url:
        return

    html, status = webRead(url, 10000)

    if status != 200:
        whisper("Could not download HCUnits team. HTTP {}".format(status))
        return

    match = re.search(
        r'<script[^>]+id=["\']teamObject["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S
    )

    if not match:
        whisper("Downloaded team page, but could not find teamObject.")
        return

    entries = re.findall(
        r'"section"\s*:\s*"([^"]+)".*?'
        r'"unit"\s*:\s*\{.*?'
        r'"id"\s*:\s*"([^"]+)"',
        match.group(1),
        re.S
    )

    if not entries:
        whisper("No HCUnits team entries were found.")
        return

    imported = 0
    missing = []

    for section, unitId in entries:
        if section == "scratch_space":
            continue

        cards = queryCard({
            "Unit ID": unitId
        }, True)

        if not cards:
            missing.append(unitId)
            continue

        if section == "sideline":
            destination = me.piles["Sideline"]
        elif section == "maps":
            destination = me.piles["Maps"]
        else:
            destination = me.piles["Team"]

        destination.create(cards[0], 1)
        imported += 1

    notify("{} imported {} units from HCUnits.".format(me, imported))

    if missing:
        whisper("Not found: " + ", ".join(missing))
