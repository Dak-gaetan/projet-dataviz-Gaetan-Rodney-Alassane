# Règles de nettoyage (couche silver)

Bronze : 4 849 004 lignes | Silver : 4 567 463 lignes | retirées : 281 541

| # | Règle | Justification | Lignes retirées |
|---|---|---|---|
| 1 | Identifiant de station manquant | Sans identifiant, la ligne ne peut être rattachée à aucune station. | 34 918 |
| 2 | Compteurs manquants ou illisibles | Capacité, places libres et vélos sont indispensables pour détecter pénuries et saturations. | 178 074 |
| 3 | Valeurs impossibles (négatives, capacité nulle) | Un nombre négatif de vélos ou de places, ou une capacité nulle, est une erreur de mesure. | 9 138 |
| 4 | Total de vélos différent de mécaniques + électriques | Le total doit être la somme des deux types ; sinon la ligne est incohérente. | 0 |
| 5 | Plus de vélos ou de places que la capacité | Incohérent avec la capacité de la station. | 9 025 |
| 6 | Station hors service | Une station hors service n'a pas de disponibilité réelle et fausserait les taux de pénurie. | 9 136 |
| 7 | Coordonnées manquantes ou hors Île-de-France | Sans coordonnées plausibles, la station ne peut pas être placée sur une carte. | 0 |
| 8 | Donnée non actualisée depuis plus de 6 h | Une station qui ne remonte plus d'information donne un état figé, pas la réalité. | 41 250 |
| 9 | Doublons (station, instantané) | Une même station ne doit apparaître qu'une fois par instantané. | 0 |
