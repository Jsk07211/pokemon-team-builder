# Based on smogon_teams. Sun teams were not run. Refer to notes for reasoning.

TEAM_ARCHETYPES = {
    "rain": {
        # Politoed sets permanent rain, Swift Swim abusers sweep
        # Based on: Sample Rain (Viper)
        "required": [
            "weather_setter",    # Politoed
            "weather_abuser",    # Kingdra, Ludicolo
            "weather_abuser",    # Swampert, Kingdra
        ],
        "optional": [
            "redirection",       # redirect moves away from sweepers
            "speed_control",     # backup speed control
            "special_attacker",  # non-weather attacker for coverage
        ]
    },

    "sand_trick_room": {
        # Tyranitar sets sand, Trick Room lets slow hard hitters move first
        # Based on: XY Mence Ferro Sand (DLTME 3-peat)
        "required": [
            "weather_setter",    # Tyranitar
            "trick_room_setter", # Cresselia, Porygon2
            "physical_attacker", # slow hard hitter
        ],
        "optional": [
            "weather_abuser",    # Excadrill (Sand Rush)
            "special_attacker",  # mixed offense
            "support",           # utility
        ]
    },

    "tailwind_offense": {
        # Prankster Tailwind from Whimsicott, fast sweepers behind it
        # Based on: Whimsicott Offense (Memoric)
        "required": [
            "speed_control",     # Whimsicott, Zapdos, Suicune
            "physical_attacker", # fast physical sweeper
            "special_attacker",  # fast special sweeper
        ],
        "optional": [
            "support",           # utility
            "physical_attacker", # second attacker
            "redirection",       # protect sweepers
        ]
    },

    "hyper_offense": {
        # No weather, no trick room — pure raw power and speed
        # Based on: Hyper Off DeoSharp + M Kangas (JRL & Tenzai)
        "required": [
            "physical_attacker", # primary sweeper
            "physical_attacker", # secondary sweeper
            "special_attacker",  # mixed offense
        ],
        "optional": [
            "physical_attacker", # third attacker
            "support",           # minimal utility
            "speed_control",     # priority or speed control
        ]
    },

    "bulky_offense": {
        # Balanced — hits hard but has defensive backbone
        # Based on: tvalks (zee), Sample MGar + Conk (Memoric)
        "required": [
            "physical_attacker", # primary attacker
            "special_attacker",  # special coverage
            "support",           # utility/disruption
        ],
        "optional": [
            "redirection",       # protect attackers
            "speed_control",     # speed control
            "support",           # second support
        ]
    },

    "redirection_offense": {
        # Double redirection — Follow Me + Rage Powder protect a setup sweeper
        # Based on: Sample MGarde + 2 Redirects (Memoric)
        "required": [
            "redirection",       # Follow Me or Rage Powder
            "redirection",       # second redirector
            "special_attacker",  # sweeper behind redirection
        ],
        "optional": [
            "physical_attacker", # physical coverage
            "speed_control",     # Tailwind support
            "support",           # utility
        ]
    },

    "trick_room": {
        # Set Trick Room, bring slow hard hitters
        # Based on: qsns team (Porygon2 + Sylveon)
        "required": [
            "trick_room_setter", # Porygon2, Cresselia, Jellicent
            "trick_room_setter", # second setter for redundancy
            "physical_attacker", # slow hard hitter
        ],
        "optional": [
            "special_attacker",  # slow special attacker
            "redirection",       # protect setter while setting TR
            "support",           # utility
        ]
    },
}