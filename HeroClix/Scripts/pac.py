PAC_GUID = "7db159f2-1eb2-425f-aaac-5492e36d755b"
PAC_POSITIONS = (-1500, -210)

def _is_pac(card, x=0, y=0):
    return card[0].size == "PAC"


def pac_panels():
    mute()
    x, y = PAC_POSITIONS
    offset = 0
    for n in range(4):
        panel = table.create(PAC_GUID, x + offset, y)
        panel.alternate = panel.alternates[n+1]
        panel.anchor = True
        offset += 127
    y += 210
    offset = 0
    for n in range(4):
        panel = table.create(PAC_GUID, x + offset, y)
        panel.alternate = panel.alternates[n+5]
        panel.anchor = True
        offset += 127

PAC_COLORS = [
    "#EB3C3B",  # Red
    "#FAA754",  # Orange
    "#F4ED64",  # Yellow
    "#B9D648",  # Light Green
    "#4BB14A",  # Green
    "#77D2F6",  # Light Blue
    "#1591BE",  # Blue
    "#7E298A",  # Purple
    "#E5C2DC",  # Pink
    "#A0735E",  # Brown
    "#2B2E31",  # Black
    "#909598",  # Gray
]


PAC_POWERS = {
    "Speed": [
        (
            "FLURRY",
            "CLOSE: Make up to two close attacks."
        ),
        (
            "LEAP/CLIMB",
            "When this character moves, they can change elevation without "
            "stopping movement, can move through outdoor blocking terrain, "
            "and can move through squares occupied by or adjacent to opposing "
            "characters without stopping. They still must break away."
        ),
        (
            "PHASING/TELEPORT",
            "MOVE: For this action, this character automatically breaks away, "
            "can change elevation without stopping movement, can move through "
            "blocking terrain but can't end movement in blocking terrain, and "
            "can move through squares adjacent to or occupied by opposing "
            "characters without stopping. Move."
        ),
        (
            "EARTHBOUND/NEUTRALIZED",
            "This character can't use Improved Abilities."
        ),
        (
            "CHARGE",
            "POWER: Halve speed. Move then CLOSE as FREE -or- make a close attack."
        ),
        (
            "MIND CONTROL",
            "CLOSE/RANGE: Minimum range 4. Make a close/range attack. Instead "
            "of normal damage, each hit character halves speed and becomes "
            "friendly to your force and, one at a time, may in either order: "
            "Move and/or make an attack, then it reverts forces."
        ),
        (
            "PLASTICITY",
            "This character breaks away on any result except a 1. Adjacent "
            "opposing characters that can't use Phasing/Teleport, Plasticity, "
            "Leap/Climb, or Hypersonic Speed only break away on a 6."
        ),
        (
            "FORCE BLAST",
            "KNOCKBACK. // POWER: Minimum range 4. Knock back an opposing "
            "character within range and line of fire 3 squares away from "
            "this character."
        ),
        (
            "SIDESTEP",
            "FREE: Move up to 2 squares."
        ),
        (
            "HYPERSONIC SPEED",
            "POWER: Halve range. For this action, this character halves range, "
            "can't carry, and can move through squares occupied by or adjacent "
            "to opposing characters without stopping. They still must break "
            "away. Move, then make an attack, then move up to your speed value "
            "minus the number of squares just moved."
        ),
        (
            "STEALTH",
            "When it's not your turn, hindered lines of fire drawn to this "
            "character by non-adjacent characters are blocked."
        ),
        (
            "RUNNING SHOT",
            "POWER: Halve speed. Move, then RANGE as FREE -or- make a range attack."
        ),
    ],

    "Attack": [
        (
            "BLADES/CLAWS/FANGS",
            "When this character makes a close attack against a single target "
            "and hits, you may roll a d6. If you do, deal damage equal to the "
            "result instead of normal damage. Minimum result is this "
            "character's printed damage value -1."
        ),
        (
            "ENERGY EXPLOSION",
            "RANGE: Make a range attack and all other characters adjacent to "
            "an original target also become targets. Hit characters are dealt "
            "2 damage instead of normal damage."
        ),
        (
            "PULSE WAVE",
            "RANGE: Range 4. Other characters within range can't use powers or "
            "abilities for this action. Make a range attack targeting all "
            "other characters within range and line of fire, including at "
            "least one opposing character, using printed defense values for "
            "each targeted character. Each hit character is dealt 1 damage "
            "instead of normal damage."
        ),
        (
            "QUAKE",
            "CLOSE: KNOCKBACK. Destroy all terrain markers and printed pieces "
            "of blocking terrain within 1 square, then make a close attack "
            "targeting all adjacent opposing characters. Each hit character "
            "is dealt 2 damage instead of normal damage."
        ),
        (
            "SUPER STRENGTH",
            "KNOCKBACK during close attacks. This character can pick up, hold "
            "and put down non-object terrain markers, excluding Smoke, Debris "
            "or Water markers."
        ),
        (
            "INCAPACITATE",
            "When this character makes an attack, instead of normal damage, "
            "you may give each hit character an action token."
        ),
        (
            "PENETRATING/PSYCHIC BLAST",
            "Damage dealt by this character's range attacks is penetrating damage."
        ),
        (
            "SMOKE CLOUD",
            "POWER: Minimum range 4. Generate up to 6 Smoke terrain markers, "
            "one at a time, in distinct squares within range. Other than the "
            "first, each marker must be adjacent to at least one other, and at "
            "least one must be within line of fire. Opposing characters "
            "occupying one or more of these markers modify attack -1. At the "
            "beginning of your next turn, even if this is lost, remove them."
        ),
        (
            "PRECISION STRIKE",
            "Damage from this character's attacks can't be reduced below 1. // "
            "When this character attacks, opposing characters decrease their "
            "Super Senses result by -1."
        ),
        (
            "POISON",
            "FREE: If this character hasn't moved or been placed this turn, "
            "deal 1 damage to all adjacent opposing characters."
        ),
        (
            "STEAL ENERGY",
            "When this character hits and damages one or more characters with "
            "a close attack, after resolutions heal this character 1 click."
        ),
        (
            "TELEKINESIS",
            "POWER: Minimum range 4. Choose a terrain marker or single-base "
            "friendly character within range and line of fire. Place it into "
            "a square within range and line of fire that is also within 4 "
            "squares and line of fire from that terrain marker/character. // "
            "This character can make RANGE Terrain Actions as if it was "
            "holding terrain markers within range and line of fire."
        ),
    ],

    "Defense": [
        (
            "SUPER SENSES",
            "When this character would be hit, you may roll a d6. 5-6: Evade."
        ),
        (
            "TOUGHNESS",
            "Reduce damage taken by 1."
        ),
        (
            "DEFEND",
            "Adjacent friendly characters may replace their defense value "
            "with this character's printed defense value."
        ),
        (
            "COMBAT REFLEXES",
            "Modify defense +2 against close attacks."
        ),
        (
            "ENERGY SHIELD/DEFLECTION",
            "Modify defense +2 against range attacks."
        ),
        (
            "BARRIER",
            "POWER: Minimum range 4. Generate up to 4 blocking terrain markers, "
            "one at a time, in distinct squares within range. Other than the "
            "first, each marker must be adjacent to at least one other, and at "
            "least one must be within line of fire. At the beginning of your "
            "next turn, even if this is lost, remove them."
        ),
        (
            "MASTERMIND",
            "When this character would be hit by an opponent's attack that "
            "deals damage, you may choose an adjacent friendly character that "
            "wouldn't be hit by this attack and that is less points or shares "
            "a keyword. That friendly character instead becomes a hit target "
            "of the attack, even if it's already a target or would be an "
            "illegal target."
        ),
        (
            "WILLPOWER",
            "At the beginning of your turn, you may roll a d6. 5-6: Remove an "
            "action token from this character."
        ),
        (
            "INVINCIBLE",
            "Reduce damage taken by 2. // Can reduce penetrating damage."
        ),
        (
            "IMPERVIOUS",
            "Reduce damage taken by 2. // When this character is dealt damage "
            "from an attack, you may roll a d6. 5-6: Damage taken is reduced to 0."
        ),
        (
            "REGENERATION",
            "POWER: Roll a d6. Heal a number of clicks equal to half the "
            "result, rounded up."
        ),
        (
            "INVULNERABILITY",
            "Reduce damage taken by 2."
        ),
    ],

    "Damage": [
        (
            "RANGED COMBAT EXPERT",
            "This character modifies attack and damage +1 while making a "
            "range attack or when given a RANGE Destroy action."
        ),
        (
            "BATTLE FURY",
            "This character can't make range attacks or be given RANGE actions "
            "except for RANGE Terrain Actions and its granted range attack, "
            "can't be carried, can't be given action tokens by opposing "
            "effects, and has SAFEGUARD: Mind Control. When this character "
            "attacks, opposing characters can't use Shape Change."
        ),
        (
            "SUPPORT",
            "POWER: Choose an adjacent friendly character and roll a d6. Heal "
            "that character a number of clicks equal to half the result, "
            "rounded up."
        ),
        (
            "EXPLOIT WEAKNESS",
            "Damage dealt by this character's close attacks is penetrating damage."
        ),
        (
            "ENHANCEMENT",
            "Adjacent friendly characters modify damage +1 while making a "
            "range attack or when given a RANGE Destroy action."
        ),
        (
            "PROBABILITY CONTROL",
            "Once per turn, you may reroll a target character's attack roll "
            "or break away roll. A targeted character must be within range "
            "and line of fire, minimum range 4."
        ),
        (
            "SHAPE CHANGE",
            "When this character would be targeted by an attack, you may roll "
            "a d6. 5-6: This character can't be targeted by the attacker this "
            "turn and the attacker may choose a different target instead."
        ),
        (
            "CLOSE COMBAT EXPERT",
            "This character modifies attack and damage +1 while making a "
            "close attack or when given a CLOSE Destroy action."
        ),
        (
            "EMPOWER",
            "Adjacent friendly characters modify damage +1 while making close "
            "attacks or when given a CLOSE Destroy action."
        ),
        (
            "PERPLEX",
            "FREE: Minimum range 4. Choose a target character within range and "
            "line of fire. Modify one of that character's combat values other "
            "than damage +1 or -1 until your next turn."
        ),
        (
            "OUTWIT",
            "FREE: Minimum range 4. Choose a target opposing character within "
            "range and line of fire and then choose one: any standard power "
            "-or- a special power printed on the target's card. The target "
            "can't use the chosen power until your next turn."
        ),
        (
            "LEADERSHIP",
            "For all friendly characters that can use Leadership, Action Total "
            "+1. // At the beginning of your turn, you may roll a d6. 5-6: "
            "Remove an action token from an adjacent friendly character that's "
            "less points or shares a keyword."
        ),
    ],
}


PAC_PANELS = [
    "Speed",
    "Attack",
    "Defense",
    "Damage",
]


def pac_speed(group, x=0, y=0):
    mute()
    _pac_window("Speed")


def _pac_window(start_panel):
    panel = start_panel

    while True:
        powers = PAC_POWERS[panel]

        buttons = []
        for power in powers:
            buttons.append(power[0])

        choice = askChoice(
            "PAC - " + panel,
            buttons,
            PAC_COLORS,
            customButtons=PAC_PANELS
        )

        # Window closed.
        if choice == 0:
            return

        # Panel buttons return -1, -2, -3, -4.
        if choice < 0:
            panel = PAC_PANELS[(-choice) - 1]
            continue

        power = powers[choice - 1]
        name = power[0]
        description = power[1]

        back = askChoice(
            name + "\n\n" + description,
            ["Back"],
            ["#808285"]
        )

        # Closing the description closes the PAC browser.
        if back == 0:
            return