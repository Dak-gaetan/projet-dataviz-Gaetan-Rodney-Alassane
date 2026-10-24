# Projet dataviz : Vélib, où et quand manque-t-il des vélos ?

Mastère Big Data & IA, M1, Sup de Vinci, session 2026-2027. Enseignant : M. L. Ndao.
Auteurs : [Prénom Nom 1], [Prénom Nom 2]

## 1. Jeu de données

- **Source** : Paris Open Data, Vélib (disponibilité en temps réel + emplacement des stations).
- **Volume** : instantanés collectés toutes les 5 min, objectif ≥ 2 millions de lignes.
- **Dimensions** : temporelle (horodatage), géographique (station, arrondissement).
- **Téléchargement** : `scripts/telecharger_donnees.sh` puis `src/collecter_velib.py`.

## 2. Persona

[À compléter : qui est le décideur, ce qu'il décide, à quelle fréquence.]

**Question principale** : [À compléter]

## 3. Architecture

Données (CSV) → **bronze** (Delta, RustFS) → **silver** (nettoyé) → **gold** (agrégats, PostgreSQL) → **Streamlit**.
Ontologie `.ttl` + requêtes SPARQL pour la couche sémantique.

## 4. Lancer le projet

**Prérequis** : Docker Desktop démarré, Git, et (pour les scripts `.sh` sous Windows) Git Bash ou WSL.

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

Le jeu temps réel ne fournit qu'un instantané à la fois. Pour accumuler l'historique (objectif ≥ 2 M de lignes), lancer la collecte et la laisser tourner plusieurs jours :

```bash
python src/collecter_velib.py
```

### Étape 3 : démarrer les services

```bash
docker compose up -d
```

> **Premier lancement long (plusieurs minutes)** : Docker télécharge les images et construit celle de Jupyter/PySpark (plusieurs Go). Spark télécharge aussi ses bibliothèques (Delta, S3, PostgreSQL) à la première exécution d'un notebook. Les lancements suivants sont rapides.

Vérifier que tout tourne : `docker compose ps` (ou `bash scripts/diagnostic.sh`).

Services démarrés : RustFS (data lake), PostgreSQL (gold), JupyterLab + Spark, Streamlit.
Le bucket du data lake est créé par le notebook 01 (`from lake import creer_bucket`).

### Étape 4 : exécuter les notebooks dans l'ordre

JupyterLab : http://localhost:8888 (token : valeur de `JUPYTER_TOKEN` dans `.env`, `velib` par défaut).

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
