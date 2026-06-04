import json

# Role taxonomy based on what a Pokemon does for the team:
# 1. Deal damage (physical or special)
# 2. Set up weather (enables weather strategy)
# 3. Abuse weather (benefits from active weather)
# 4. Control speed (Tailwind, Trick Room, Icy Wind)
# 5. Protect teammates (redirection, Intimidate, Wide Guard)
# 6. Disrupt opponents (status, Taunt, trapping)

LABEL_MAPPING = {
    # --- Deal damage ---
    "All-Out Attacker":         {"physical_attacker"},
    "Attacker":                 {"physical_attacker"},
    "Bulky Attacker":           {"physical_attacker"},
    "Bulky Special Attacker":   {"special_attacker"},
    "Fast Attacker":            {"special_attacker"},            # e.g. Manectric, special despite name
    "Fast Mixed Attacker":      {"physical_attacker", "special_attacker"},
    "Gale Wings Attacker":      {"physical_attacker"},           # Talonflame, priority Flying
    "Life Orb Attacker":        {"special_attacker"},            # e.g. Landorus, Sheer Force special
    "Mega Mixed Attacker":      {"physical_attacker", "special_attacker"},
    "Mega Physical Attacker":   {"physical_attacker"},
    "Megabus":                  {"physical_attacker"},           # Azumarill, Huge Power wallbreaker
    "Mixed Attacker":           {"physical_attacker", "special_attacker"},
    "Physical Attacker":        {"physical_attacker"},
    "Special Attacker":         {"special_attacker"},
    "Special Tank":             {"special_attacker"},            # hits hard, takes special hits
    "Recover + 3 Attacks":      {"special_attacker"},            # self-sufficient attacker

    # --- Setup sweepers (deal damage via setup) ---
    "Calm Mind":                {"special_attacker"},            # SpA/SpD boost
    "Dragon Dance":             {"physical_attacker"},           # Atk/Spe boost
    "Offensive Quiver Dance":   {"special_attacker"},            # SpA/SpD/Spe boost
    "Power-Up Punch":           {"physical_attacker"},           # Atk boost on hit
    "SubCM":                    {"special_attacker"},            # Substitute + Calm Mind
    "Swords Dance":             {"physical_attacker"},           # Atk boost
    "Tail Glow":                {"special_attacker"},            # extreme SpA boost

    # --- Set up weather ---
    "Rain Setter":              {"weather_setter"},
    # "Sun Attacker": {"special_attacker", "weather_setter"},  # Charizard-Mega-Y; Sun teams not viable in Gen 6 DOU

    # --- Abuse weather ---
    "Rain Attacker":            {"special_attacker", "weather_abuser"},
    "Sand Rush Attacker":       {"physical_attacker", "weather_abuser"},
    "Swift Swim Attacker":      {"physical_attacker", "weather_abuser"},
    "Non-Mega Support":         {"support", "weather_abuser"},   # Swampert, rain utility

    # --- Control speed ---
    "Bulky Tailwind":           {"speed_control"},
    "Bulky Thunder Wave":       {"speed_control", "support"},    # paralyzes faster threats
    "Fast Support":             {"speed_control", "support"},    # Raichu, Tailwind/Thunder Wave
    "Hazard Setter":            {"support"},                     # disrupts opponent tempo
    "Offensive Trick Room":     {"trick_room_setter", "special_attacker"},  # Cresselia/Diancie/Hoopa all special
    "Trick Room":               {"trick_room_setter"},
    "Bulky Trick Room Setter":  {"trick_room_setter"},
    "Trick Room Trapper":       {"trick_room_setter", "support"}, # Gothitelle, traps + sets TR

    # --- Protect teammates ---
    "Follow Me":                {"redirection"},
    "Follow Me Support":        {"redirection", "support"},
    "Friend Guard Support":     {"redirection", "support"},      # reduces partner damage
    "Pivot":                    {"redirection", "support"},      # Intimidate + Fake Out
    "Rage Powder":              {"redirection"},
    "Wide Guard Tank":          {"redirection", "special_attacker"}, # Aegislash, blocks spread moves

    # --- Disrupt opponents ---
    "GeoPass":                  {"support"},                     # Smeargle Baton Pass gimmick
    "Prankster":                {"support", "speed_control"},    # priority Tailwind/Thunder Wave
    "Substitute":               {"support"},                     # stalling/disruption
    "Substitute Leftovers":     {"support"},                     # passive stalling
    "Transform Support":        {"support"},                     # Mew, unpredictable utility

    # --- Defensive / tank ---
    "Assault Vest":             {"physical_attacker"},           # bulky attacker, no support moves
    "Bulky Support":            {"support"},
    "Defensive":                {"support"},
    "Mega Tank":                {"special_attacker", "support"}, # Venusaur, tanks + attacks
    "Offensive":                {"special_attacker"},            # e.g. Milotic, Shaymin-Sky are special
    "Offensive Support":        {"special_attacker", "support"}, # deals damage but primarily supports
    "Safety Goggles":           {"support"},                     # weather immune utility
    "Specially Defensive":      {"support"},                     # tanks special hits
    "Support":                  {"support"},

    # --- Item-defined roles ---
    "Choice Band":              {"physical_attacker"},
    "Choice Scarf":             {"physical_attacker"},           # speed control via item; corrected per-pokemon in overrides
    "Choice Specs":             {"special_attacker"},
}

