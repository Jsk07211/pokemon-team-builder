import pandas as pd
import json
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sklearn.metrics import silhouette_score
from collections import Counter

def encode_pokemon(data):
    stats = data["baseStats"]
    abilities = data["abilities"]
    moves = data["learnset"]
    return {
        # # base stats
        "hp": stats["hp"],
        "atk": stats["atk"],
        "def": stats["def"],
        "spa": stats["spa"],
        "spd": stats["spd"],
        "spe": stats["spe"],
        # derived stats
        "bulk_physical": stats["hp"] * stats["def"],
        "bulk_special": stats["hp"] * stats["spd"],
        "offensive_bias": stats["atk"] - stats["spa"],
        # weather setters (ability)
        "has_drizzle": int("Drizzle" in abilities),
        "has_drought": int("Drought" in abilities),
        "has_sand_stream": int("Sand Stream" in abilities),
        "has_snow_warning": int("Snow Warning" in abilities),
        # weather setters (move)
        "has_rain_dance": int("raindance" in moves),
        "has_sunny_day": int("sunnyday" in moves),
        "has_sandstorm": int("sandstorm" in moves),
        "has_hail": int("hail" in moves),
        # weather abusers
        "has_swift_swim": int("Swift Swim" in abilities),
        "has_chlorophyll": int("Chlorophyll" in abilities),
        "has_sand_rush": int("Sand Rush" in abilities),
        "has_sand_force": int("Sand Force" in abilities),
        # speed control
        "has_tailwind": int("tailwind" in moves),
        "has_trick_room": int("trickroom" in moves),
        "has_icy_wind": int("icywind" in moves),
        "has_thunder_wave": int("thunderwave" in moves),
        # doubles specific
        "has_spread_move": int(any(m in moves for m in
                                ["earthquake", "surf", "blizzard", "rockslide"])),
        "has_redirection": int(any(m in moves for m in
                                ["followme", "ragepowder"])),
        "has_fake_out": int("fakeout" in moves),
        # competitive abilities
        "has_prankster": int("Prankster" in abilities),
        "has_intimidate": int("Intimidate" in abilities),
        "has_levitate": int("Levitate" in abilities),
        "has_sturdy": int("Sturdy" in abilities),
        "has_magnet_pull": int("Magnet Pull" in abilities),
        "has_shadow_tag": int("Shadow Tag" in abilities),
        "has_trace": int("Trace" in abilities),
        "has_friend_guard": int("Friend Guard" in abilities),
    }

def get_smogon_label(name, smogon_sets):
    if name not in smogon_sets:
        return "No Label"
    return list(smogon_sets[name].keys())[0]

import json

def get_labels(smogon_sets):
    all_labels = set()
    for pokemon, sets in smogon_sets.items():
        for set_name in sets.keys():
            all_labels.add(set_name)

    for label in sorted(all_labels):
        print(label)

with open('gen6dou.json', 'r') as f:
    pokemon_data = json.load(f)
with open('smogon_sets_gen6doublesou.json', 'r') as f:
    smogon_sets = json.load(f)

smogon_names = set(smogon_sets.keys())
encoded = {pokemon: encode_pokemon(info) for pokemon, info in pokemon_data.items()}
df = pd.DataFrame(encoded).T

df['bst'] = df[['hp', 'atk', 'def', 'spa', 'spd', 'spe']].sum(axis=1)
df_filtered = df[(df['bst'] >= 400) | (df.index.isin(smogon_names))]
df_filtered = df_filtered.drop(columns=['bst'])

df_filtered['bulk_physical'] = df_filtered['hp'] * df_filtered['def']
df_filtered['bulk_special'] = df_filtered['hp'] * df_filtered['spd']
df_filtered['offensive_bias'] = df_filtered['atk'] - df_filtered['spa']
df_filtered = df_filtered.drop(columns=['hp', 'def', 'spd', 'atk', 'spa'])

X = StandardScaler().fit_transform(df_filtered)
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X)

# observe PCA results
plt.scatter(X_pca[:, 0], X_pca[:, 1])
for i, name in enumerate(smogon_names):
    plt.annotate(name, (X_pca[i, 0], X_pca[i, 1]), fontsize=8)
