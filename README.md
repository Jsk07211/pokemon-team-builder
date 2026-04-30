## Pokemon Gen 6 OU Team Builder

https://github.com/pkmn/smogon/tree/main/smogon - retrieve data of a pokemon
https://pokeapi.co/docs/v2#pokemon-section - retrieves more data!

discussion:
https://www.smogon.com/forums/threads/ou-tier-api.3772302/

Pokemon eligible for Gen 9 OU include any species listed in formats-data.ts with a tier of OU, UU, RU, NU, or lower, as tiers are upwardly inclusive, excluding only Ubers and Anything Goes. To reconcile with generation info, cross-reference species with a Pokédex source or check specific generational mods for past-gen data.
https://github.com/smogon/pokemon-showdown/blob/master/data/formats-data.ts


### Phase 1 — Data Pipeline
- [ ] Parse Smogon Gen 6 OU usage stat files (monthly CSVs)
- [ ] Extract per-Pokemon moveset distributions
- [ ] Extract EV spread distributions per moveset
- [ ] Extract teammate co-occurrence rates
- [ ] Store as structured, queryable format (dict or SQLite)

### Phase 2 — Role Classifier
- [ ] Define multi-label role taxonomy (`hazard_setter`, `hazard_remover`, `setup_sweeper`, `wallbreaker`, `revenge_killer`, `wall`, `cleric`, `pivot`, `win_condition`)
- [ ] Build rule-based label bootstrapper from moveset + item features
- [ ] Extract per-Pokemon set features (moves, item, stats, typing)
- [ ] Train multi-label GNN (GAT) for role classification in PyTorch Geometric
- [ ] Train XGBoost baseline for comparison
- [ ] Evaluate per-role F1 score, confirm GNN outperforms baseline

### Phase 3 — Archetype Classifier
- [ ] Define archetype label set (`hyper_offense`, `balance`, `volt_turn`, `weather_sun`, `weather_rain`, `weather_sand`, `trick_room`, `stall`)
- [ ] Engineer team-level aggregate features (avg speed, weather abilities, TR presence, Mega slot)
- [ ] Train multiclass archetype classifier
- [ ] Validate on held-out teams from replay data

### Phase 4 — Team Builder
- [ ] Implement Mega Evolution selector (first slot, dedicated step)
- [ ] Implement greedy slot filler using Smogon teammate co-occurrence as ranking prior
- [ ] Add role coverage constraint checker (ensure all required roles are filled)
- [ ] Add type synergy filter (penalise overlapping weaknesses)
- [ ] Add speed tier validator (ensure at least one Pokemon beats key speed benchmarks)
- [ ] Wire archetype classifier output as conditioning input to slot filler
- [ ] End-to-end test: seed Pokemon in → valid role-complete team out

# Ideal Project Layout
```
gen6ou-team-builder/
│
├── README.md
├── requirements.txt
├── .gitignore
├── pyproject.toml
│
├── data/
│   ├── raw/                    # unmodified smogon stat files
│   └── processed/              # cleaned, queryable outputs
│
├── teambuilder/                # main package
│   ├── __init__.py
│   ├── models.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── scraper.py          # fetches smogon usage stat files
│   │   ├── parser.py           # parses raw stat text into structured dicts
│   │   └── store.py            # reads/writes processed data to disk
│   │
│   ├── classifier/
│   │   ├── __init__.py
│   │   ├── rules.py            # rule-based label bootstrapper
│   │   ├── features.py         # feature engineering for sets and teams
│   │   ├── role_classifier.py  # GAT multi-label role model
│   │   └── archetype_classifier.py  # team-level multiclass model
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── team_graph.py       # builds PyG Data object from a team
│   │   └── gat.py              # GAT model definition
│   │
│   ├── builder/
│   │   ├── __init__.py
│   │   ├── mega_selector.py    # dedicated mega evolution selection step
│   │   ├── slot_filler.py      # greedy slot filling logic
│   │   └── validator.py        # role coverage, type synergy, speed tier checks
│   │
│   └── constants.py            # role taxonomy, archetype labels, speed tiers
│
├── scripts/
│   ├── fetch_data.py           # one-off: pull smogon stats
│   ├── train_role_classifier.py
│   └── train_archetype_classifier.py
│
├── models/                     # saved model weights, gitignored if large
│   └── .gitkeep
│
└── tests/
    ├── test_parser.py
    ├── test_rules.py
    ├── test_team_graph.py
    └── test_validator.py
```

ran `python -m showdown_server.server` to make server.py a `showdown_server` a module
* tells python to act as if server.py is the main entry point for this session
* code executes from here