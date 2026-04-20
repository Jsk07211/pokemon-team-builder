# Strategy
* Long-term planning
  * Type synergy (weakness coverage, how it sets you up for the future)
* There needs to be a way to roughly guess the EV spreads of the opposing pokemon
  * These are most likely teams that have historical data maybe?
  * Need to understand what the team is trying to achieve

Role Coverage — this is probably the biggest gap. Type synergy alone doesn't build a functional team. You need to explicitly model:
* Hazard setter (Stealth Rock is nearly mandatory in Gen 6 OU)
* Hazard removal (Rapid Spin or Defog user)
* Revenge killer (usually a Choice Scarf user or priority abuser)
* Wallbreaker vs. Sweeper distinction
* Cleric/support (Wish passer, status absorber)

Speed Tiers — Gen 6 OU has very defined speed benchmarks (e.g., base 110 for Gengar/Latios, Talonflame's priority, Scarf thresholds). Your model needs to reason about who outspeeds whom before and after boosts.
The Mega Evolution slot — only one Mega per team, and it's the single highest-impact decision. It probably deserves its own dedicated selection step before filling the remaining 5 slots.

Win Condition Identification — your team needs a primary win condition and the other 5 slots should support it. Common archetypes in Gen 6 OU: setup sweeper (e.g., Mega Charizard X), VoltTurn momentum, weather (rain/sand), or stall. Your builder should classify which archetype it's building before slot-filling.

EV Spread Estimation — for this, supervised learning on Smogon's usage stats is actually the right call. They publish monthly CSVs with spread distributions per Pokemon per tier. You can train a small classifier: given a Pokemon's moveset and item, predict the most likely EV spread bucket. This is clean tabular ML (XGBoost works great here).

Threat Assessment / Team Weakness Audit — after generating a candidate team, you need a pass that checks: "Is this team 6-0'd by Landorus-T? Does anything beat a +2 Mega Kangaskhan?" This is essentially a coverage matrix check against a threat list of the top ~30 Gen 6 OU Pokemon.

Lure Sets and Deceptive Movesets — harder to model but important. A Garchomp running Fire Blast to lure Ferrothorn is a common pattern. Historical replay data is your best signal here.

Team Builder (RL Policy)
    └── Slot filler: GNN over existing team graph + threat matrix
    └── Mega selector: dedicated classifier (highest-impact choice)
    └── Role checker: constraint satisfaction over role coverage

In-Battle Agent (MCTS + NN)
    └── Value network: estimates win probability from game state
    └── Policy network: move/switch prior probabilities
    └── EV estimator: Bayesian update as opponent's stats are revealed in battle

Pretraining Data
    └── Smogon usage stats (EV spreads, common sets)
    └── Pokemon Showdown replays (pmariglia/showdown has tooling for this)

Multi-label over single-label classification
This is the easiest to defend. You can point to concrete examples — Landorus-T is simultaneously a hazard setter, pivot, and wallbreaker. Any interviewer who pushes back is just wrong, and the examples make that immediately obvious.
GAT over basic GCN
Solid reasoning: you need the model to learn which teammate relationships matter most, not just that relationships exist. Attention weights give you that, and they're interpretable — you can actually show which edges got reinforced after training. The interpretability angle is a strong secondary justification.
GNN over independent classification
The core argument is that role is context-dependent — a Trick Room setter label can't be assigned without seeing the rest of the team. Independent classifiers have no mechanism to capture that. This is a structural argument about the problem, not just a "GNNs are cool" argument, which is exactly what interviewers want to hear.
XGBoost as baseline
This one actually makes you look more credible, not less. Choosing a simpler baseline and explicitly evaluating against it shows you understand that architectural complexity needs to be justified empirically. A lot of junior candidates skip baselines entirely.

The one decision you should be ready to dig into is why GAT specifically over other GNN variants — GraphSAGE and GIN are also reasonable choices here. The honest answer is that attention weights map naturally onto the "edge reinforcement" concept you had early on, and they give you interpretable output that's useful for debugging the team builder. That's a legitimate reason, not a hand-wavy one.

# Sources
1. [Competitive Pokemon may be Impossible to Explain](https://www.youtube.com/watch?v=wrR6MquGU6A&t=14s)
2. Claude
