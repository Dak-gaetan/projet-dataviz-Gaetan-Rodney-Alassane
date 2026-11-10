# Projet dataviz : Vélib, où et quand manque-t-il des vélos ?

Mastère Big Data & IA, M1, Sup de Vinci, session 2026-2027. Enseignant : M. L. Ndao.
Auteurs : Gaetan, Rodney, Alassane

## 1. Jeu de données

- **Source** : Paris Open Data, Vélib (disponibilité en temps réel + emplacement des stations).
- **Volume** : instantanés collectés toutes les 2 min, objectif ≥ 2 millions de lignes.
- **Dimensions** : temporelle (horodatage), géographique (station, arrondissement).
- **Téléchargement** : `scripts/telecharger_donnees.sh` puis `src/collecter_velib.py`.

## 2. Persona

**Le décideur** : le responsable de la régulation du parc Vélib, qui pilote les équipes déplaçant les vélos entre stations.

**Ce qu'il décide** : quelles stations réapprovisionner ou désengorger, à quels créneaux horaires et dans quels secteurs.

**Fréquence** : plusieurs fois par jour (tournée du jour) et chaque semaine (plan type semaine / week-end).

**Question principale** : quelles stations et quels secteurs manquent de vélos ou de places, et à quelles heures de la semaine ?

Détails dans [`docs/persona.md`](docs/persona.md).

## 3. Architecture

Données (CSV) → **bronze** (Delta, RustFS) → **silver** (nettoyé) → **gold** (agrégats, PostgreSQL) → **Streamlit**.
Ontologie `.ttl` + requêtes SPARQL pour la couche sémantique.

## 4. Lancer le projet

### Installations nécessaires (à faire une fois)

| Outil | Version | Pourquoi | Vérifier |
|---|---|---|---|
| Docker Desktop | récent, démarré (« Engine running ») | RustFS, PostgreSQL, Streamlit, collecte | `docker --version` |
| Git | récent | versionnage, scripts `.sh` via Git Bash | `git --version` |
| Python | **3.12** (pas 3.13 : PySpark 3.5 ne le supporte pas) | notebooks et PySpark | `py -3.12 --version` |
| Java (JDK) | **17** (pas 21 ni plus récent : Spark 3.5 ne démarre pas) | requis par Spark | `java -version` |
| VS Code + extensions Python et Jupyter | récent | exécuter les notebooks | |

Prévoir au moins 10 Go d'espace libre pour Docker et Spark (les bibliothèques Spark se téléchargent au premier lancement d'un notebook).

### Étape 1 : récupérer le dépôt et la configuration

```bash
git clone <url-du-depot>
cd projet-dataviz-nom1-nom2
```

Créer le fichier `.env` (il n'est pas versionné, il contient les identifiants locaux) :

```powershell
# PowerShell (Windows)
Copy-Item .env.example .env
```
```bash
# Git Bash / WSL / Linux / macOS
cp .env.example .env
```

Les valeurs par défaut conviennent pour un usage local.

### Étape 2 : télécharger les données

Les données ne sont pas versionnées. Depuis Git Bash ou WSL :

```bash
bash scripts/telecharger_donnees.sh
```

Le jeu temps réel ne fournit qu'un instantané à la fois (~1 500 stations). Pour accumuler l'historique (objectif ≥ 2 M de lignes), lancer la collecte continue et la laisser tourner (PC allumé, sans veille) :

```bash
docker compose --profile collect up -d collector
docker compose logs -f collector     # avancement en % de l'objectif
```

Un instantané toutes les 2 min (`COLLECT_INTERVAL_S` dans `.env`) : environ 2 M de lignes en 2 jours, une semaine complète de données en 7 jours.

### Étape 3 : démarrer les services Docker

```bash
docker compose up -d
```

Services démarrés : RustFS (data lake), PostgreSQL (gold), Streamlit (dashboard).
Vérifier : `docker compose ps`. Le bucket du data lake est créé par le notebook 01 (`from lake import creer_bucket`).

> JupyterLab dans Docker est disponible en option (`docker compose --profile jupyter up -d`) mais l'image est lourde. Par défaut, les notebooks tournent dans VS Code (étape 4).

### Étape 4 : environnement Python local et notebooks

Créer l'environnement Python et installer les paquets (une seule fois, à la racine du projet) :

```bash
# Git Bash (Windows)
py -3.12 -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```
```powershell
# PowerShell (Windows)
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
```bash
# Linux / macOS
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Dans VS Code : ouvrir un notebook, cliquer sur **Sélectionner le noyau** > **Environnements Python** > **`.venv`** (Python 3.12), puis exécuter dans l'ordre. L'activation du terminal n'est utile que pour installer les paquets.

Problèmes fréquents :
- `import pyspark` échoue : le noyau n'est pas `.venv`, ou Python n'est pas en 3.12.
- Spark ne démarre pas ou reste bloqué sans message : vérifier `java -version`. Si la version n'est pas 17 (par exemple 25), installer Temurin 17 et renseigner `SPARK_JAVA_HOME` dans `.env` (voir `.env.example`).
- Spark sous Windows signale `winutils` ou `HADOOP_HOME` : avertissement sans gravité pour la lecture, mais si l'écriture échoue, installer `winutils` pour Hadoop 3.3.

1. `01_extraction_bronze.ipynb`
2. `02_silver_gold.ipynb`
3. `03_rdf_sparql.ipynb`
4. `04_perception_avant_apres.ipynb`
5. `05_exploration.ipynb`

### Étape 5 : ouvrir le dashboard

http://localhost:8501 (disponible une fois la couche gold écrite dans PostgreSQL par le notebook 02).

### Arrêter / réinitialiser

```bash
docker compose down        # arrête les services (données conservées)
docker compose down -v     # arrête ET supprime les volumes (lake et PostgreSQL)
```

### Dépannage rapide

- `variable is not set` / `.env not found` : le fichier `.env` n'a pas été créé (étape 1).
- `pull access denied` : vérifier que Docker Desktop est démarré et connecté à Internet.
- Un service redémarre en boucle : `docker compose logs <service>` (ex. `rustfs`, `postgres`).

## URL des services

| Service | URL |
|---|---|
| JupyterLab | http://localhost:8888 |
| Spark UI | http://localhost:4040 |
| Console RustFS | http://localhost:9001 |
| Dashboard Streamlit | http://localhost:8501 |

## 5. Structure du dépôt

```
app/          dashboard Streamlit (Dockerfile, app.py)
docker/       image Jupyter/PySpark
docs/         persona, fiches KPI, règles de nettoyage
notebooks/    notebooks numérotés, à exécuter dans l'ordre
ontologie/    ontologie .ttl et requêtes SPARQL
scripts/      téléchargement des données, diagnostic
sql/          initialisation PostgreSQL
src/          code Python partagé (config, session Spark, collecte)
data/         données (non versionnées)
```

## 6. Conventions de travail

- Une branche par personne et par tâche, fusion par pull request relue.
- Commits clairs, à l'impératif, ex. `Ajoute la règle de nettoyage des stations hors service`.