plt.savefig('data_exploration/results/pca_plot.png', dpi=150, bbox_inches='tight')

# elbow method
inertias = []
k_range = range(2, 20)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_pca)
    inertias.append(kmeans.inertia_)

plt.figure()
plt.plot(k_range, inertias, 'bo-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.savefig('data_exploration/results/elbow.png', dpi=150, bbox_inches='tight')

# smogon labels
df_filtered = df_filtered.copy()
df_filtered['smogon_label'] = [get_smogon_label(name, smogon_sets)
                                for name in df_filtered.index]

# infer labels for unlabeled pokemon from nearest labeled neighbor
labeled_mask = df_filtered['smogon_label'] != 'No Label'
unlabeled_mask = ~labeled_mask

X_labeled = X_pca[labeled_mask.values]
X_unlabeled = X_pca[unlabeled_mask.values]
labels_labeled = df_filtered['smogon_label'][labeled_mask].values

distances = cdist(X_unlabeled, X_labeled)
nearest_idx = distances.argmin(axis=1)
inferred_labels = labels_labeled[nearest_idx]

df_filtered['smogon_label_inferred'] = df_filtered['smogon_label'].copy()
df_filtered.loc[unlabeled_mask, 'smogon_label_inferred'] = inferred_labels

# plot with inferred labels
labels = df_filtered['smogon_label_inferred'].values
unique_labels = list(set(labels))
colors = cm.tab20(np.linspace(0, 1, len(unique_labels)))
color_map = dict(zip(unique_labels, colors))

fig, ax = plt.subplots(figsize=(14, 10))
for name, x, y, label in zip(df_filtered.index, X_pca[:, 0], X_pca[:, 1], labels):
    ax.scatter(x, y, color=color_map[label], alpha=0.7)
    ax.annotate(name, (x, y), fontsize=6)

for label, color in color_map.items():
    ax.scatter([], [], color=color, label=label)
ax.legend(fontsize=7, loc='upper right', bbox_to_anchor=(1.3, 1))
plt.savefig('data_exploration/results/pca_smogon_labels.png', dpi=150, bbox_inches='tight')

# silhouette scores
print("Silhouette scores:")
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42, init='k-means++', n_init=20)
    cluster_labels = kmeans.fit_predict(X_pca)
    if len(set(cluster_labels)) > 1:  # silhouette needs at least 2 clusters
        score = silhouette_score(X_pca, cluster_labels)
        print(f"  k={k}: {score:.3f}")

# cluster inspection
k = 4
kmeans = KMeans(n_clusters=k, random_state=42, init='k-means++', n_init=20)
df_filtered['cluster'] = kmeans.fit_predict(X_pca)

for cluster_id in range(k):
    cluster_pokemon = df_filtered[df_filtered['cluster'] == cluster_id].index.tolist()
    cluster_labels = df_filtered[df_filtered['cluster'] == cluster_id]['smogon_label'].values
    labeled_only = [l for l in cluster_labels if l != 'No Label']

    if labeled_only:
        counter = Counter(labeled_only)
        most_common = counter.most_common(1)[0]
        purity = most_common[1] / len(labeled_only)
        print(f"\nCluster {cluster_id} (purity: {purity:.2f}, dominant: {most_common[0]}, labeled: {len(labeled_only)}/{len(cluster_pokemon)}):")
    else:
        print(f"\nCluster {cluster_id} (no labeled pokemon):")

    for name in cluster_pokemon:
        if name in smogon_sets:
            set_names = list(smogon_sets[name].keys())
            print(f"  {name}: {set_names}")

# save
output = {}
for name in df_filtered.index:
    output[name] = {
        'cluster': int(df_filtered.loc[name, 'cluster']),
        'smogon_label': df_filtered.loc[name, 'smogon_label'],
        'inferred_label': df_filtered.loc[name, 'smogon_label_inferred'],
    }
with open('data_exploration/results/pokemon_roles.json', 'w') as f:
    json.dump(output, f, indent=2)