with open('smogon_sets_gen6doublesou.json', 'r') as f:
    smogon_sets = json.load(f)

with open('gen6dou.json', 'r') as f:
    pokemon_data = json.load(f)

roles = {}

# assign roles from smogon set names
for pokemon, sets in smogon_sets.items():
    for set_name in sets.keys():
        mapped = LABEL_MAPPING.get(set_name, set())
        for role in mapped:
            roles.setdefault(role, set()).add(pokemon)

# assign weather roles from set ability
# set names don't always capture weather setting (e.g. Tyranitar's "Dragon Dance")
# falls back to available abilities if set doesn't specify one (e.g. Tyranitar only has Sand Stream)
WEATHER_ABILITIES = {
    'Drizzle':      'weather_setter',
    'Drought':      'weather_setter',
    'Sand Stream':  'weather_setter',
    'Snow Warning': 'weather_setter',
    'Swift Swim':   'weather_abuser',
    'Sand Rush':    'weather_abuser',
    'Sand Force':   'weather_abuser',
    'Ice Body':     'weather_abuser',
}

for pokemon, sets in smogon_sets.items():
    if pokemon not in pokemon_data:
        continue
    for set_name, set_data in sets.items():
        set_ability = set_data.get('ability')

        if set_ability is None:
            abilities_to_check = pokemon_data[pokemon]['abilities']
        elif isinstance(set_ability, list):
            abilities_to_check = set_ability
        else:
            abilities_to_check = [set_ability]

        for ability in abilities_to_check:
            if ability in WEATHER_ABILITIES:
                role = WEATHER_ABILITIES[ability]
                roles.setdefault(role, set()).add(pokemon)

# manual overrides — applied last, highest priority
# handles edge cases where set name or stat-based inference is insufficient
ROLE_OVERRIDES = {
    # Huge Power doubles effective Atk, making it a strong physical attacker
    # despite base Atk of 50 (lower than SpA of 60)
    "Azumarill":    {"physical_attacker"},

    # Storm Drain gives Water immunity in Rain but doesn't boost offense
    # Gastrodon is a Rain counter, not a Rain abuser
    "Gastrodon":    {"special_attacker"},

    # Dragon Dance set is physical (Rock Slide/Crunch) despite having no ability field
    # Tyranitarite ability is Sand Stream which is correctly captured by weather logic
    "Charizard":    {"physical_attacker"},    # Sun teams not viable; do not count as weather setter

    # Rotom-W runs Choice Scarf as a special attacker (SpA=105 > Atk=65)
    # Choice Scarf label defaults to physical_attacker in LABEL_MAPPING
    "Rotom-Wash":   {"special_attacker"},

    # Thundurus-T runs Choice Scarf/Specs as special attacker (SpA=145 > Atk=105)
    "Thundurus-Therian": {"special_attacker"},

    # Venusaur and Whimsicott have Chlorophyll but Sun teams are not viable in Gen 6 DOU
    # removing them from weather_abuser to avoid generating invalid Sun teams
    "Venusaur":     {"special_attacker", "support"},
    "Whimsicott":   {"support", "speed_control"},
}

# apply overrides — removes pokemon from all roles first, then adds correct ones
for pokemon, correct_roles in ROLE_OVERRIDES.items():
    for role in list(roles.keys()):
        roles[role].discard(pokemon)
    for role in correct_roles:
        roles.setdefault(role, set()).add(pokemon)

# convert sets to list for JSON serialization
roles = {role: list(pokemon_set) for role, pokemon_set in roles.items()}

with open('pokemon_roles.json', 'w') as f:
    json.dump(roles, f, indent=2)