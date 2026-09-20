import re


def _get_team_entries(team_data):
    starts = []

    for match in re.finditer(
        r'\{"id"\s*:\s*\d+\s*,\s*"force"\s*:\s*\d+\s*,\s*"section"\s*:',
        team_data
    ):
        starts.append(match.start())

    entries = []

    for index in range(len(starts)):
        start = starts[index]

        if index + 1 < len(starts):
            end = starts[index + 1]
        else:
            end = len(team_data)

        entries.append(team_data[start:end])

    return entries


def _get_starting_click(entry):
    point_values_match = re.search(
        r'"point_values"\s*:\s*\[(.*?)\]\s*,\s*"rarity"',
        entry,
        re.S
    )

    if not point_values_match:
        return ""

    selected_values = re.findall(
        r'"point_value"\s*:\s*(\d+)',
        entry
    )

    if not selected_values:
        return ""

    selected_points = selected_values[-1]

    point_options = re.findall(
        r'"point_value"\s*:\s*(\d+).*?'
        r'"click_number"\s*:\s*(\d+)',
        point_values_match.group(1),
        re.S
    )

    for point_value, click_number in point_options:
        if point_value == selected_points:
            return click_number

    return ""


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

    entries = _get_team_entries(match.group(1))

    if not entries:
        whisper("No HCUnits team entries were found.")
        return

    imported = 0
    missing = []

    for entry in entries:
        section_match = re.search(
            r'"section"\s*:\s*"([^"]+)"',
            entry
        )

        unit_match = re.search(
            r'"unit"\s*:\s*\{\s*'
            r'"id"\s*:\s*"([^"]+)"',
            entry,
            re.S
        )

        if not section_match or not unit_match:
            continue

        section = section_match.group(1)
        unitId = unit_match.group(1)

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

        card = destination.create(cards[0], 1)

        starting_click = _get_starting_click(entry)

        if starting_click:
            card.properties["Starting Line"] = starting_click

        imported += 1

    notify("{} imported {} units from HCUnits.".format(me, imported))

    if missing:
        whisper("Not found: " + ", ".join(missing))
